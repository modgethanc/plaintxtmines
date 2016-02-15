#!/usr/bin/python

## TODO: make this all only bot speaking; call kbot.say to
## actually communicate. move meta stuff to game.py.

import os.path
import random
import inflect
import json
import imp
import re

import util
import handlers

import game

p = inflect.engine()
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")
CMD_DEF = "commands.json"
COMMANDS = {}
STRANGER = "I don't know who you are, stranger.  If you'd like to enlist your talents in the name of the empress, you may do so with \"!join PROVINCE\"."

## i/o

def init():
    # reloads all modules and initializes them

    imp.reload(game)
    imp.reload(handlers)
    game.init()
    handlers.init()

def load_cmd(commandfile=os.path.join(CONFIG, CMD_DEF)):
    # takes a commandfile and loads into memory via handlers

    global COMMANDS

    imp.reload(handlers)
    handlers.load(commandfile)
    COMMANDS = handlers.COMMANDS

def save():
    # calls game save

    game.save()

## input processing

def handle(user, time, message):
    # main command processing

    response = []
    print("handling: "+message)
    if re.match('^:!', message):
        inputs = message.split(" ")
        command = inputs[0].split("!")[1]

        if command in COMMANDS:
            print("found command "+ command)
            playerID = game.is_playing(user)

            if COMMANDS[command].get("player only"):
                if playerID:
                    handler = getattr(handlers, command)
                    response.extend(handler(playerID, user, time, inputs))
                else:
                    response.append(STRANGER)
            else:
                handler = getattr(handlers, command)
                response.extend(handler(playerID, user, time, inputs))

    return response
