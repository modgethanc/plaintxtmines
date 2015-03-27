#!/usr/bin/python

import socket
import os
import os.path
import sys
import time as systime
from optparse import OptionParser
import random
import inflect
from datetime import datetime

import formatter
import mines
import players
import gibber
import empress
import golems

### CONFIG
p = inflect.engine()
j = ", "

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

def listDossiers():
    gamedata = os.listdir('../data/')
    playerlist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "dossier":
            playerlist.append(entry[0])
    return playerlist

dossierList = listDossiers()
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

def isPlaying(user):
    return os.path.isfile('../data/'+user+'.dossier')

def isMine(mine):
    return os.path.isfile('../data/'+mine+'.mine')

def hasGolem(user):
    return os.path.isfile('../data/'+user+'.golem')

def listPlayers():
    gamedata = os.listdir('../data/')
    playerlist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "stats":
            playerlist.append(entry[0])
    return playerlist

def listGolems():
    gamedata = os.listdir('../data/')
    golemlist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "golem":
            golemlist.append(entry[0])
    return golemlist

def listMines():
    gamedata = os.listdir('../data/')
    minelist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "mine":
            minelist.append(entry[0])
    return minelist

### gameplay functions

def newPlayer(channel, user):
    if os.path.isfile('../data/'+user+'.stats'):
        players.newDossier(user)
    else:
        players.newPlayer(user)

    #playerlist = open("../data/players.txt", 'a')
    #playerlist.write(user+"\n")
    #playerlist.close()
    global dossierList
    dossierList.append(user)

    ircsock.send("PRIVMSG "+channel+" :"+ user + ": New dossier created.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with '!open'.\n")

    return user

def newMine(channel, user, rates="standardrates"):
    mine = players.newMine(user, "standardrates").capitalize()
    players.decAvailableMines(user)
    ircsock.send("PRIVMSG "+ channel +" :"+ user + ": Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+mine+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts, and begin with an enthusiastic '!strike'.\n")

    return mine

def newGolem(channel, user, time, golemstring):
    if hasGolem(user):
        ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You can't make a new golem until your old golem finishes working!  It'll be ready in "+formatter.prettyTime(golems.getLifeRemaining(user, time))+".\n")
    else:
        if golems.calcStrength(golems.parse(golemstring)) > 0:
            if players.canAfford(user, golems.parse(golemstring)):
                golemfilter = list(golemstring)
                maxgolem = (players.getStrength(user)*3.5)
                if len(golemfilter) > maxgolem:
                  ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You're not strong enough to construct a golem that big, friend.  The most you can use is "+p.no("resource", maxgolem)+".\n")
                else:
                  golemshape = []
                  for x in golemfilter:
                      if x in ['~', '@', '#', '^', '&', '*', '[', ']']:
                          golemshape.append(x)

                  golem = golems.newGolem(user, ''.join(golemshape), time)
                  players.removeRes(user, golems.getStats(user))
                  ircsock.send("PRIVMSG "+ channel +" :"+ user + ": "+players.printExcavation(golems.getStats(user))+ " has been removed from your holdings.  Your new golem will last for "+formatter.prettyTime(golems.getLifeRemaining(user, time))+".  Once it expires, you can gather all the resources it harvested for you.\n")
                  logGolem(user)
            else:
                ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You don't have the resources to make that golem, friend.\n")
        else:
            ircsock.send("PRIVMSG "+ channel +" :"+ user + ": That's not a valid golem, friend.  The golem has to be constructed from resources you've acquired.\n")

def logGolem(user): 
  golemarchive = open("../data/golems.txt", 'a')
  golemtext = golems.getShape(user) + "\t"
  golemtext += str(golems.getStrength(user)) + "/" + str(golems.getInterval(user)) + "\t"
  golemtext += " ("+user+" on "+datetime.now().date().__str__()+")"
  golemarchive.write(golemtext+"\n")
  golemarchive.close()

def updateGolems(time):
    for x in listGolems():
        strikeDiff = int(time) - golems.getLastStrike(x)
        interval = golems.getInterval(x)

        if strikeDiff >= interval and len(players.getMines(x)) > 0: # golem strike
            target = players.getMines(x)[0]
            strikeCount = strikeDiff/interval
            i = 0
            elapsed = golems.getLastStrike(x)
            while i < strikeCount:
                if mines.getTotal(target) > 0:
                    print "golemstrike"+ str(golems.strike(x, target))
                elapsed += interval
                i += 1

            golems.updateLastStrike(x, elapsed)

        if int(time) > golems.getDeath(x): # golem death
            golem = golems.getShape(x)
            mined = players.printExcavation(golems.expire(x))
            golemgrave = "in front of you"
            if len(players.getMines(x)) > 0:
                golemgrave = "inside of "+players.getMines(x)[0].capitalize()

            ircsock.send("PRIVMSG "+ x +" :"+golem+" crumbles to dust "+golemgrave+" and leaves a wake of "+mined+"\n")

def strike(msg, channel, user, time):
    mineList = players.getMines(user)
    target = mineList[0] #autotarget first mine

    selected = msg.split(COMMANDS[3])[-1].split(" ")[-1] #check for targetted mine
    if selected != "":
        if mineList.count(selected) == 0:
            ircsock.send("PRIVMSG "+ user +" : That's not a mine you're working on, friend.\n")
            return

        if target != selected:
            target = selected
            mineList.remove(target)    #bump this to the top of the minelist
            mineList.insert(0, target)

    #diff = int(time)-int(players.getLastStrike(user))
    #if diff < baseFatigue: # fatigue check
    #    left =  baseFatigue - diff
    #    fatigue = left * 2
    #    time = int(time) + fatigue - baseFatigue

    fatigue = players.fatigueCheck(user, time)
    if fatigue > 0:
        fatigue = fatigue * 2
        time = int(time) + fatigue - (baseFatigue - players.getEndurance(user))# still hardcoded bs
        ircsock.send("PRIVMSG "+ user +" :You're still tired from your last attempt.  You'll be ready again in "+str(fatigue)+" seconds.  Please take breaks to prevent fatigue; rushing will only lengthen your recovery.\n")

    else: # actual mining actions
        emptyMines = []
        status = players.incStrikes(user)
        excavation = players.strike(user, target)
        mined = players.printExcavation(players.acquireRes(user, excavation))
        ircsock.send("PRIVMSG "+ user +" :\x03" + random.choice(['4', '8', '9', '11', '12', '13'])+random.choice(['WHAM! ', 'CRASH!', 'BANG! ', 'KLANG!', 'CLUNK!', 'PLINK!', 'DINK! '])+"\x03  "+status+"You struck at " + target.capitalize() +" and excavated "+mined+"\n")

        if mines.getTotal(target) == 0:
            emptyMines.append(target)
            players.incCleared(user)
            players.incEndurance(user)
            players.incAvailableMines(user)
            ircsock.send("PRIVMSG "+ user +" :As you clear the last of the rubble from "+target.capitalize()+", a mysterious wisp of smoke rises from the bottom.  You feel slightly rejuvinated when you breathe it in.\n")
            ircsock.send("PRIVMSG "+ user +" :"+target.capitalize()+" is now empty.  The empress shall be pleased with your progress.  I'll remove it from your dossier now; feel free to request a new mine.\n")
            ircsock.send("PRIVMSG "+config[1]+" :There's a distant rumbling as "+user+" clears the last few resources from "+target.capitalize()+".\n")

        for x in emptyMines:
            mineList.remove(x)

    players.updateOwned(user, mineList)
    players.updateLastStrike(user, time)

def report(msg, channel, user, time):
    if len(players.getMines(user)) > 0:
        ircsock.send("PRIVMSG "+ user +" :"+mineListFormatted(msg, channel, user)+"\n")
    ircsock.send("PRIVMSG "+ user +" :"+resourcesFormatted(channel, user)+"\n")
    if hasGolem(user):
        ircsock.send("PRIVMSG "+ user +" :"+golemStats(channel, user, time)+".\n")
    ircsock.send("PRIVMSG "+ user +" :"+statsFormatted(channel, user)+"\n")

def grovel(msg, channel, user, time):
    players.incGrovel(user)
    statement = '\x03' + random.choice(['4', '8', '9', '11', '12', '13']) + str(empress.speak()).rstrip()

    ircsock.send("PRIVMSG "+ channel + " :" + user +": The empress "+random.choice(['says', 'states', 'replies', 'snaps', 'mumbles', 'mutters'])+", \""+statement+"\x03\"  "+random.choice(INTERP_NEU)+"\n")

def stirke(msg, channel, user, time): #hazelnut memorial disfeature
    a = 0

def fatigue(msg, channel, user, time): #~krowbar memorial feature
    fatigue = players.fatigueCheck(user, time)
    if fatigue > 0:

        ircsock.send("PRIVMSG "+ channel + " :" + user +": You'll be ready to strike again in "+formatter.prettyTime(fatigue)+".  Please rest patiently so you do not stress your body.\n")
    else:
        ircsock.send("PRIVMSG "+ channel + " :" + user +": You're refreshed and ready to mine.  Take care to not overwork; a broken body is no use to the empress.\n")

def mineListFormatted(msg, channel, user):
    plural = ''
    if len(players.getMines(user)) > 0:
        plural = 's'

    prejoin = []

    mineList = players.getMines(user)
    rawlist = []
    for x in mineList:
        depletion = int(100*float(mines.getTotal(x))/float(mines.getStarting(x)))
        prefix = ''

        if mineList.index(x) == 0: # currently targetted
            prefix= '>'

        rawlist.append([prefix+x.capitalize(), depletion])

    rawlist.sort(key=lambda entry:int(entry[1]))

    for x in rawlist:
        depletion = x[1]

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

        prejoin.append(x[0] + " (" + color + str(depletion) + "%\x03)")

    return "You're working on the following mine"+plural+": "+j.join(prejoin)

def resourcesFormatted(channel, user):
    return "You're holding the following resources: "+players.heldFormatted(user)

def statsFormatted(channel, user):
    stats = "You can mine up to "+str(3*players.getStrength(user))+" units every strike, and strike every "+p.no("second", baseFatigue - players.getEndurance(user))+" without experiencing fatigue.  "
    plural = 's'
    if players.getClearedCount(user) == 1: plural = ''
    stats += "You've cleared "+str(players.getClearedCount(user))+" mine"+plural+".  "
    stats += "You can make a golem with up to "+p.no("resource", int(3.5*players.getStrength(user)))+".  "
    stats += "Please continue working hard for the empress!"

    return stats

def golemStats(channel, user, time):
    status = golems.getShape(user)+" is hard at work!  "
    status += "It can excavate up to "+p.no("resource", golems.getStrength(user))+" per strike, and strikes every "+p.no("second", golems.getInterval(user))+".  It'll last another "+formatter.prettyTime(golems.getLifeRemaining(user, time))

    return status

def rankings(msg, channel, user):
    dossiers = dossierList
    #playerlist = open("../data/players.txt", 'r')
    #for x in playerlist:
    #   dossiers.append(x.rstrip())
    #playerlist.close()

    records = []
    for x in dossiers:
        records.append([x, str(players.getHeldTotal(x))])

    records.sort(key=lambda entry:int(entry[1]), reverse=True)
    ircsock.send("PRIVMSG " + channel + " :The wealthiest citizens are:\n")

    for x in range (0, min(5, len(records))):
        entry = records[x]
        ircsock.send("PRIVMSG " + channel + " :" + entry[0] + " with " + entry[1] + " units\n")

###########################

def listen():
  lastcheck = int(systime.time())
  while 1:
    #####
    now = int(systime.time())
    if now - lastcheck > 0: #updates
        #print "tick: " + str(now - lastcheck)
        lastcheck = now
        updateGolems(now)
    #####
    #print "waiting " + str(now)
    msg = ircsock.recv(2048)
    #print msg

    if msg.find("PING") != -1: 
        ping()

    msg = msg.strip('\n\r').lower() #case insensitive
    formatted = formatter.format_message(msg)

    if "" == formatted:
          continue

    #if msg.find("PING :") != -1: ping()

    #else:
        #if msg.find("PING :") != -1: ping()
    if 1:

        nick = msg.split("!")[0].split(":")[1]

        split       = formatted.split("\t")
        time        = split[0]
        user        = split[1]
        command     = split[2]
        channel     = split[3] #if you include the :: we can do slicker PM
        messageText = split[4]

        #print channel
        #print msg
        #print formatted

        if nick != user: #check for weird identity stuff
            user = nick

        if channel == botName:  #check for PM
            channel = user

        #if channel == botName or msg.find(":!") != -1: #only log PM and commands
        #    logfile = open("irclog", 'a')
        #    logfile.write(msg+"\n")
        #    logfile.close()

        ###### admin commands
        if msg.find(":!join") != -1 and user == admin:
            split = msg.split(" ");
            for x in split:
                if x.find("#") != -1:
                    joinchan(x)

        elif msg.find(":!allplayers") != -1 and user == admin:
            ircsock.send("PRIVMSG "+channel+" :"+ user + ": "+j.join(listPlayers())+"\n")

        elif msg.find(":!alldossiers") != -1 and user == admin:
            ircsock.send("PRIVMSG "+channel+" :"+ user + ": "+j.join(listDossiers())+"\n")

        elif msg.find(":!allgolems") != -1 and user == admin:
            ircsock.send("PRIVMSG "+channel+" :"+ user + ": "+j.join(listGolems())+"\n")

        elif msg.find(":!allmines") != -1 and user == admin:
            ircsock.send("PRIVMSG "+channel+" :"+ user + ": "+j.join(listMines())+"\n")

        elif msg.find(":!forcenew") != -1:
            if user == admin:
                split = msg.split(" ");
                rates = ''
                for x in split:
                    if os.path.isfile(x):
                        rates = x
                for x in split:
                    if isPlaying(x):
                        if rates is not '':
                            newMine(msg, x, x, rates)
                        else:
                            newMine(msg, x, x)
            else:
                ircsock.send("PRIVMSG "+ channel +" :"+ user + ": Sorry, friend, but only "+admin+" can request new mines on behalf of others.\n")
        elif msg.find(":!brb") != -1:
          ircsock.send("QUIT\n")
          print "manual shutdown"
          break

        ###### gameplay commands
        elif msg.find(":!rollcall") != -1: # tildetown specific
            ircsock.send("PRIVMSG "+ channel +" :I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike {mine}, !report, !stats, !fatigue, !golem {resources}, !grovel, !rankings, !info.\n")

        elif msg.find(":!"+COMMANDS[7]) != -1: # !info
            ircsock.send("PRIVMSG "+ channel +" :"+ user + ": I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike {mine}, !report, !stats, !fatigue, !golem {resources}, !grovel, !rankings, !info.\n")

        elif msg.find(":!"+COMMANDS[0]) != -1: # !init
            if isPlaying(user):
                ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You already have a dossier in my records, friend.\n")
            else:
                newPlayer(channel, user)

        elif msg.find(":!"+COMMANDS[1]) != -1: # !open
            if isPlaying(user):
                if players.getAvailableMines(user) > 0:
                     newMine(channel, user)
                else:
                    ircsock.send("PRIVMSG "+ channel + " :" + user + ": You do not have permission to open a new mine at the moment, friend.  Perhaps in the future, the empress will allow you further ventures.\n")
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I can't open a mine for you until you have a dossier in my records, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[2]) != -1: # !mines
            if isPlaying(user):
                if len(players.getMines(user)) == 0:
                    ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
                else:
                    ircsock.send("PRIVMSG "+channel+" :" + user + ": "+mineListFormatted(msg, channel, user)+"\n")
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[9]) != -1: # !stats
            if isPlaying(user):
                ircsock.send("PRIVMSG "+channel+" :" + user + ": "+statsFormatted(channel, user)+"\n")
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[11]) != -1: # !res
            if isPlaying(user):
                ircsock.send("PRIVMSG "+channel+" :" + user + ": "+resourcesFormatted(channel, user)+"\n")
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[3]) != -1: # !strike
            if isPlaying(user):
                if len(players.getMines(user)) == 0:
                    ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
                else:
                    strike(msg, channel, user, time)
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[5]) != -1: # !fatigue
            if isPlaying(user):
                fatigue(msg, channel, user, time)
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[6]) != -1: # !grovel
            if isPlaying(user):
                #grovel(msg, channel, user, time)
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": The empress is indisposed at the moment.  Perhaps she will be open to receiving visitors in the future.  Until then, I'd encourage you to work hard and earn her pleasure.\n")
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I advise against groveling unless you're in my records, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[4]) != -1: # !report
            if isPlaying(user):
                report(msg, channel, user, time)
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[10]) != -1: # !golem
            if isPlaying(user):
                parse = msg.split("!"+COMMANDS[10])
                if parse[1] == '': #no arguments
                    if hasGolem(user):
                        ircsock.send("PRIVMSG "+ channel + " :" + user + ": "+golemStats(channel, user, time)+".\n")
                        ircsock.send("PRIVMSG "+ channel + " :" + user + ": It's holding the following resources: "+golems.heldFormatted(user)+".\n")
                        #ircsock.send("PRIVMSG "+ channel + " :" + user + ": "+golems.getShape(user)+" is hard at work!  It'll last for another "+p.no("second", golems.getLifeRemaining(user, time))+".\n")
                    else:
                        ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have a golem working for you, friend.  Create one with '!golem {resources}'.\n")
                else: # check for mines??
                    newGolem(channel, user, time, parse[1].lstrip())
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

        elif msg.find(":!"+COMMANDS[8]) != -1: # !rankings
            rankings(msg, channel, user)

#########################
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect(options.server, options.channel, options.nick)
listen()
