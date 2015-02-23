#!/usr/bin/python

import socket
import os
import os.path
import sys
from optparse import OptionParser

import formatter
import mines
import players
import names

### IRC CONFIG

configfile = open("ircconfig", 'r')
config = []

for x in configfile:
    config.append(x.rstrip())

configfile.close()

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default=config[0], help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default=config[1], help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default=config[2], help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

###

def ping():
  ircsock.send("PONG :pingis\n")

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :"+config[3]+"\n")
  ircsock.send("NICK "+ botnick +"\n")

  joinchan(channel)

###

def newPlayer(msg, channel, user):
    players.new(user)
    ircsock.send("PRIVMSG "+ channel +" :"+ user + ": New dossier created.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with '!open'.\n")

def newMine(msg, channel, user):
    mine = players.newMine(user, "standardrates").capitalize()
    ircsock.send("PRIVMSG "+ channel +" :"+ user + ": Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+mine+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts.\n")

def excavate(msg, channel, user):
    mineList = players.getMines(user)
    for x in mineList:
        mined = players.printExcavation(players.acquire(user, players.excavate(user, x)))
        ircsock.send("PRIVMSG "+ user +" :WHAM!  You struck at " + x.capitalize() +" and excavated the following: "+mined+"\n")

def report(msg, channel, user):
    ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You have acquired the following resources: "+players.report(user)+"\n")

###########################

def listen():
  lastTick = 0

  while 1:
    msg = ircsock.recv(2048)
    msg = msg.strip('\n\r')

    if msg.find("PING :") != -1:
      ping()

    formatted = formatter.format_message(msg)

    if "" == formatted:
      continue

    #print formatted
    #user = msg.split("!")[0].split(":")[1]

    split = formatted.split("\t")
    time = split[0]
    user = split[1]
    command = split[2]
    channel = split[3]
    messageText = split[4]

    #print command
    #print user
    #print channel

    if user == "nbsp":
        user = "hvincent"

    #print msg

    if channel == config[2] or msg.find(":!") != -1:
        logfile = open("irclog", 'a')
        logfile.write(formatted+"\n")
        logfile.close()

    #####  meta commands
    if msg.find(":!join") != -1:
        split = msg.split(" ");
        for x in split:
            if x.find("#") != -1:
                joinchan(x)

    ###### gameplay
    if msg.find(":!rollcall") != -1:
        ircsock.send("PRIVMSG "+ channel +" :I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike, !report, !info.\n")

    if msg.find(":!info") != -1:
        ircsock.send("PRIVMSG "+ channel +" :"+ user + ": I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike, !report, !info.\n")

    if msg.find(":!init") != -1:
        if os.path.isfile('../data/'+user+'.player'):
            ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You already have a dossier in my records, friend.\n")
        else:
            newPlayer(msg, channel, user)

    if msg.find(":!open") != -1:
        if os.path.isfile('../data/'+user+'.player'):
            if len(players.getMines(user)) == 0:
                 newMine(msg, channel, user)
            else: 
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You have already been assigned your alotted mine.  Perhaps in the future, the empress will permit further ventures.\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I can't open a mine for you until you have a dossier in my records, friend.  Request a new dossier with '!init'.\n")

    if msg.find(":!mines") != -1:
        if os.path.isfile('../data/'+user+'.player'):
            if len(players.getMines(user)) == 0:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else: 
                plural = ''
                if len(players.getMines(user)) > 0:
                    plural = 's'
                j = ', '
                mines = j.join(players.getMines(user)).capitalize()
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You own the following mine"+plural+": "+mines+"\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    if msg.find(":!strike") != -1:
        if os.path.isfile('../data/'+user+'.player'):
            if len(players.getMines(user)) == 0:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else: 
                excavate(msg, channel, user)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    if msg.find(":!report") != -1:
        if os.path.isfile('../data/'+user+'.player'):
            report(msg, channel, user)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

#########################
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
