#!/usr/bin/python

import inflect
import os
import json
import random
import util
import game

p = inflect.engine()
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")
CMD_DEF = "commands.json"
LANG_DEF = "lang.json"
COMMANDS = {}
LANG = {}
UNIMP = "I'm sorry, friend, but this function is currently disabled.  I expect it to return with an improved ability to support your mining ventures."

## file i/o

def init():
    # calls all the loading methods

    load_lang()
    load_cmd()

def load_lang(langfile=os.path.join(CONFIG, LANG_DEF)):
    # takes a langfile and loads into memory

    global LANG

    infile = open(langfile, "r")
    LANG = json.load(infile)
    infile.close()

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
            #zoneID = game.is_zone(inputs[1])
            zoneID = game.match_province(inputs[1])
            newID, hasSpace, zoneExists = game.new_player(make_player(user, now, zoneID))
            if newID:
                print("new player: "+newID)
                response.append("Your citizenship of the province of "+game.name_zone(zoneID)+" is now acknowledged.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with \"!new\".")
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

    response.append(UNIMP)

    return response

def mines(playerID, user, time, inputs):

    response = []

    minelist = game.list_mines(playerID)

    msg = "You own the following "+p.plural("mines", len(minelist))+": "
    msg += ", ".join(minelist)

    response.append(msg)

    return response

def info(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def stats(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def fatigue(playerID, user, now, inputs):

    response = []

    fatigue = game.fatigue_left(playerID, now)

    if fatigue:
        response.append("You'll be ready to strike again in "+util.pretty_time(fatigue)+".  Please rest patiently so you do not stress your body.")
    else:
        response.append("You're refreshed and ready to mine.  Take care to not overwork; a broken body is no use to the empress.")

    return response

def report(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def strike(playerID, user, now, inputs):

    response = []

    if len(game.list_mines(playerID)) < 1:
        response.append("I'm sorry, friend, but you have no mines at which to strike.  Open a new mine with \"!new\",")
        return response

    if len(inputs) < 2:
        targetted = game.targetted(playerID)
    else:
        targetted = game.is_mine(inputs[1])
        if not targetted:
            targetted = game.targetted(playerID)

    fatigue, permitted, depleted, reslist = game.strike(playerID, targetted, now)

    mineName = game.name_mine(targetted)

    if reslist:
        response.append(random.choice(LANG.get("wham")) + "  You struck at "+ mineName + " and mined the following: "+ game.print_reslist(reslist))
        if depleted:
            response.append("As you clear the last of the rubble from "+mineName+", a mysterious wisp of smoke rises from the bottom.  You feel slightly rejuvinated when you breathe it in.")
    else:
        response.append(strike_failure(fatigue, permitted))

    return response

def rankings(playeID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def golem(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def res(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def alias(playerID, user, time, inputs):

    response = []

    if len(inputs) < 2:
        response.append("You need to specify at least one alias to add to your dossier, friend.")
    else:
        inputs.pop(0)
        added = []
        unadded = []
        print(inputs)
        for alias in inputs:
            if game.alias(playerID, alias):
                added.append(alias)
            else:
                unadded.append(alias)
        if added:
            response.append("I've added "+",".join(added)+" to your alias list.")
        if unadded:
            response.append(", ".join(added)+" could not be added due to conflicting records.")

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

    msg = "The following "+p.plural("province", len(zones))+" "+p.plural("falls", len(zones))+" under the empress's rule: "
    msg += ", ".join(zones)

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
        msg += "You're still tired from your last attempt.  You'll be ready again in "+str(fatigue)+" seconds.  Please take breaks to prevent fatigue; rushing will only lengthen your recovery."

    if not permitted:
        if fatigue:
            msg += "  Additionally, y"
        else:
            msg += "Y"

        msg += "ou do not have permission to work on that mine, friend."

    return msg
