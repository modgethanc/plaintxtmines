#!/usr/bin/python

import gibber
import util
import inflect

import json
import random
import os

DATA = os.path.join("..", "data")
ATS = "worldautosave.json"
CONFIG = os.path.join("config")
WORLD = {}
DEFAULTS = {
    "residents":[],
    "mines":[],
    "max mines":100,
    "max residents": 10,
    "rates": {
      "size":100,
      "tilde":40,
      "pound":20,
      "spiral":15,
      "amper":10,
      "splat":6,
      "lbrack":4,
      "rbrack":4,
      "carat":1 },
    "level":0
}

p = inflect.engine()

## file i/o

def load(worldfile=os.path.join(DATA,ATS)):
    # takes a json from worldfile and loads it into memory
    # returns number of zones loaded

    global WORLD

    infile = open(worldfile, "r")
    WORLD = json.load(infile)
    infile.close()

    return len(WORLD)

def save(savefile=os.path.join(DATA,ATS)):
    # save current WORLD to savefile, returns save location

    outfile = open(savefile, "w")
    outfile.write(json.dumps(WORLD, sort_keys=True, indent=2, separators=(',', ':')))
    outfile.close()

    return savefile

def new(init=DEFAULTS):
    # generates new zone entry from given inits, adds to memory, returns new zoneID

    zonedata = {}

    zoneID = util.genID(3)
    while zoneID in WORLD:
        zoneID = util.genID(3)

    zonename = gibber.medium().capitalize()
    while exists(zonename):
        zonename = gibber.medium()

    init.update({"name":zonename})

    for x in DEFAULTS:  # checking for required things
        if x not in init:
            init.update({x:DEFAULTS[x]})

    for x in init:
        zonedata.update({x:init[x]})

    WORLD.update({zoneID:zonedata})
    return zoneID

## world output

def data(zoneID):
    # takes str zoneID and returns zone data, or none

    if zoneID in WORLD:
        return {zoneID:WORLD[zoneID]}
    else:
        return None

def get(zoneID, field):
    # takes str zoneID and field and returns whatever it is
    # returns None if zone or field doesn't exist

    if zoneID in WORLD:
        return WORLD[zoneID].get(field)
    else:
        return None

def find(searchdict):
    # returns a list of str IDs that match search dict

    matches = []

    for x in WORLD:
        found = True
        zone = WORLD[x]

        for y in searchdict:
            if zone.get(y) == searchdict.get(y):
                found = True
            else:
                found = False
                break

        if found:
            matches.append(x)

    return matches

def exists(zonename):
    # check to see if zonename exists

    for x in WORLD:
        if WORLD[x].get("name") == zonename:
            return True

    return False

def has_space(zoneID, target):
    # check to see if named zoneID can take one more of named target
    # target should be an array, with "max {target}" as the limit

    if get(zoneID, "max "+target) > len(get(zoneID, target)):
        return True
    else:
        return False

## world actions

def update(zoneID, updateDict):
    # updates the stuff in updateDict for a given zone

    zone = data(zoneID)

    for x in updateDict:
        #print(x)
        zone[zoneID].update({x:updateDict[x]})
        #print(player)

    return zoneID

def inc(zoneID, field):
    # increases an integer counter named field, returns new value

    value = get(zoneID, field)

    if value is not None:
        value += 1
        update(zoneID, {field:value})

    return value

def dec(zoneID, field):
    # decreases an integer counter named field, returns new value

    value = get(zoneID, field)

    if value > 0:
        value -= 1
        update(zoneID, {field:value})

    return value
