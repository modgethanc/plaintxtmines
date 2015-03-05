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
    # 3 favors

    playerfile.close()

    return player # for name confirmation

def newPlayer(player): # makes new player instance, including dossier
    newDossier(player)

    playerfile = open('../data/'+player+'.stats', 'w+')

    playerfile.write("0\n") # 0 last strike
    playerfile.write("0,0,0\n") # 1 tool
    playerfile.write("1\n") # 2 strength
    playerfile.write("1\n") # 3 endurance
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

    return playerdata[2] 

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
    playerdata[0] = str(time) + "\n"
    writeStats(player, playerdata)

    return time

def incStrikes(player): # increment strike count
    s = int(getStrikes(player))
    s += 1

    playerdata = openStats(player)
    playerdata[4] = str(s) + "\n"
    writeStats(player, playerdata)

    return s

#### mine wrangling

def newMine(player, rates):
    minename = gibber.medium()
    while os.path.isfile('../data/'+minename+'.mine'): # check for mine colision
        minename = gibber.medium()

    mines.writeMine(mines.generate(rates), '../data/'+minename+'.mine') # create minefile

    currentMines = getOwned(player)
    currentMines.append(minename)

    updateOwned(player, currentMines)

    return minename

## redundant shit; clean this up sometime

def new(player):
    newPlayer(player)

def lastMined(player): # REPLACED WITH  getLastStrike
    return getLastStrike(player)

def updateLast(player, time): # REPLACED WITH updateLastStrike
    updateLastStrike(player, time)

def totalResources(player): # REPLACED WITH getHeldTotal
    return getHeldTotal(player)

def updateMines(player, minelist): # REPLACED WITH updateOwned
    return updateOwned(player, minelist)

def getMines(player):
    minelist = getOwned(player)

    for x in getContracted(player):
        minelist.append(x)

    return minelist

def acquireRes(player, mine): # performs mining action 
    # TODO: include depth/width calculation
    excavation = mines.excavate('../data/'+mine+'.mine')

    held = getHeld(player)
    res = int(getTotalMined(player))

    i = 0
    for x in excavation:
        r = int(held[i]) + x
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
    playerdata = openDossier(player)
    held = getHeld(player)

    return held[0]+ " tilde, "+held[1]+ " pound, "+held[2]+ " spiral, "+held[3]+ " amper, "+held[4]+ " splat, "+held[5]+ " lbrack, "+held[6]+ " rbrack, and "+held[7]+" carat, for a total of "+str(totalResources(player))+" units"
