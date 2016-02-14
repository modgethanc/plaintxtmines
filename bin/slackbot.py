#!/usr/bin/python

from slackclient import SlackClient
import os
import sys
from optparse import OptionParser

import json
import fileinput
import random
import re
import time as systime
import threading

import formatter
import inflect
import txtminebot

### config

p = inflect.engine()
tokenfile = open("slack4token", 'r')
for x in tokenfile:
  token = x.rstrip()

sc = SlackClient(token)
botname = "txtminebot"
txtminebot.init()

### slack API handling

def scrape(data): # interprects a json dict
  return json.loads(json.dumps(data))

def collection(type): # stupid hardcoding types from api for get_target
  if type == "users":
    return 'members'
  elif type == "im":
    return 'ims'
  else:
    return type

def get_target(name, type, source, target):
  # returns value of <target> when given value <name> of field <source> of
  # collective <type> from a .list method
  # valid types: "channels", "users", "im", "reactions", "groups", "emoji"

  # sample: get_target(chanName, "channels", "name", "id") will return the id
  # of channel channel called chanName

  for x in json.loads(sc.api_call(type+".list"))[collection(type)]:
    data = scrape(x)
    if data[source] == name:
      return data[target]

  #print name + " not found"
  return ""

### SHORTCUT HELPERS
def get_nick(msg_raw): # retrieve nick from raw message
  return get_target(msg_raw['user'], "users", "id", "name")

def get_time(msg_raw): # retrieve time from raw message
  return systime.localtime(float(msg_raw['ts']))

### helper functions

def is_pm(msg_raw): #determine if a message is a pm; SUPER UGLY
  id = msg_raw['channel']
  for x in json.loads(sc.api_call("im.list"))["ims"]:
    data = scrape(x)
    if data['id'] == id:
      return True
  return False

def is_listen(msg_raw, chan): #determine if a message is in a targeted channel
  return msg_raw['channel'] == get_target(chan, "channels", "name", "id")

### chat functions

def say(chan, msg, nick=""):
  if nick:
    msg = "@" + nick + " " + msg

  sc.api_call("chat.postMessage", channel=get_target(chan, "channels", "name", "id"), text=msg, as_user="true")

  return msg

def multisay(chan, msglist, nick=""):
 for x in msglist:
   say(chan, x, nick)

def pm(nick, msg):
  id = get_target(nick, "users", "name", "id")
  chan = get_target(id, "im", "user", "id")

  sc.api_call("chat.postMessage", channel=chan, text=msg, as_user="true")

###

def listen(chan):
  if sc.rtm_connect():
    time = systime.localtime()
    date = systime.strftime("%Y-%m-%d",time)
    sc.api_call("users.setPresence", presence="auto")

    while True:
      time = systime.localtime()
      date = systime.strftime("%Y-%m-%d",time)

      try:
        msglist = sc.rtm_read()
        for x in msglist:
          #print x
          msg_raw = scrape(x)
          msgType = msg_raw['type']
          #print msgType
          nick = get_target(msg_raw['user'], "users", "id", "name")
          if msgType == 'message':
            ## extracting info to more readable names
            ts   = float(msg_raw['ts'])
            time = systime.localtime(ts)
            date = systime.strftime("%Y-%m-%d", time)
            msg  = msg_raw['text']
            msgChan = get_target(msg_raw['channel'], "channels", "id", "name")
            #print irc_style(msg_raw)
            if (is_listen(msg_raw, chan) or is_pm(msg_raw)):
              if not nick == botname:
                  multisay(chan, txtminebot.handle(nick, ts, msg), nick)
        systime.sleep(1)

      except KeyboardInterrupt:
        #print "killed"
        sc.api_call("users.setPresence", presence="away")
        return

      except:
        continue

  else:
    print("nak")
