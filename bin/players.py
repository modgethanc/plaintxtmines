#!/usr/bin/python

import random
import mines
import gibber
import os

def newDossier(player): # makes a new .dossier file for named player
    playerfile = open('../data/'+player+'.dossier', 'w+')

    playerfile.write('\n') # 0 owned mines
    playerfile.write('\n') # 1 contracted mines
    playerfile.write("0,0,0,0,0,0,0,0\n") # 2 held res
    playerfile.write("0\n") # 3 total mined 
    playerfile.write("0,0,0,0,0,0,0,0\n") # 4 tithed res
    playerfile.write("0\n") # 5 tithed total
    playerfile.write("\n") # 6 finished mines
    playerfile.write("0,0,0,0\n") # 7 empress stats 
    # 0 available mines
    # 1 grovel count
    # 2 tithe count
    # 3 favor level

    playerfile.close()

    return player # for name confirmation

def newPlayer(player): # makes new player instance, including dossier
    newDossier(player)

    playerfile = open('../data/'+player+'.stats', 'w+')

    playerfile.write("0\n") # 0 last strike
    playerfile.write("0,0,0\n") # 1 tool
    playerfile.write("1\n") # 2 strength
    playerfile.write("0\n") # 3 endurance
    playerfile.write("0\n") # 4 strike count
    playerfile.write("0\n") # 5 mine completion count
    # player.golem

    playerfile.close()

    return player # for name confirmation

### dossier outputting

def openDossier(player): # returns str list of the entire dossier
    playerfile = open('../data/'+player+'.dossier', 'r')

    playerdata = []
    for x in playerfile:
        playerdata.append(x.rstrip())

    playerfile.close()
    return playerdata

def getOwned(player): # returns str list of owned mines
    playerdata = openDossier(player)

    ownedlist = playerdata[0].rstrip().split(',')

    while ownedlist.count('') > 0:
        ownedlist.remove('') #dirty hack

    return ownedlist

def getContracted(player): #returns str list of contracted mines
    playerdata = openDossier(player)

    contractedlist = playerdata[1].rstrip().split(',')

    while contractedlist.count('') > 0:
        contractedlist.remove('') #dirty hack

    return contractedlist

def getHeld(player): #returns int list of held resources
    playerdata = openDossier(player)

    heldlist = playerdata[2].rstrip().split(',')

    return heldlist

def getHeldTotal(player): #returns int of current held assets
    res = getHeld(player)
    total = 0
    for x in res:
        total += int(x)

    return total

def getTotalMined(player): #returns int of all-timee mined
    playerdata = openDossier(player)
    total = playerdata[3].rstrip()

    return total

def getTithed(player): #returns int list of tithed resources
    playerdata = openDossier(player)
    tithedist = int(playerdata[4].rstrip().split(','))

    return tithedlist

def getTithedTotal(player): #returns int of tithed total
    playerdata = openDossier(player)
    tithed = int(playerdata[5].rstrip())

    return tithed

def getFinished(player): #returns str list of finished mines
    playerdata = openDossier(player)
    finishedlist = playerdata[6].rstrip().split(',')

    while finishedlist .count('') > 0:
        finishedlist.remove('') #dirty hack

    return finishedlist

def getEmpressStats(player): #returns int list of empress stats
    playerdata = openDossier(player)
    empressstats = playerdata[7].rstrip().split(',')

    return empressstats

### stats outputting

def openStats(player): # returns str list of the entire stats 
    playerfile = open('../data/'+player+'.stats', 'r')

    playerdata = []
    for x in playerfile:
        playerdata.append(x.rstrip())

    playerfile.close()

    return playerdata

def getLastStrike(player): #returns int of last strike time
    playerdata = openStats(player)
    return playerdata[0] 

def getTool(player): #returns str list of tool
    playerdata = openStats(player)
    tool = playerdata[1].rstrip().split(',')

    return tool 

def getStrength(player): #returns int of strength
    playerdata = openStats(player)

    return int(playerdata[2])

def getEndurance(player): #returns int of endurance
    playerdata = openStats(player)

    return playerdata[3] 

def getStrikes(player): #returns int of strike count
    playerdata = openStats(player)

    return playerdata[4]

def getClearedCount(player): #returns int of cleared mines count
    playerdata = openStats(player)

    return playerdata[5] 

### dossier updating

def writeDossier(player, playerdata):
    playerfile = open('../data/'+player+'.dossier', 'w')
    for x in playerdata:
        playerfile.write(str(x) + "\n")
    playerfile.close()

def updateOwned(player, minelist): # overwrites previous minelist with passed in one
    mines = ''
    j = ','
    mines = j.join(minelist)

    playerdata = openDossier(player)
    playerdata[0] = mines

    writeDossier(player, playerdata)

    return mines

### stats updating

def writeStats(player, playerdata):
    playerfile = open('../data/'+player+'.stats', 'w')
    for x in playerdata:
        playerfile.write(str(x) + "\n")
    playerfile.close()

def updateLastStrike(player, time):
    playerdata = openStats(player)
    playerdata[0] = str(time)
    writeStats(player, playerdata)

    return time

def incStrikes(player): # increment strike count
    status = ''
    s = int(getStrikes(player))
    s += 1

    playerdata = openStats(player)
    playerdata[4] = str(s)

    x = int(playerdata[2])
    if random.randrange(0,99) < 20/x: # scaling level up
        x += 1
        playerdata[2] = str(x)
        status = "You're feeling strong!  "

    ### rank-based rates
    #if x < 4: # low level rates
    #    if random.randrange(0,99) < 15:
    #        x += 1
    #        playerdata[2] = str(x)
    #        status = "You're feeling strong!  "
    #elif x < 8: # mid level rates
    #    if random.randrange(0,99) < 8:
    #        x += 1
    #        playerdata[2] = str(x)
    #        status = "You're feeling strong!  "
    #else: # high level rates
    #    if random.randrange(0,99) < 1:
    #        x += 1
    #        playerdata[2] = str(x)
    #        status = "You're feeling strong!  "

    writeStats(player, playerdata)

    return status

def incCleared(player): # increment cleared count
    c = int(getClearedCount(player))
    c += 1

    playerdata = openStats(player)
    playerdata[5] = str(c)
    writeStats(player, playerdata)

    return c

def incEndurance(player): # increment endurance
    e = int(getEndurance(player))
    e += 1

    playerdata = openStats(player)
    playerdata[3] = str(e)
    writeStats(player, playerdata)

    return e

def fatigueCheck(player, time): # return remaining fatigue in seconds
    baseFatigue = 10 # hardcode bs
    diff = int(time)-int(getLastStrike(player))
    left =  baseFatigue - diff

    return left

#### mine wrangling

def newMine(player, rates):
    minename = mines.newMine(player, rates)

    currentMines = getOwned(player)
    currentMines.append(minename)

    updateOwned(player, currentMines)

    return minename

def getMines(player):
    minelist = getOwned(player)

    for x in getContracted(player):
        minelist.append(x)

    return minelist

def acquireRes(player, mine): # performs mining action 
    baseDepth = 3
    strikeDepth = baseDepth * getStrength(player)

    excavation = mines.excavate(mine, strikeDepth)

    held = getHeld(player)
    res = int(getTotalMined(player))

    i = 0
    for x in excavation:
        r = int(held[i]) + int(x)
        res += int(x)
        held[i] = str(r)
        i += 1

    j = ','
    playerdata = openDossier(player)
    playerdata[2] = j.join(held)
    playerdata[3] = res

    writeDossier(player, playerdata)

    return excavation

def printExcavation(excavation):
    total = 0

    for x in excavation:
        total += int(x)

    if total == 0:
        return "nothing but rubble."

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

def heldFormatted(player):
    playerdata = openDossier(player)
    held = getHeld(player)

    return held[0]+ " tilde, "+held[1]+ " pound, "+held[2]+ " spiral, "+held[3]+ " amper, "+held[4]+ " splat, "+held[5]+ " lbrack, "+held[6]+ " rbrack, and "+held[7]+" carat, for a total of "+str(getHeldTotal(player))+" units"


