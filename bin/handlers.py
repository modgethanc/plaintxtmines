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
            if zoneID:
                if game.has_space(zoneID, "residents"):
                    newID = successful_join(user, now, zoneID)
                    print("new player: "+newID)
                    response.append("Your citizenship is now acknowledged.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with \"!new\".")
                else:
                    response.append("I'm sorry, friend, but that province cannot support any additional residents.  Please choose a different one in order to prevent overcrowding.")
            else:
                response.append("I've never heard of that province, stranger.")

    return response

def successful_join(user, now, zoneID):
    # creates a new player

    playerdata = {}
    playerdata.update({"nick":user})
    playerdata.update({"home":zoneID})
    playerdata.update({"joined":now})

    return game.new_player(playerdata)

def new(user, time, inputs):

    response = []

    return response

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

