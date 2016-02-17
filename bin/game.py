#!/usr/bin/python

import golems
import players
import mines
import world
import empress
import gibber
import util

from fuzzywuzzy import process
import inflect

from datetime import datetime
import json
import os
import random
import time as systime
import imp

p = inflect.engine()
j = ", "
baseFatigue = 10

RESOURCES = {}
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")

## file i/o

def init(playerfile=os.path.join(DATA,"playersautosave.json"), minefile=os.path.join(DATA,"mineautosave.json"), worldfile=os.path.join(DATA,"worldautosave.json")):
    # game init stuff

    imp.reload(players)
    imp.reload(world)
    imp.reload(mines)
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

    return mine.exists(minename)

def has_space(zoneID, target):
    # checks if zoneID has space

    return world.has_space(zoneID, target)

def name_mine(mineID):
    # returns name of mine

    return mines.get(mineID, "name")

def name_zone(zoneID):
    # returns name of zoneID

    return world.get(zoneID, "name")

def list_zones():
    # returns sorted list of zone names

    zonelist = world.list_names()

    return zonelist

def list_mines(playerID):
    # returns list of mine names

    rawlist = []

    for mineID in players.get(playerID, "mines owned"):
        prefix = ""
        depletion = None

        if mineID == players.get(playerID, "targetted"):
            prefix = ">"

        if players.get(playerID, "surveying"):
            depletion = int(100*float(mines.get(mineID, "current total"))/float(mines.get(mineID, "starting total")))

        rawlist.append([prefix+mines.get(mineID, "name"), depletion])

    if players.get(playerID, "surveying"):
        rawlist.sort(key = lambda mine:mine[1])

    minelist = []

    for mine in rawlist:
        postfix = ""

        if mine[1] is not None:   # True if depletion has been set
            postfix = " ("+str(mine[1])+"%)"

        minelist.append(mine[0]+postfix)

    return minelist

def targetted(playerID):
    # returns mineID that player has targetted

    return players.get(playerID, "targetted")

def fatigue_left(playerID, now):
    # returns fatigue left for playerID from passed in no

    return players.fatigue_left(playerID, now)

def may_strike(playerID, mineID):
    # returns True if player is permitted to strike at selected mine

    permitted = []
    permitted.extend(players.get(playerID, "mines owned"))
    permitted.extend(players.get(playerID, "mines assigned"))

    return mineID in permitted

def held_res(player):
    # returns dict of player's held res

    return players.get(player, "held res")

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
    match = process.extractOne(target, zones)[0]

    return world.exists(match)

## player actions

def strike(playerID, mineID, now):
    # step through strike checks
    # returns if player is fatigued, if player is permitted to strike, if mine is depleted, and res list

    permitted = False
    depleted = False
    reslist = None
    fatigue = 1

    if may_strike(playerID, mineID):
        permitted = True
        fatigue = players.fatigue_left(playerID, now)
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

## BRINGING SOME FORMATTING SHIT OVER

def heldFormatted(player):
    held = getHeld(player)

    return held[0]+ " tilde, "+held[1]+ " pound, "+held[2]+ " spiral, "+held[3]+ " amper, "+held[4]+ " splat, "+held[5]+ " lbrack, "+held[6]+ " rbrack, and "+held[7]+" carat, for a total of "+str(getHeldTotal(player))+" units"

############################# LINE OF DEATH ################

## meta functions

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
