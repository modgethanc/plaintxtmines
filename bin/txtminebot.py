#!/usr/bin/python

## TODO: make this all only bot speaking; call kbot.say to
## actually communicate. move meta stuff to game.py.

import os.path
import random
import inflect
import json
import imp

import util

import world
import game
import mines
import players

### CONFIG
p = inflect.engine()
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")
CMD_DEF = "commands.json"

COMMANDS = {}

## lang import

def init():
    # reloads all modules and initializes them

    imp.reload(game)
    imp.reload(players)
    imp.reload(world)
    imp.reload(mines)
    game.init()

    load_cmd()

def load_cmd(commandfile=os.path.join(CONFIG, CMD_DEF)):
    # takes a commandfile and loads into memory

    global COMMANDS

    infile = open(commandfile, "r")
    COMMANDS = json.load(infile)
    infile.close()

### gameplay functions

def process(channel, user, time, message):
    # main command processing

    return "hi"
