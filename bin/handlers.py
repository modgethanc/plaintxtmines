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
STRANGER = "I don't know who you are, stranger.  If you'd like to enlist your talents in the name of the empress, you may do so with \"!join PROVINCE\"."

## file i/o

def load(commandfile=os.path.join(CONFIG, CMD_DEF)):
    # takes a commandfile and loads into memory

    global COMMANDS

    infile = open(commandfile, "r")
    COMMANDS = json.load(infile)
    infile.close()

def list():
    # returns a list of all loaded commands

    return [command for command in iter(COMMANDS)]

## base handler functions

def join(user, now, inputs):
    # creates a new player

    response = []

    playerID = game.is_playing(user)

    if playerID:
        response.append("You are already registered, my friend.")
    else:
        if len(inputs) < 2:
            response.append("You must declare a province to which you call home, stranger.")
        else:
            zoneID = game.is_zone(inputs[1])
            newID, hasSpace, zoneExists = game.new_player(make_player(user, now, zoneID))
            if newID:
                print("new player: "+newID)
                response.append("Your citizenship is now acknowledged.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with \"!new\".")
            else:
                response.append(failed_join(hasSpace, zoneExists))

    return response

def make_player(user, now, zoneID):
    # creates a new player

    playerdata = {}
    playerdata.update({"nick":user})
    playerdata.update({"home":zoneID})
    playerdata.update({"joined":now})

    return playerdata

def failed_join(hasSpace, zoneExists):
    # processes join failure

    if not zoneExists:
        return "I've never heard of that province, stranger."

    if not hasSpace:
        return "I'm sorry, friend, but that province cannot support any additional residents.  Please choose a different one in order to prevent overcrowding."

def new(user, time, inputs):
    # new mine creation
    print("creating new mine for "+user)

    response = []
    playerID = game.is_playing(user)

    if playerID:
        mineID, hasSpace, mayCreate = game.new_mine(playerID)
        if mineID:
            minename = game.name_mine(mineID)
            response.append("Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+minename+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts, and begin with an enthusiastic \'!strike\".")
        else:
            response.append(failed_new(hasSpace, mayCreate))
    else:
        response.append(STRANGER)

    return response

def failed_new(hasSpace, mayCreate):
    # generated mine failure message

    msg = "I could not open a new mine on your behalf because"

    if not hasSpace:
        msg += " your current locale cannot support an additional mining venture"

    if not mayCreate:
        if not hasSpace:
            msg += " and"

        msg += " you do not have permission to open any more mines"

    return msg + "."

def grovel(user, time, inputs):

    response = []

    return response

def mines(user, time, inputs):

    response = []

    return response

def info(user, time, inputs):

    response = []

    return response

def stats(user, time, inputs):

    response = []

    return response

def fatigue(user, time, inputs):

    response = []

    return response

def report(user, time, inputs):

    response = []

    return response

def strike(user, time, inputs):

    response = []

    return response

def rankings(user, time, inputs):

    response = []

    return response

def golem(user, time, inputs):

    response = []

    return response

def res(user, time, inputs):

    response = []

    return response

