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
COMMANDS = []

## config

def init():
    # reloads all modules and initializes them

    imp.reload(game)
    game.init()
    load_cmd()

def load_cmd(commandfile=os.path.join(CONFIG, CMD_DEF)):
    # takes a commandfile and loads into memory

    global COMMANDS

    imp.reload(handlers)
    handlers.load(commandfile)
    COMMANDS = handlers.list()

## input processing

def process(channel, user, time, message):
    # main command processing

    response = []

    if re.match('^!', message):
        inputs = message.split(" ")
        command = inputs[0].split("!")[1]

        if command in COMMANDS:
            print("found command "+ command)
            handler = getattr(handlers, command)
            response.extend(handler(user, time, inputs))

    return response
