#!/usr/bin/python

import golems
import players
import mines
import world
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

    print("players: "+str(players.load(playerfile)))
    print("mines: "+str(mines.load(minefile)))
    print("zones: " +str(world.load(worldfile)))

    #players.load(playerfile)
    #mines.load(minefile)
    #world.load(worldfile)

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

def save():
    # call save on everything

    mines.save()
    players.save()
    world.save()

## object creation

def new_player(init):
    # creates a new player with passed in defaults

    newID = None
    hasSpace = False
    localID = init.get("home")

    if localID:
        init.update({"location":init.get("home")})
        hasSpace = world.has_space(localID, "residents")

    if hasSpace:
        newID = players.new(init)
        world.get(localID, "residents").append(newID)

    return newID

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

    return newID

def new_zone(init):
    # creates a new zone with passed in defaults

    newID = world.new(init)

    return newID

## player actions

def strike(playerID, mineID, now):
    # step through strike checks
    # TODO: figure out what this should return at each condition

    if may_strike(playerID, mineID):
        if players.fatigue_left(playerID, now) <= 0:
            successful_strike(playerID, mineID, now)

            if mines.get(mineID, "status") == "depleted":
                mine_depleted(playerID, mineID)
        else: # increase fatigue
            return
    else:  # not permitted to strike
        return

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

## meta helpers

def mine_depleted(playerID, mineID):
    # TODO: give player end boost

    return

def successful_open(playerID, customRate=False):
    # opens a new mine for playerID
    # updates worldfile, playerfile, and minefile
    # pulls standard rate for that zone, or custom rate if player has a boost
    # returns ID of new mine

    localID = players.get(playerID, "location")

    if customeRate:
        minerate = customeRate
    else:
        minerate = world.get(localID, "rates")

    newID = mines.new(playerID, localID, minerate)
    world.get(localID, "mines").append(newID)

    players.dec(playerID, "mines available")
    players.get(playerID, "mines owned").append(newID)

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

    strength_roll(playerID)

def strength_roll(playerID):
    # rolls for an increase in strength

    strength  = players.get(playerID, "str")

    if random.randrange(0,99) < 20/strength: # scaling level up
        players.inc(playerID, "str")
        # "You're feeling strong!"
        return True
    else:
        return False

def may_strike(playerID, mineID):
    # returns True if player is permitted to strike

    permitted = []
    permitted.extend(players.get(playerID, "mines owned"))
    permitted.extend(players.get(playerID, "mines assigned"))

    return mineID in permitted

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
