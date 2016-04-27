#!/usr/bin/python

import mines
import gibber
import util

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
    "mines completed":[],
    "mines available":1,
    "str":1,
    "end":0,
    "strikes":0,
    "favor level":0,
    "favors":[],
    "held res":{},
    "held total":0,
    "tithed res":{},
    "tithed total":0,
    "historic res":{},
    "historic total":0,
    "last strike":0,
    "inventory":[]
  }

BASEFATIGUE = 10  # starting seconds of fatigue
BASESTRIKE = 3    # strike depth multiplier

p = inflect.engine()

## file i/o

def load(playerfile=os.path.join(DATA, ATS)):
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

def new(init=DEFAULTS):
    # generates new player entry from given inits, adds to memory, returns new playerID

    playerdata = {}

    playerID = util.genID(5)
    while playerID in PLAYERS:
        playerID = util.genID(5)

    for x in DEFAULTS:  # checking for required things
        if x not in init:
            init.update({x:DEFAULTS[x]})

    for x in init:
        playerdata.update({x:init[x]})

    PLAYERS.update({playerID:playerdata})
    return playerID

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

def fatigue_left(playerID, now):
    # returns seconds untiil fatigue depletes after given time

    #return (BASEFATIGUE - min(BASEFATIGUE - 1, get(playerID, "end"))) - int(time) - get(playerID, "last strike")
    return max(0, fatigue_shift(playerID) - now + get(playerID, "last strike"))

def fatigue_shift(playerID):
    # returns modified fatigue, calculated from base fatigue and player endurance

    return BASEFATIGUE - min(9, get(playerID, "end"))

def strikerate(playerID):
    # calculates strike depth and width for playerID and does and returns that as a tuple

    depth = BASESTRIKE * get(playerID, "str")

    tool = get(playerID, "equipped")
    if tool:
        # TODO calculate strike width
        width = 1
    else:
        width = 1

    return (depth, width)

def can_afford(playerID, resllist):
    # checks list of res against held and returns True if player can afford it

    held = get(playerID, "held res")

    for x in reslist:
        current = held.get(x)
        if not current:
            return False
        elif reslist.get(x) > current:
            return False

    return True

## player actions

def update(playerID, updateDict):
    # updates the stuff in updateDict for a given player

    player = data(playerID)

    for x in updateDict:
        #print(x)
        player[playerID].update({x:updateDict[x]})
        #print(player)

    return playerID

def inc(playerID, field):
    # increases an integer counter named field, returns new value

    value = get(playerID, field)

    if value is not None:
        value += 1
        update(playerID, {field:value})

    return value

def dec(playerID, field):
    # decreases an integer counter named field, returns new value

    value = get(playerID, field)

    if value > 0:
        value -= 1
        update(playerID, {field:value})

    return value

def add_res(playerID, reslist):
    # for given dict reslist, add to player's held and historical

    held = get(playerID, "held res")
    history = get(playerID, "historic res")

    if not history:  # for backwards compatibility
        update(playerID, {"historic res":{}})
        update(playerID, {"historic total":0})
        history = get(playerID, "historic res")

    for res in reslist:
        current = held.get(res)
        historic = history.get(res)
        if current:
            current += reslist.get(res)
        else:
            current = reslist.get(res)
        if historic:
            historic += reslist.get(res)
            history.update({res:historic})
        else:
            history.update({res:reslist.get(res)})
        held.update({res:current})

    update(playerID, {"held total":util.sum_res(held)})
    update(playerID, {"historic total":util.sum_res(history)})

    return held

def remove_res(playerID, reslist):
    # for given dict reslist, removes those from playerID held
    # returns player's held reslist, or False if player does not
    # have enough of any res

    held = get(playerID, "held res")

    for x in reslist:
        resValue = held.get(x)
        if not resValue:
            return False
        elif resValue < reslist.get(x):
            return False
        else:
            held[x] -= reslist.get(x)

    update(playerID, {"held total":util.sum_reslist(held)})

    return held

def double_fatigue(playerID, now):
    # modifies strike time to double the fatigue from specified now
    # returns new fatigue left in seconds

    fatigue = fatigue_left(playerID, now) * 2
    newLast = fatigue - fatigue_shift(playerID) + now

    update(playerID, {"last strike":newLast})

    return fatigue

#################

def test():
    load()
    util.pretty(PLAYERS)
    #PLAYERS.update(new())
