#!/usr/bin/python

import socket
import os
import sys
from optparse import OptionParser

import formatter
import mines
import players
import names

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default='irc.freenode.net', help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default='#kvincent', help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default='txtminebot', help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

def ping():
  ircsock.send("PONG :pingis\n")

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :hvincent\n") 
  ircsock.send("NICK "+ botnick +"\n")

  joinchan(channel)


###########################

def listen():
  while 1:
    msg = ircsock.recv(2048)
    msg = ircmsg.strip('\n\r')

    if ircmsg.find("PING :") != -1:
      ping()

    formatted = formatter.format_message(ircmsg)

    if "" == formatted:
      continue

    split = formatted.split("\t")
    time = split[0]
    user = split[1]
    command = split[2]
    channel = split[3]
    messageText = split[4]

    if msg.find("!join") != -1:
        #ircsock.send("PRIVMSG " + channel + " :" + user + ": k\n")
        split = msg.split(" ");
        for x in split:
            if x.find("#") != -1:
                joinchan(x)

#########################
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
