#!/usr/bin/python

import players
import mines
import os
import random

j = ','

def newGolem(player, golemstring, time):
    golem = parse(golemstring)

    golemfile = open("../data/"+player+".golem", 'w+')
    golemfile.write(golemstring+"\n") # 0 golem string
    golemfile.write(j.join(golem)+"\n") # 1 golem stats
    golemfile.write(str(calcHeight(golem))+"\n") # 2 height
    golemfile.write(str(calcWidth(golem))+"\n") # 3 width
    golemfile.write(str(calcStrength(golem))+"\n") # 4 strength
    golemfile.write(str(calcDeath(golem, time))+"\n") # 5 death time
    golemfile.write(time+"\n") # 6 birth

    golemfile.close()
    return golemstring

def parse(golemstring):
    golem = [0,0,0,0,0,0,0,0]
    components = list(golemstring)

    for x in components:
        if x == '~': golem[0] += 1
        elif x == '#': golem[1] += 1
        elif x == '@': golem[2] += 1
        elif x == '&': golem[3] += 1
        elif x == '*': golem[4] += 1
        elif x == '[': golem[5] += 1
        elif x == ']': golem[6] += 1
        elif x == '^': golem[7] += 1

    i = 0
    while i < 8: # stupid string hax
        r = str(golem[i])
        golem[i] = r
        i += 1

    return golem

def calcStrength(golem):
    return calcHeight(golem) * calcWidth(golem)

def calcHeight(golem): # total number of res
    total = 0
    for x in golem:
        total += int(x)

    return total

def calcWidth(golem): # number of different res
    width = 0
    for x in golem:
        if int(x) > 0:
            width += 1

    return width

def calcDeath(golem, time): # calcuate expiration time
    death = int(time)
    life = random.randrange(1, max(2,calcStrength(golem) * calcWidth(golem))) * random.randrange(1,max(calcStrength(golem), 50))
    death = int(time) + life

    return death

### golem outputting

def openGolem(player):
    golemfile = open('../data/'+player+'.golem', 'r')
    golemdata = []
    for x in golemfile:
        golemdata.append(x.rstrip())
    golemfile.close()

    return golemdata

def getShape(player): # return str of shape
    return openGolem(player)[0]

def getStats(player): # return str list of stats
    return openGolem(player)[1].split(',')

def getHeight(player): # return int of height 
    return int(openGolem(player)[2])

def getWidth(player): # return int of width
    return int(openGolem(player)[3])

def getStrength(player): # return int of strength 
    return int(openGolem(player)[4])

def getDeath(player): # return int of death time
    return int(openGolem(player)[5])

def getBirth(player): # return int of birth time
    return int(openGolem(player)[6])

def getLifeRemaining(player, time): # return int of seconds left
    return getDeath(player) - int(time)

## golem updating

def writeGolem(player, golemdata):
    golemfile = open('../data/'+player+'.golem', 'w')
    for x in golemdata:
        golemfile.write(str(x) + "\n")
    golemfile.close()

def updateLastStrike(player, time):
    golemdata = openGolem(player)
    golemdata[6] = time
    writeGolem(player, golemdata)

    return time

## actions

def expire(player):
    mineList = players.getMines(player)
    target = mineList[0] #autotarget first mine
    strikes = (getDeath(player) - getBirth(player))/10

    i = 0
    golemstrike = [0,0,0,0,0,0,0,0]
    while i < strikes:
        excavation = mines.excavate(target, getStrength(player), getWidth(player))
        j = 0
        while j < 8:
            golemstrike[j] += excavation[j]
            j += 1

        i += 1

    players.acquireRes(player, golemstrike)
    return golemstrike
