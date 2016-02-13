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

def init(user, time, inputs):
    # takes care of creating a new player
    response = []

    print("called init handler!!!")

    return response

def open(user, time, inputs):

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

