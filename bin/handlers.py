#!/usr/bin/python

import inflect
import os
import json

import game

p = inflect.engine()
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")
CMD_DEF = "commands.json"
COMMANDS = {}
LANG = {}
STRANGER = "I don't know who you are, stranger.  If you'd like to enlist your talents in the name of the empress, you may do so with \"!join PROVINCE\"."

## file i/o

def load_cmd(commandfile=os.path.join(CONFIG, CMD_DEF)):
    # takes a commandfile and loads into memory

    global COMMANDS

    infile = open(commandfile, "r")
    COMMANDS = json.load(infile)
    infile.close()

def list():
    # returns a list of all loaded commands

    return [command for command in iter(COMMANDS)]

## base handler functions

def join(playerID, user, now, inputs):
    # creates a new player

    response = []

    if playerID:
        response.append("You are already registered, my friend.")
    else:
        if len(inputs) < 2:
            response.append("You must declare a province to which you call home, stranger.  "+provinces())
        else:
            zoneID = game.is_zone(inputs[1])
            newID, hasSpace, zoneExists = game.new_player(make_player(user, now, zoneID))
            if newID:
                print("new player: "+newID)
                response.append("Your citizenship is now acknowledged.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with \"!new\".")
            else:
                response.append(failed_join(hasSpace, zoneExists))

    return response

def new(playerID, user, time, inputs):
    # new mine creation
    print("creating new mine for "+user)

    response = []

    mineID, hasSpace, mayCreate = game.new_mine(playerID)

    if mineID:
        minename = game.name_mine(mineID)
        response.append("Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+minename+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts, and begin with an enthusiastic \'!strike\".")
    else:
        response.append(failed_new(hasSpace, mayCreate))

    return response

def grovel(playerID, user, time, inputs):

    response = []

    return response

def mines(playerID, user, time, inputs):

    response = []

    minelist = game.list_mines(playerID)

    msg = "You own the following "+p.plural("mines", len(minelist))+": "
    msg += ", ".join(minelist)

    return response

def info(playerID, user, time, inputs):

    response = []

    return response

def stats(playerID, user, time, inputs):

    response = []

    return response

def fatigue(playerID, user, time, inputs):

    response = []

    return response

def report(playerID, user, time, inputs):

    response = []

    return response

def strike(playerID, user, now, inputs):

    response = []

    if len(inputs) < 2:
        targetted = game.targetted(playerID)
    else:
        targetted = game.is_mine(inputs[1])
        if not targetted:
            targetted = game.targetted(playerID)

    fatigue, permitted, depleted, reslist = game.strike(playerID, targetted, now)

    if reslist:
        response.append("strike successful: " + game.print_reslist(reslist))
        if depleted:
            response.append(" mine depleted")
    else:
        response.append(strike_failure(fatigue, permitted))

    return response

def rankings(playeID, user, time, inputs):

    response = []

    return response

def golem(playerID, user, time, inputs):

    response = []

    return response

def res(playerID, user, time, inputs):

    response = []

    return response


## helper functions

def make_player(user, now, zoneID):
    # creates new inits for a player

    playerdata = {}
    playerdata.update({"nick":user})
    playerdata.update({"home":zoneID})
    playerdata.update({"joined":now})

    return playerdata

def failed_join(hasSpace, zoneExists):
    # processes join failure

    if not zoneExists:
        return "I've never heard of that province, stranger.  "+provinces()

    if not hasSpace:
        return "I'm sorry, friend, but that province cannot support any additional residents.  Please choose a different one in order to prevent overcrowding."

def provinces():
    # returns list of provinces

    zones = game.list_zones()

    msg = "The following "+p.plural("provinces", len(zones))+" fall under the empress's rule: "
    msg += ", ".join(zones)
    msg += "."

    return msg

def failed_new(hasSpace, mayCreate):
    # generates mine failure message

    msg = "I could not open a new mine on your behalf because"

    if not hasSpace:
        msg += " your current locale cannot support an additional mining venture"

    if not mayCreate:
        if not hasSpace:
            msg += " and"

        msg += " you do not have permission to open any more mines"

    return msg + "."

def strike_failure(fatigue, permitted):
    # generates strike failure message

    msg = ""

    if fatigue:
        msg += str(fatigue) + " seconds remaining"

    if not permitted:
        msg += "not permitted to strike that mine"

    return msg
