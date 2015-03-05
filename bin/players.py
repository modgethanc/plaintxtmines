#!/usr/bin/python

import random
import mines
import gibber
import os

# PLAYER.DOSSIER
# 0 owned mines
# 1 contracted mines
# 2 held res
# 3 mined total
# 4 tithed res
# 5 tithed total

# PLAYER.STATS
# 0 last strike
# 1 tool
# 3 golem

def newDossier(player): # makes a new .dossier file for named player
    playerfile = open('../data/'+player+'.dossier', 'w+')

    playerfile.write('\n') # owned mines
    playerfile.write('\n') # contracted mines
    playerfile.write("0,0,0,0,0,0,0,0\n") # held res
    playerfile.write("0\n") # all-time mined
    playerfile.write("0,0,0,0,0,0,0,0\n") # tithed res
    playerfile.write("0\n") # tithed total

    playerfile.close()

    return player # for name confirmation

def newPlayer(player):
    newDossier(player)

    playerfile = open('../data/'+player+'.stats', 'w+')

    playerfile.write("0\n") # last strike
    playerfile.write("0,0,0\n") # tool
    playerfile.write("\n") # golem

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

    tool = playerdata[0].rstrip().split(',')

    return tool 

def getGolem(player): #returns str of golem
    playerdata = openStats(player)

    golem = playerdata[0].rstrip()

    return golem

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

########### LINE OF DEATH ###############

def excavate(player, mine):
    holdings = getMines(player)

    if holdings.count(mine) > 0: # this check shoudn't happen here
        return mines.excavate('../data/'+mine+'.mine')
    else:
        return "that's not ur mine"

def acquire(player, excavation):
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
