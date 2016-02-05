#!/usr/bin/python

import golems
import players
import mines
import empress
import gibber
import util

import inflect
import formatter

from datetime import datetime
import json
import os
import random
import time as systime

p = inflect.engine()
j = ", "
baseFatigue = 10

RESOURCES = {}
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")

## file i/o 

def init(playerfile=os.path.join(DATA,"playersautosave.json"), minefile=os.path.join(DATA,"mineautosave.json"), worldfile=""):
    # game init stuff

    players.load(playerfile)
    mines.load(minefile)
    #util.pretty_dict(players.PLAYERS)
    #util.pretty_dict(mines.MINES)

def load_res(resfile=os.path.join(CONFIG, "resources.json")):
    # takes a json from resfile and loads into memory
    # returns number of different kinds of res

    global RESOURES

    infile = open(resfile, "r")
    RESOURCES = json.load(infile)
    infile.close()

    return len(RESOURCES)

def load_rate(ratefile=os.path.join(CONFIG, "baserate.json")):
    # takes a json from ratefile and returns dict of it

    infile = open(ratefile, "r")
    rates = json.load(infile)
    infile.close()

    return rates

## object creation

def new_player(init):
    # creates a new player with passed in defaults

    newID = players.new(init)

    return newID

def new_mine(playerID, zoneID="", minerate=load_rate()):
    # creates a new mine belonging to given playerID in area zoneID with either given minerate, or default
    # does all the proper linking

    newID = mines.new(playerID, zoneID, minerate)
    players.get(playerID, "mines owned").append(newID)

    return newID

## player actions

def strike(playerID, mineID):
    # does all the striking actions:
    # check if player has permission to strike at mine
    # check for fatigue
    # strike at mine
    # remove res from mine, add to player
    # returns ???

    return

## meta helpes

def can_strike(playerID, mineID):
    # returns True if player is permitted to strike

    return True

## NEW STUFF ENDS HERE

def incStrikes(player): # increment strike count
    ## TODO brought this over from players to save it

    status = '' #level up message

    playerdata = openStats(player)
    playerdata[4] = str(int(playerdata[4]) + 1)

    x = int(playerdata[2])
    if random.randrange(0,99) < 20/x: # scaling level up
        playerdata[2] = str(x+1)
        status = "You're feeling strong!  "

    writeStats(player, playerdata)

    return status

## BRINGING SOME FORMATTING SHIT OVER

def printExcavation(excavation):
    total = 0

    for x in excavation:
        total += int(x)

    if total == 0:
        return "nothing but rubble."

    if total > 100:
        return "a lot of resources!"

    mined = ''
    y = 0
    for x in excavation:
        if y == 0: item = '~'
        elif y == 1: item = '#'
        elif y == 2: item = '@'
        elif y == 3: item = '&'
        elif y == 4: item = '*'
        elif y == 5: item = '['
        elif y == 6: item = ']'
        elif y == 7: item = '^'

        i = 0
        while i < int(x):
            mined += item
            i += 1

        y += 1

    return mined

def heldFormatted(player):
    held = getHeld(player)

    return held[0]+ " tilde, "+held[1]+ " pound, "+held[2]+ " spiral, "+held[3]+ " amper, "+held[4]+ " splat, "+held[5]+ " lbrack, "+held[6]+ " rbrack, and "+held[7]+" carat, for a total of "+str(getHeldTotal(player))+" units"

## END FORMAT IMPORT

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
    stats = "You can mine up to "+str(3*players.getStrength(user))+" units every strike, and strike every "+p.no("second", baseFatigue - min(9, players.getEndurance(user)))+" without experiencing fatigue.  "
    plural = 's'
    if players.getClearedCount(user) == 1: plural = ''
    stats += "You've cleared "+str(players.getClearedCount(user))+" mine"+plural+".  "
    stats += "You can make a golem with up to "+p.no("resource", int(3.5*players.getStrength(user)))+".  "
    stats += "Please continue working hard for the empress!"

    return stats

def golemStats(channel, user, time):
    status = golems.getShape(user)+" is hard at work!  "
    status += "It can excavate up to "+p.no("resource", golems.getStrength(user))+" per strike, and strikes every "+p.no("second", golems.getInterval(user)) + ".  "
    status += "It's been going for "+util.pretty_time(golems.getLife(user, time))+"."

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

#### MOVING IRC BOT STUFF HERE

# status checking

def isPlaying(user):
    return os.path.isfile('../data/'+user+'.dossier')

def isMine(mine):
    return os.path.isfile('../data/'+mine+'.mine')

def hasGolem(user):
    return os.path.isfile('../data/'+user+'.golem')
