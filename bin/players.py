#!/usr/bin/python

import random
import mines
import names
import os

def new(player):
    playerfile = open('../data/'+player+'.player', 'w+')

    playerfile.write('\n')
    i = 0
    while i < 8:
        playerfile.write("0\n")
        i += 1
    
    playerfile.write("0\n")
    playerfile.close()

    return player

def newMine(player, rates):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []

    for x in playerfile:
        playerdata.append(x)

    minename = names.medium()
    while os.path.isfile('../data/'+minename+'.mine'):
        minename = names.medium()

    mines.writeMine(mines.generate(rates), '../data/'+minename+'.mine')
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

def updateMines(player, minelist):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []

    for x in playerfile:
        playerdata.append(x)

    playerfile.close()

    minelist.append('')
    mines = ''
    j = ','
    mines = j.join(minelist)

    playerdata[0] = mines + "\n"

    playerfile = open('../data/'+player+'.player', 'w')
    for x in playerdata:
        playerfile.write(x)
    playerfile.close()

    return mines

def lastMined(player):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []

    for x in playerfile:
        playerdata.append(x)

    return playerdata[-1]

def updateLast(player, time):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []

    for x in playerfile:
        playerdata.append(x)

    playerfile.close()

    playerdata[-1] = str(time) + "\n"

    playerfile = open('../data/'+player+'.player', 'w')
    for x in playerdata:
        playerfile.write(x)
    playerfile.close()

def excavate(player, mine):
    holdings = getMines(player)
    if holdings.count(mine) > 0:
        return mines.excavate('../data/'+mine+'.mine')
    else:
        return "that's not ur mine"

def acquire(player, excavation):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []

    for x in playerfile:
        playerdata.append(str(x).rstrip())

    playerfile.close()

    i = 0
    for x in excavation:
        res = int(playerdata[i+1])
        res += excavation[i]
        playerdata[i+1] = res
        i += 1

    playerfile = open('../data/'+player+'.player', 'w')
    for x in playerdata:
        playerfile.write(str(x)+'\n')
    playerfile.close()

    return excavation

def printExcavation(excavation):
    total = 0

    for x in excavation:
        total += x

    if total == 0:
        return "nothing useful..."

    mined = ''
    y = 0
    for x in excavation:
        if y == 0:
            item = '~'
        elif y == 1:
            item = '#'
        elif y == 2:
            item = '@'
        elif y == 3:
            item = '&'
        elif y == 4:
            item = '*'
        elif y == 5:
            item = '['
        elif 7 == 6:
            item = ']'
        elif y == 7:
            item = '^'

        i = 0
        while i < int(x):
            mined += item
            i += 1

        y += 1

    return mined

def report(player):
    playerfile = open('../data/'+player+'.player', 'r')
    playerdata = []

    for x in playerfile:
        playerdata.append(str(x).rstrip())

    playerfile.close()

    return playerdata[1]+ "x tilde, "+playerdata[2]+ "x pound, "+playerdata[3]+ "x spiral, "+playerdata[4]+ "x amper, "+playerdata[5]+ "x splat, "+playerdata[6]+ "x lbrack, "+playerdata[7]+ "x rbrack, "+playerdata[8]+"x carat"

#new("hvincent")
#print newMine("hvincent", "standardrates")
#print getMines("hvincent")
#print report(acquire("hvincent", excavate("hvincent", getMines("hvincent")[0])))
#mined("hvincent")
