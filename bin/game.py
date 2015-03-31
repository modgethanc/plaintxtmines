#!/usr/bin/python
import formatter
import random
import golems
import players
import mines
import empress
import gibber
import inflect
from datetime import datetime
import os
import os.path
import time as systime

p = inflect.engine()
j = ", "
baseFatigue = 10

## meta functions

def listDossiers():
    gamedata = os.listdir('../data/')
    playerlist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "dossier":
            playerlist.append(entry[0])
    return playerlist

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
            minelist.append(entry[0].capitalize())
    return minelist

def logGolem(user): 
  golemarchive = open("../data/golems.txt", 'a')
  golemtext = golems.getShape(user) + "\t"
  golemtext += str(golems.getStrength(user)) + "/" + str(golems.getInterval(user)) + "\t"
  golemtext += " ("+user+" on "+datetime.now().date().__str__()+")"
  golemarchive.write(golemtext+"\n")
  golemarchive.close()

## output formatting

def itemizeRes(resources): # takes list of res and outputs as human-readable
    total = 0
    output = []
    i = 0
    item = ""
    for res in resources:
        x = int(res)
        total += x
        if i == 0: item = "tilde"
        elif i == 1: item = "pound"
        elif i == 2: item = "spiral"
        elif i == 3: item = "amper"
        elif i == 4: item = "splat"
        elif i == 5: item = "lbrack"
        elif i == 6: item = "rbrack"
        elif i == 7: item = "carat"

        if x > 0:
          output.append(p.no(item, x))

        i += 1

    if total > 0:
      output.append("for a total of "+p.no("unit", total))
    else:
      output.append("nothing useful")

    return ", ".join(output)
    #return str(resources[0])+" tilde, "+str(resources[1])+" pound, "+str(resources[2])+" spiral, "+str(resources[3])+" amper, "+str(resources[4])+" splat, "+str(resources[5])+" lbrack, "+str(resources[6])+" rbrack, and "+str(resources[7])+" carat, for a total of "+str(total)+" units"

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
    status += "It can excavate up to "+p.no("resource", golems.getStrength(user))+" per strike, and strikes every "+p.no("second", golems.getInterval(user)) + ".  "
    status += "It's been going for "+formatter.prettyTime(golems.getLife(user, time))+"."

    return status

def resourcesFormatted(channel, user):
    return "You're holding the following resources: "+itemizeRes(players.getHeld(user))

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

#### status updating

