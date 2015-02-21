#!/usr/bin/python

import random
import mines

def new(player):
    playerfile = open('../data/'+player+'.player', 'w+')
   
    playerfile.write('\n')
    i = 0
    while i < 8:
        playerfile.write("0\n")
        i += 1

    playerfile.close()

    return player

def newMine(player):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []
    
    for x in playerfile:
         playerdata.append(x)

    minename = mines.writeMine(mines.generate("standardrates"))
    minelist = playerdata[0].rstrip()
    minelist += "," + minename + "\n"
    playerdata[0] = minelist
    playerfile.close()

    playerfile = open('../data/'+player+'.player', 'w')
    for x in playerdata:
        playerfile.write(x)

    return minename

new("hvincent")
print newMine("hvincent")
