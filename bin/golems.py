#!/usr/bin/python

import players
import os
import random

j = ','

def newGolem(player, golemstring, time):
    golem = parse(golemstring)

    golemfile = open("../data/"+player+".golem", 'w+')
    golemfile.write(golemstring+"\n") # 0 golem string
    golemfile.write(j.join(golem)+"\n") # 1 golem stats
    golemfile.write(str(calcStrength(golem))+"\n") # 2 strength
    golemfile.write(str(calcWidth(golem))+"\n") # 3 width
    golemfile.write(str(calcDeath(golem, time))+"\n") # 4 death time


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
    total = 0
    for x in golem:
        total += int(x)

    return total

def calcWidth(golem): # number of different res
    width = 0
    for x in golem:
        if x > 0:
            width += 1

    return width

def calcDeath(golem, time): # calcuate expiration time
    death = int(time)
    life = calcStrength(golem) * 100
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

def getShape(player):
    return openGolem(player)[0]

def getStats(player):
    return parse(getShape(player)) # kind of dumb??

def getStrength(player): # return int of strength
    return int(openGolem(player)[2])

def getWidth(player): # return int of width
    return int(openGolem(player)[3])

def getDeath(player): # return int of death time
    return int(openGolem(player)[0])
