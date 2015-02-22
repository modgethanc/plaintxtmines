#!/usr/bin/python

import socket
import os
import sys
from optparse import OptionParser

import formatter

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default='irc.freenode.net', help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default='#kvincent', help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default='txtminebot', help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :hvincent\n") # user authentication
  ircsock.send("NICK "+ botnick +"\n")

  joinchan(channel)

def listen():
  while 1:
    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip('\n\r')

    formatted = formatter.format_message(ircmsg)

    if "" == formatted:
      continue

    # print formatted

    split = formatted.split("\t")
    time = split[0]
    user = split[1]
    command = split[2]
    channel = split[3]
    messageText = split[4]

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
