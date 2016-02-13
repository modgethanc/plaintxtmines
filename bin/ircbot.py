#!/usr/bin/python

import socket
import os
import sys
import fileinput
import random
import re
import time as systime
import imp

import formatter
import txtminebot

config = []
channels = []

configfile = open("ircconfig", "r")
for x in configfile:
    config.append(x.rstrip())
configfile.close()

SERVER = config[0]
CHAN = config[1]
BOTNAME = config[2]
ADMIN = config[3]
TEST = "testicles"

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(msg):
    ircsock.send(msg.encode())

### irc functions

def ping():
  send("PONG :pingis\n")

def joinchan(chan):
  channels.append(chan)
  send("JOIN "+ chan +"\n")

def part(chan):
  channels.remove(chan)
  send("PART "+ chan +"\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))

  send("USER "+botnick+" "+botnick+" "+botnick+" :"+ADMIN+"\n")
  send("NICK "+botnick+"\n")

  joinchan(channel)

def disconnect():
  send("QUIT " +"\n")

def say(channel, msg, nick=""):
  if nick == channel: #don't repeat nick if in PM
    nick = ""
  elif nick:
    nick += ": "

  #print "trying to say: " + channel + ":>" + nick+msg
  #print ":::PRIVMSG "+channel+" :"+nick+msg+":::"
  send("PRIVMSG "+channel+" :"+nick+msg+"\n")

def multisay(channel, msglist, nick=""):
 for x in msglist:
   say(channel, x, nick)

def wall(msg):
  global channels
  for x in channels:
    say(x, msg)

def multiwall(msglist):
  global channels
  for x in msglist:
    wall(x)

## admin

def adminPanel(channel, user, time, msg):
  if msg.find(":!join") != -1:
    split = msg.split(" ")
    for x in split:
      if x.find("#") != -1:
        joinchan(x)
        say(channel, "joining "+x, user)

    return "join"

  elif msg.find(":!brb") != -1:
    say(channel, "leaving this channel", user)
    split = msg.split(" ")
    part(channel)
    return "part"

  elif msg.find(":!gtfo") != -1:
    say(channel, "disconnecting")
    #print "manual shutdown"
    disconnect()
    return "die"

  elif msg.find(":!names") != -1:
    ircsock.send("NAMES "+channel+"\n")
    return "names"

  elif msg.find(":!channels") != -1:
    chanlist = " ".join(channels)
    say(channel, "i'm in "+chanlist)
    return "channels"

  elif msg.find(":!wall") != -1:
    split = msg.split("!wall ")
    wallmsg = "".join(split[1])
    wall(wallmsg)

    return "wall"

def listen():
  while 1:
    msg = ircsock.recv(2048).decode()
    print(msg)
    if msg:
      receive(msg)

def receive(msg):
      #print msg

    if msg.find("PING :") != -1:
        return ping()

    msg = msg.strip('\n\r')
    process = msg.split(" ")

    nick = ""

    if len(msg.split("!")[0].split(":")) > 1:
        nick = msg.split("!")[0].split(":")[1]

    time = int(systime.time())
    user = nick
    command = ""
    channel = ""
    mode = ""
    target = ""
    message = ""

    if len(process) > 1:
        command = process[1]
    if len(process) > 2:
        channel = process[2]
    if len(process) > 3:
        if command == "MODE":
            mode = process[3]
            if len(process) > 4:
                target = process[4]
        else:
            message = " ".join(process[3:])

    #print("command: "+command)
    formatted = formatter.format_message(msg)

    if formatted != "":
        user = formatted.split("\t")[1]

    if nick != user: #check for weird identity stuff
          user = nick

    if channel == BOTNAME:  #check for PM
        channel = user

    #if msg.find("JOIN #") != -1:
      #  ircsock.send("MODE "+channel+" +o "+user+"\n")
      #  say(channel, kvincent.seen(channel, user))

    if user == ADMIN:
        code = adminPanel(channel, user, time, message)

    if command == "PRIVMSG":
        response = txtminebot.handle(user, time, message)

        if response:
            multisay(channel, response, user)

    sys.stdout.flush()

#########################
def start():
    connect(SERVER, CHAN, BOTNAME)

def reload():
    imp.reload(txtminebot)
    txtminebot.init()
