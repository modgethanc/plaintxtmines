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

    outfile.write("<h1>STATE OF THE EMPRESS'S DOMAIN</h1>") 

    outfile.write("<h3>Provinces recognized by the empress</h3>")
    outfile.write("<ul>")
    for zone in game.list_zones():
      outfile.write("<li>"+zone+"</li>")
    outfile.write("</ul>")

    outfile.write("<h3>Workers registered as citizens</h3>")
    outfile.write("<ul>")
    for player in game.list_players():
      outfile.write("<li>"+player+" ("+game.player_home(game.is_playing(player))+")</li>")
    outfile.write("</ul>")

    for line in FOOTER:
        outfile.write(line)

    outfile.close()
