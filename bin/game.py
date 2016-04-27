#!/usr/bin/python
import golems
import players
import mines
import world
import empress
import gibber
import util
import htmlout

#from fuzzywuzzy import process
import inflect

from datetime import datetime
import json
import sys
import os
import random
import time as systime
import imp

p = inflect.engine()

RESOURCES = {}
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")
IRC_COLORS = False

## file i/o

def init(playerfile=os.path.join(DATA,"playersautosave.json"), minefile=os.path.join(DATA,"mineautosave.json"), worldfile=os.path.join(DATA,"worldautosave.json")):
    # game init stuff

    imp.reload(players)
    imp.reload(world)
    imp.reload(mines)
    imp.reload(htmlout)
    load_res()

    print("players: "+str(players.load(playerfile)))
    print("mines: "+str(mines.load(minefile)))
    print("zones: " +str(world.load(worldfile)))

def load_res(resfile=os.path.join(CONFIG, "resources.json")):
    # takes a json from resfile and loads into memory
    # returns number of different kinds of res

    global RESOURCES

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

def save():
    # call save on everything

    mines.save()
    players.save()
    world.save()

    htmlout.write("world.html")

## object creation

def new_player(init):
    # creates a new player with passed in defaults
    # returns new player's ID

    newID = None
    hasSpace = False
    localID = init.get("home")
    nick = init.get("nick")

    if localID:
        init.update({"location":localID})
        if has_space(localID, "residents"):
            hasSpace = True

    if nick:
        init.update({"aliases":[nick]})

    if hasSpace:
        newID = players.new(init)
        world.get(localID, "residents").append(newID)

    return newID, hasSpace, localID

def new_mine(playerID, customRate=False):
    # checks if a new mine can be created

    newID = None
    hasSpace = False
    mayCreate = False
    localID = players.get(playerID, "location")

    if players.get(playerID, "mines available") > 0:
        mayCreate = True

    hasSpace = world.has_space(localID, "mines")

    if hasSpace and mayCreate:
        newID = successful_open(playerID, customRate)

    return newID, hasSpace, mayCreate

def new_zone(init):
    # creates a new zone with passed in defaults

    newID = world.new(init)

    return newID

## game state querying

def is_playing(nick):
    # checks for nick in playerdata
    # returns playerID if listed

    return players.registered(nick)

def is_zone(province):
    # checks for named province in world data
    # returns  zoneID if listed

    return world.exists(province)

def is_mine(minename):
    # checks for named mine in mine data
    # returrns mineID if listed

    return mines.exists(minename)

def has_space(zoneID, target):
    # checks if zoneID has space

    return world.has_space(zoneID, target)

def get_data(datatype, dataID, field):
    # calls specific get function for named data time
    # returns value of field
    # valid datatypes: players, world, mines

    dataget = getattr(getattr(sys.modules[__name__], datatype), "get")

    return dataget(dataID, field)

def list_zones():
    # returns sorted list of zone names

    zonelist = world.list_names()

    return zonelist

def list_players():
    # returns list of player names

    playerlist = players.list_names()

    return playerlist

def list_mines(playerID):
    # returns list of mine names assigned to given playerID

    rawlist = []

    showPercent = "foresight" in players.get(playerID, "favors")

    for mineID in players.get(playerID, "mines owned"):
        prefix = ""
        depletion = None

        if mineID == players.get(playerID, "targetted"):
            prefix = ">"

        if showPercent:
            depletion = int(100*float(mines.get(mineID, "current total"))/float(mines.get(mineID, "starting total")))

        rawlist.append([prefix+mines.get(mineID, "name"), depletion])

    if showPercent:
        rawlist.sort(key = lambda mine:mine[1])

    return rawlist

def fatigue_left(playerID, now):
    # returns fatigue left for playerID from passed in no

    return players.fatigue_left(playerID, now)

def may_strike(playerID, mineID):
    # returns True if player is permitted to strike at selected mine

    permitted = []
    permitted.extend(players.get(playerID, "mines owned"))
    permitted.extend(players.get(playerID, "mines assigned"))

    return mineID in permitted

def player_fatiguerate(playerID):
    # return fatigue seconds

    return players.fatigue_shift(playerID)

def player_strikerate(playerID):
    # return player strikerate

    return players.strikerate(playerID)

def player_home(playerID):
    # return name of player's home province

    zoneID = players.get(playerID, "home")

    return world.get(zoneID, "name")

###

def print_reslist(reslist):
    # processes a dict reslist into human-readable

    resprint = ""

    for res in reslist:
        glyph = RESOURCES.get(res).get("glyph")
        count = reslist.get(res)
        i = 0
        while i < count:
            resprint += glyph
            i += 1

    return resprint

def match_province(target):
    # takes entered string and picks closest matching zone name
    # returns zoneID

    zones = world.list_names()
    #match = process.extractOne(target, zones)[0]

    #return world.exists(match)
    return world.exists(target)

## player actions

def strike(playerID, mineID, now):
    # step through strike checks
    # returns if player is fatigued, if player is permitted to strike, if mine is depleted, and res list

    permitted = False
    depleted = False
    reslist = None
    fatigue = 1
    lvlUp = False

    fatigue = players.fatigue_left(playerID, now)

    if may_strike(playerID, mineID):
        permitted = True
        #fatigue = players.fatigue_left(playerID, now)
        if fatigue > 0:
            fatigue = players.double_fatigue(playerID, now)

    if not fatigue and permitted:
        reslist, lvlUp  = successful_strike(playerID, mineID, now)

    if mines.get(mineID, "status") == "depleted":
        mine_depleted(playerID, mineID)
        depleted = True

    return fatigue, permitted, depleted, reslist, lvlUp

def move(playerID, newzoneID):
    # checks if playerID can move to newzoneID and calls move if possible
    # returns boolean moved (True if move happened), hasSpace (True if
    # new zone has space), and mayMove (True if player has move
    # permission)

    moved = False
    hasSpace = False
    mayMove = False

    if newzoneID in world.WORLD:
        hasSpace = world.has_space(newzoneID, "residents")
        if 1:  # placeholder check for player move permission
            mayMove = True

    if hasSpace and mayMove:
        successful_move(playerID, newzoneID)
        moved = True

    return moved, hasSpace, mayMove

def alias(playerID, newAlias):
    # adds new alias to playerID

    aliases = []

    if not is_playing(newAlias):
        players.get(playerID, "aliases").append(newAlias)
        aliases = players.get(playerID, "aliases")

    return aliases

## meta helpers

def mine_depleted(playerID, mineID):
    # increase player endurance and mines available
    # move mine to completed

    players.inc(playerID, "mines available")
    players.inc(playerID, "end")
    players.get(playerID, "mines completed").append(mineID)

    return

def successful_open(playerID, customRate=False):
    # opens a new mine for playerID
    # updates worldfile, playerfile, and minefile
    # pulls standard rate for that zone, or custom rate if player has a boost
    # returns ID of new mine

    localID = players.get(playerID, "location")

    if customRate:
        minerate = customRate
    else:
        minerate = world.get(localID, "rates")

    newID = mines.new(playerID, localID, minerate)
    world.get(localID, "mines").append(newID)

    players.dec(playerID, "mines available")
    players.get(playerID, "mines owned").append(newID)

    players.update(playerID, {"targetted":newID})

    return newID

def successful_move(playerID, newzoneID):
    # moves playerID to named newzone
    # updates worldfile and playerfile

    localID = player.get("playerID", "location")

    world.get(localID, "residents").remove(playerID)
    player.update({"location":newzoneID})
    world.get(newzoneID, "residents").append(playerID)

def successful_strike(playerID, mineID, now):
    # takes players's strikerate, applies to mine, adds excavation to player's held

    strike = players.strikerate(playerID)
    reslist = mines.excavate(mineID, strike[0], strike[1])
    players.add_res(playerID, reslist)
    players.update(playerID, {"last strike":now})
    players.inc(playerID, "strikes")

    return reslist, strength_roll(playerID)

def strength_roll(playerID):
    # rolls for an increase in strength

    strength  = players.get(playerID, "str")

    if random.randrange(0,99) < 20/strength: # scaling level up
        players.inc(playerID, "str")
        return True
    else:
        return False

############################# LINE OF DEATH ################

## meta functions

def logGolem(user):
  golemarchive = open("../data/golems.txt", 'a')
  golemtext = golems.getShape(user) + "\t"
  golemtext += str(golems.getStrength(user)) + "/" + str(golems.getInterval(user)) + "\t"
  golemtext += " ("+user+" on "+datetime.now().date().__str__()+")"
  golemarchive.write(golemtext+"\n")
  golemarchive.close()
