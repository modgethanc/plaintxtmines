#!/usr/bin/python

import game

import os

WWW = os.path.join("www")
CONFIG = os.path.join("config")

HEADER = []
FOOTER = []

infile = open(os.path.join(CONFIG, "outhead.txt"), 'r')
for line in infile:
    HEADER.append(line.rstrip())
infile.close()

infile = open(os.path.join(CONFIG, "outfoot.txt"), 'r')
for line in infile:
    FOOTER.append(line.rstrip())
infile.close()

def write(outurl):
    outfile = open(os.path.join(WWW, outurl), "w")

    for line in HEADER:
        outfile.write(line)

    outfile.write("<h1>whatup</h1>")

    for line in FOOTER:
        outfile.write(line)

    outfile.close()
