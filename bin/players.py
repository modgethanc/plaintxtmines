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

def newMine(player, rates):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []
    
    for x in playerfile:
         playerdata.append(x)

    minename = mines.writeMine(mines.generate(rates))
    playerdata[0] = playerdata[0].rstrip() + minename + ",\n"
    playerfile.close()

    playerfile = open('../data/'+player+'.player', 'w')
    for x in playerdata:
        playerfile.write(x)
    playerfile.close()

    return minename

def getMines(player):
    playerfile = open('../data/'+player+'.player', 'r')
    minelist = playerfile.readline().rstrip().split(',')
    minelist.remove('')
    playerfile.close()

    return minelist

def excavate(player, mine):
    holdings = getMines(player)
    if holdings.index(mine):
        return mines.excavate(mine)
    else:
        return "that's not ur mine"

#new("hvincent")
#print newMine("hvincent", "standardrates")
print getMines("hvincent")
print excavate("hvincent", getMines("hvincent")[0])
