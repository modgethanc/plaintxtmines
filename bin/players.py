#!/usr/bin/python

import mines
import gibber
import util
from util import sum_res

import inflect
import json
import os
import random
import time

DATA = os.path.join("..", "data")
ATS = "playersautosave.json"
CONFIG = os.path.join("config")
PLAYERS = {}
DEFAULTS = {
    "joined":0,
    "last seen":0,
    "mines owned":[],
    "mines assigned":[],
    "mines available":1,
    "stats":{
      "str":1,
      "end":0,
      "strikes":0
    },
    "favor level":0,
    "held res":{},
    "held total":0,
    "tithed res":{},
    "tithed total":0,
    "last strike":0,
    "inventory":[]
  }

BASEFAATIGUE = 10

p = inflect.engine()

## file i/o

def load_players(playerfile=os.path.join(DATA, ATS)):
    # takes a json from playerfile and loads it into memory
    # returns number of players loaded

    global PLAYERS

    infile = open(playerfile, "r")
    PLAYERS = json.load(infile)
    infile.close()

    return len(PLAYERS)

def save(savefile=os.path.join(DATA, ATS)):
    # save current MINES to savefile, returns save location

    outfile = open(savefile, "w")
    outfile.write(json.dumps(PLAYERS, sort_keys=True, indent=2, separators=(',', ':')))
    outfile.close()

    return savefile

def new_player(init = DEFAULTS):
    # generates new player entry from given

    playerdata = {}

    playerID = util.genID(5)
    while playerID in PLAYERS:
        playerID = util.genID(5)

    for x in DEFAULTS:  # checking for required things
        if x not in init:
            init.update({x:DEFAULTS[x]})

    for x in init:
        playerdata.update({x:init[x]})

    return {playerID:playerdata}

## player output

def data(playerID):
    # takes str playerID and returns player data, or none

    if playerID in PLAYERS:
        return {playerID:PLAYERS[playerID]}
    else:
        return None

def get(playerID, field):
    # takes str mineID and field and returns whatever it is
    # returns None if player or field doesn't exist

    if playerID in PLAYERS:
        return PLAYERS[playerID].get(field)
    else:
        return None

def stat(playerID, stat):
    # takes str playerID and stat and returns dict of stats

    if playerID in PLAYERS:
        return PLAYERS[playerID].get("stats").get(stat)
    else:
        return None

def find(searchdict):
    # returns a list of str IDs that match search dict

    matches = []

    for x in PLAYERS:
        found = True
        player = PLAYERS[x]

        for y in searchdict:
            if player.get(y) == searchdict.get(y):
                found = True
            else:
                found = False
                break

        if found:
            matches.append(x)

    return matches

def registered(playername):
    # check to see if playername shows up in any alias list
    # returns either False or some playerID that triggers true

    for x in PLAYERS:
        if playername in get(x, "aliases"):
            return x

    return False

## meta helpers

def fatigue_left(playerID, time):
    # returns seconds untiil fatigue depletes after given time

    return (BASEFATIGUE - min(BASEFATIGUE - 1, stat(playerID, "end"))) - int(time) - get(playerID, "last strike")

##### LINE OF DEATH

## player actions

def update(playerID, updateDict):
    # updates the stuff in updateDict for a given player

    player = data(playerID)

    for x in updateDict:
        player.update({x:updateDict[x]})

    return playerID

def remove_res(playerID, res):
    # for given dict res, removes those from playerID held
    # returns player's held res, or False if player does not
    # have enough of any res

    held = get(playerID, "held res")

    for x in res:
        resValue = held.get(x)
        if not resValue:
            return False
        elif resValue < res.get(x):
            return False
        else:
            held[x] -= res.get(x)
   
    update(playerID, {"held total":sum_res(held)})

    return held

def incAvailableMines(player): # increase mine permission
    statlist = getEmpressStats(player)
    statlist[0] = str(int(statlist[0]) + 1)
    updateEmpressStats(player, statlist)

    return int(statlist[0])

def decAvailableMines(player): # decrease mine permission
    statlist = getEmpressStats(player)
    statlist[0] = str(int(statlist[0]) - 1)
    updateEmpressStats(player, statlist)

    return int(statlist[0])

def incTithe(player): # increase tithe count
    statlist = getEmpressStats(player)
    statlist[2] = str(int(statlist[2]) + 1)
    updateEmpressStats(player, statlist)

    return int(statlist[2])

def incFavor(player): # increase favor level
    statlist = getEmpressStats(player)
    statlist[3] = str(int(statlist[3]) + 1)
    updateEmpressStats(player, statlist)

    return int(statlist[3])

def decFavor(player): # decrease favor level
    statlist = getEmpressStats(player)
    statlist[3] = str(int(statlist[3]) - 1)
    updateEmpressStats(player, statlist)

    return int(statlist[3])

### stats updating

def writeStats(player, playerdata):
    playerfile = open('../data/'+player+'.stats', 'w')
    for x in playerdata:
        playerfile.write(str(x) + "\n")
    playerfile.close()

def updateLastStrike(player, time):
    playerdata = openStats(player)
    playerdata[0] = str(time)
    writeStats(player, playerdata)

    return time

def incStrength(player): # increment strength
    playerdata = openStats(player)
    playerdata[2] = str(int(playerdata[2]) + 1)
    writeStats(player, playerdata)

    return playerdata[2]

def incEndurance(player): # increment endurance
    playerdata = openStats(player)
    playerdata[3] = str(int(playerdata[3]) + 1)
    writeStats(player, playerdata)

    return playerdata[3]

def incStrikes(player): # increment strike count
    status = '' #level up message

    playerdata = openStats(player)
    playerdata[4] = str(int(playerdata[4]) + 1)

    x = int(playerdata[2])
    if random.randrange(0,99) < 20/x: # scaling level up
        playerdata[2] = str(x+1)
        status = "You're feeling strong!  "

    writeStats(player, playerdata)

    return status

def incCleared(player): # increment cleared count
    playerdata = openStats(player)
    playerdata[5] = str(int(playerdata[5]) + 1)
    writeStats(player, playerdata)

    return int(playerdata[5])

#### mine wrangling

def newMine(player, rates):
    minename = mines.newMine(player, rates)

    currentMines = getOwned(player)
    currentMines.append(minename)

    updateOwned(player, currentMines)

    return minename

def getMines(player):
    minelist = getOwned(player)

    for x in getContracted(player):
        minelist.append(x)

    return minelist

def strike(player, mine): # performs mining action
    baseDepth = 3
    strikeDepth = baseDepth * getStrength(player)

    return mines.excavate(mine, strikeDepth)

def acquireRes(player, excavation): # adds res to held
    held = getHeld(player)
    res = int(getTotalMined(player))

    i = 0
    for x in excavation:
        r = int(held[i]) + int(x)
        res += int(x)
        held[i] = str(r)
        i += 1

    playerdata = openDossier(player)
    playerdata[2] = j.join(held)
    playerdata[3] = res

    writeDossier(player, playerdata)

    return excavation

def canAfford(player, cost): # checks list of res against held
    held = getHeld(player)
    i = 0
    while i < 8:
        if int(held[i]) < int(cost[i]):
            return False
        i += 1

    return True

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

#################

def test():
    load_players()
    PLAYERS.update(new_player())

