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
    "minecap":100,
    "residentcap": 10,
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
    while zoneID in ZONES:
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

    ZONES.update({zoneID:zonedata})
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
