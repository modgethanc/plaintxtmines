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
    golemfile.write(str(calcSize(golem))+"\n") # 2 size
    golemfile.write(str(calcWidth(golem))+"\n") # 3 width
    golemfile.write(str(calcStrength(golem))+"\n") # 4 strength
    golemfile.write(str(calcInterval(golem))+"\n") # 5 interval
    golemfile.write(str(calcDeath(golem, time))+"\n") # 6 death time
    golemfile.write(time+"\n") # 7 birth time
    golemfile.write(time+"\n") # 8 last strike
    golemfile.write("0,0,0,0,0,0,0,0\n") # 9 held res

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
    return calcSize(golem) * random.randrange(1, max(2, min(int(golem[1]), 10)))

def calcInterval(golem):
    return 200/max(1, min(int(golem[3]), 100))

def calcSize(golem): # total number of res
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
    #life = random.randrange(1, max(2,calcStrength(golem) * calcWidth(golem))) * random.randrange(1,max(calcStrength(golem), 50))
    tail = int(golem[0]) * random.randrange(1,10)
    life = 100 * random.randrange(1, calcStrength(golem)) + tail
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

def getSize(player): # return int of size
    return int(openGolem(player)[2])

def getWidth(player): # return int of width
    return int(openGolem(player)[3])

def getStrength(player): # return int of strength
    return int(openGolem(player)[4])

def getInterval(player): # return int of strength
    return int(openGolem(player)[5])

def getDeath(player): # return int of death time
    return int(openGolem(player)[6])

def getBirth(player): # return int of birth time
    return int(openGolem(player)[7])

def getLastStrike(player): # return int of birth time
    return int(openGolem(player)[8])

def getHeld(player): # return str list of held res
    return openGolem(player)[9].split(',')

def getLifeRemaining(player, time): # return int of seconds left
    return getDeath(player) - int(time)

def getLife(player, time): # return int of total seconds alive
    return int(time) - getBirth(player)

def getHeldTotal(player): #returns int of current held assets
    total = 0
    for x in getHeld(player):
        total += int(x)

    return total

def heldFormatted(player):
    held = getHeld(player)

    return held[0]+ " tilde, "+held[1]+ " pound, "+held[2]+ " spiral, "+held[3]+ " amper, "+held[4]+ " splat, "+held[5]+ " lbrack, "+held[6]+ " rbrack, and "+held[7]+" carat, for a total of "+str(getHeldTotal(player))+" units"

## golem updating

def writeGolem(player, golemdata):
    golemfile = open('../data/'+player+'.golem', 'w')
    for x in golemdata:
        golemfile.write(str(x) + "\n")
    golemfile.close()

def updateLastStrike(player, time):
    golemdata = openGolem(player)
    golemdata[8] = time
    writeGolem(player, golemdata)

    return time

## actions

def strike(player, target): # performs mining action
    excavation = mines.excavate(target, getStrength(player), getWidth(player))
    held = getHeld(player)

    i = 0
    for x in excavation:
        r = int(held[i]) + int(x)
        held[i] = str(r)
        i += 1

    golemdata = openGolem(player)
    golemdata[9] = j.join(held)

    writeGolem(player, golemdata)

    if random.randrange(1,100) < 50:
        decay(player, 1)

    return excavation

def decay(player, pieces):
    golemdata = openGolem(player)
    golemshape = list(golemdata[0])

    i = 0
    while i < pieces:
        chunk = random.randrange(0,len(golemshape))
        if golemshape[chunk] != " ":
            golemshape[chunk] = " "
            i += 1

    newshape = ''
    for x in golemshape:
        newshape += x

    golemdata[0] = newshape
    golemdata[2] = str(int(golemdata[2]) - pieces)
    writeGolem(player, golemdata)

    return golemdata[2]

def expire(player):
    golemheld = getHeld(player)
    os.remove("../data/"+player+".golem")
    players.acquireRes(player, golemheld)

    return golemheld

def destroy(player):
    golemheld = getHeld(player)
    os.remove("../data/"+player+".golem")
    recovered = []

    for x in golemheld:
        if int(x) > 0:
            recovered.append(random.randrange(0, max(1,int(x))))
        else:
            recovered.append(0)

    players.acquireRes(player, recovered)

    return recovered
