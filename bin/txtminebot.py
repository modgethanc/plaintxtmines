#!/usr/bin/python

import socket
import os
import os.path
import sys
from optparse import OptionParser
import random

import formatter
import mines
import players
import gibber
import empress

### CONFIG

configfile = open("ircconfig", 'r')
config = []

for x in configfile:
    config.append(x.rstrip())

configfile.close()

botName = config[2]
admin   = config[3]

parser = OptionParser()

parser.add_option("-s", "--server", dest="server", default=config[0], help="the server to connect to", metavar="SERVER")
parser.add_option("-c", "--channel", dest="channel", default=config[1], help="the channel to join", metavar="CHANNEL")
parser.add_option("-n", "--nick", dest="nick", default=botName, help="the nick to use", metavar="NICK")

(options, args) = parser.parse_args()

## gameplay config defaults

baseFatigue     = 10

file_commands   = "lang/commands.txt"
file_interp_pos = "lang/interp-pos.txt"
file_interp_neu = "lang/interp-neu.txt"
file_interp_neg = "lang/interp-neg.txt"
file_wham = "lang/wham.txt"

if config[4]:
    baseFatigue = int(config[4])
if config[5]:
    file_commands = config[5]
if config[6]:
    file_interp_pos = config[6]
if config[7]:
    file_interp_neu = config[7]
if config[8]:
    file_interp_neg = config[8]
if config[9]:
    file_wham = config[9]

## lang import

COMMANDS = []
for x in open(file_commands):
    COMMANDS.append(x.rstrip())

INTERP_POS = []
for x in open(file_interp_pos):
    INTERP_POS.append(x.rstrip())

INTERP_NEU = []
for x in open(file_interp_neu):
    INTERP_NEU.append(x.rstrip())

INTERP_NEG = []
for x in open(file_interp_neg):
    INTERP_NEG.append(x.rstrip())

WHAM = []
for x in open(file_wham):
    WHAM.append(x.rstrip())

### irc functions 

def ping():
  ircsock.send("PONG :pingis\n")

def joinchan(chan):
  ircsock.send("JOIN "+ chan +"\n")

def connect(server, channel, botnick):
  ircsock.connect((server, 6667))
  ircsock.send("USER "+botnick+" "+botnick+" "+botnick+" :"+admin+"\n")
  ircsock.send("NICK "+botnick+"\n")

  joinchan(channel)

### meta functions

def isPlaying(player):
    return os.path.isfile('../data/'+player+'.player')

### gameplay functions

def newPlayer(msg, channel, user):
    players.new(user)
    playerlist = open("../data/players.txt", 'a')
    playerlist.write(user+"\n")
    playerlist.close()

    ircsock.send("PRIVMSG "+channel+" :"+ user + ": New dossier created.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with '!open'.\n")

    return user

def newMine(msg, channel, user):
    mine = players.newMine(user, "standardrates").capitalize()
    ircsock.send("PRIVMSG "+ channel +" :"+ user + ": Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+mine+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts, and begin with an enthusiastic '!strike'.\n")

    return mine

def excavate(msg, channel, user, time):
    diff = int(time)-int(players.lastMined(user))
    if diff < baseFatigue: # fatigue check
        left =  baseFatigue - diff
        fatigue = left * 2
        time = int(time) + fatigue - baseFatigue

        ircsock.send("PRIVMSG "+ user +" :You're still tired from your last attempt.  You'll be ready again in "+str(fatigue)+" seconds.  Please take breaks to prevent fatigue.\n")

    else: # actual mining actions
        mineList = players.getMines(user)
        emptyMines = []
        for x in mineList:
            mined = players.printExcavation(players.acquire(user, players.excavate(user, x)))
            ircsock.send("PRIVMSG "+ user +" :\x03" + random.choice(['4', '8', '9', '11', '12', '13'])+random.choice(['WHAM! ', 'CRASH!', 'BANG! ', 'KLANG!', 'CLUNK!', 'PLINK!', 'DINK! '])+"\x03  You struck at " + x.capitalize() +" and excavated "+mined+"\n")

            if mines.remaining("../data/"+x+".mine") == 0:
                emptyMines.append(x)
                ircsock.send("PRIVMSG "+ user +" :"+x.capitalize()+" is now empty.  The empress shall be pleased with your progress.  I'll remove it from your dossier now.\n")
       
        for x in emptyMines:
                mineList.remove(x)
 
	players.updateMines(user, mineList)

    players.updateLast(user, time)

def report(msg, channel, user):
    ircsock.send("PRIVMSG "+ user +" :You have acquired the following resources: "+players.report(user)+"\n")
    ircsock.send("PRIVMSG "+ user +" :"+mineList(msg, channel, user)+"\n")

def grovel(msg, channel, user, time):
    statement = '\x03' + random.choice(['4', '8', '9', '11', '12', '13']) + str(empress.speak()).rstrip()
    commentfile = open("empresscomments.txt", 'r')
    comments = []
    for x in commentfile:
        comments.append(x.rstrip())
    
    ircsock.send("PRIVMSG "+ channel + " :" + user +": The empress "+random.choice(['says', 'states', 'replies', 'snaps', 'mumbles', 'mutters'])+", \""+statement+"\x03\"  "+random.choice(comments)+"\n")

def stirke(msg, channel, user, time): #hazelnut memorial disfeature
    a = 0

def fatigue(msg, channel, user, time): #~krowbar memorial feature
    diff = int(time)-int(players.lastMined(user))
    if diff < baseFatigue: # fatigue check
        fatigue =  baseFatigue - diff

        ircsock.send("PRIVMSG "+ channel + " :" + user +": You'll be ready to strike again in "+str(fatigue)+" seconds.  Please rest patiently so you do not stress your body.\n")
    else:
        ircsock.send("PRIVMSG "+ channel + " :" + user +": You're refreshed and ready to mine.  Take care to not overwork; a broken body is no use to the empress.\n")

def mineList(msg, channel, user):
    plural = ''
    if len(players.getMines(user)) > 0:
        plural = 's'

    prejoin = []

    rawList = players.getMines(user)
    for x in rawList:
        depletion = int(100*float(mines.remaining("../data/"+x+".mine"))/float(mines.starting("../data/"+x+".mine")))

        color = '' 
        if depletion > 98:
            color += "\x0311"
        elif depletion > 90:
            color += "\x0309"
        elif depletion > 49:
            color += "\x0308"
        elif depletion > 24:
            color += "\x0307"
        elif depletion > 9:
            color += "\x0304"
        else:
            color += "\x0305"

        prejoin.append(x.capitalize() + " (" + color + str(depletion) + "%\x03)")

    j = ", "
    return "You own the following mine"+plural+": "+j.join(prejoin)

def rankings(msg, channel, user):
    dossiers = []
    playerlist = open("../data/players.txt", 'r')
    for x in playerlist:
       dossiers.append(x.rstrip())
    playerlist.close()

    records = [] 
    for x in dossiers:
        records.append([x, str(players.totalResources(x))])

    records.sort(key=lambda entry:int(entry[1]), reverse=True)
    ircsock.send("PRIVMSG " + channel + " :The top most productive citizens are:\n")
    
    for x in range (0, 5):
        entry = records[x]
        ircsock.send("PRIVMSG " + channel + " :" + entry[0] + " with " + entry[1] + " units\n") 

###########################

def listen():
  while 1:
    msg = ircsock.recv(2048)

    if msg.find("PING :") != -1:
      ping()

    msg = msg.strip('\n\r').lower() #case insensitive
    formatted = formatter.format_message(msg)

    if "" == formatted:
      continue

    nick = msg.split("!")[0].split(":")[1]

    split       = formatted.split("\t")
    time        = split[0]
    user        = split[1]
    command     = split[2]
    channel     = split[3] #if you include the :: we can do slicker PM
    messageText = split[4]

    #print msg
    #print formatted
    
    if nick != user: #check for weird identity stuff
        user = nick

    if channel == botName:  #check for PM
        channel = user


    if channel == botName or msg.find(":!") != -1: #only log PM and commands
        logfile = open("irclog", 'a')
        logfile.write(msg+"\n")
        logfile.close()

    ###### admin commands
    if msg.find(":!join") != -1 and user == admin:
        split = msg.split(" ");
        for x in split:
            if x.find("#") != -1:
                joinchan(x)

    if msg.find(":!forcenew") != -1:
        if user == admin:
            split = msg.split(" ");
            for x in split:
                if isPlaying(x):
                    newMine(msg, x, x)
        else:
            ircsock.send("PRIVMSG "+ channel +" :"+ user + ": Sorry, friend, but only "+admin+" can force new mines right now.\n")

    ###### gameplay commands
    if msg.find(":!rollcall") != -1: # tildetown specific
        ircsock.send("PRIVMSG "+ channel +" :I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike, !report, !fatigue, !grovel, !rankings, !info.\n")

    elif msg.find(":!"+COMMANDS[7]) != -1: # !info
        ircsock.send("PRIVMSG "+ channel +" :"+ user + ": I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike, !report, !fatigue, !grovel, !rankings, !info.\n")

    elif msg.find(":!"+COMMANDS[0]) != -1: # !init
        if isPlaying(user):
            ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You already have a dossier in my records, friend.\n")
        else:
            newPlayer(msg, channel, user)

    elif msg.find(":!"+COMMANDS[1]) != -1: # !open
        if isPlaying(user):
            if len(players.getMines(user)) == 0:
                 newMine(msg, channel, user)
            else: 
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You have already been assigned your alotted mine.  Perhaps in the future, the empress will permit further ventures.\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I can't open a mine for you until you have a dossier in my records, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[2]) != -1: # !mines
        if isPlaying(user):
            if len(players.getMines(user)) == 0:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else: 
                ircsock.send("PRIVMSG "+channel+" :" + user + ": "+mineList(msg, channel, user)+"\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[3]) != -1: # !strike
        if isPlaying(user):
            if len(players.getMines(user)) == 0:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else: 
                excavate(msg, channel, user, time)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[5]) != -1: # !fatigue
        if isPlaying(user):
            fatigue(msg, channel, user, time)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[6]) != -1: # !grovel
        if isPlaying(user):
            grovel(msg, channel, user, time)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I advise against groveling unless you're in my records, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[4]) != -1: # !report
        if isPlaying(user):
            report(msg, channel, user)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[8]) != -1: # !rankings
        rankings(msg, channel, user)

#########################
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
