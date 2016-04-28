#!/usr/bin/python

import gibber
import util

import inflect
import json
import os
import random
import time

DATA = os.path.join("..", "data")
ATS = "empressautosave.json"
CONFIG = os.path.join("config")
EMPRESS = {}

## file i/o

def load(empressfile=os.path.join(DATA, ATS)):
    # takes a json from empressfile and loads to memory
    # returns empressfile location

    global EMPRESS

    infile = open(playerfile, "r")
    EMPRESS = json.load(infile)
    infile.close()

    return empressfile

def save(savefile=os.path.join(DATA, ATS)):
    # save current EMPRESS to savefile, returns save location

    outfile = open(savefile, "w")
    outfile.write(json.dumps(EMPRESS, sort_keys=True, indent=2, separators=(',', ':')))
    outfile.close()

    return savefile
