#!/usr/bin/python

import random
import mines
import gibber
import os

j = ','

def newDossier(player): # makes a new .dossier file for named player
    playerfile = open('../data/'+player+'.dossier', 'w+')

    playerfile.write('\n') # 0 owned mines
    playerfile.write('\n') # 1 contracted mines
    playerfile.write("0,0,0,0,0,0,0,0\n") # 2 held res
    playerfile.write("0\n") # 3 total mined 
    playerfile.write("0,0,0,0,0,0,0,0\n") # 4 tithed res
    playerfile.write("0\n") # 5 tithed total
    playerfile.write("\n") # 6 finished mines
    playerfile.write("1,0,0,0\n") # 7 empress stats 
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
    ownedlist = openDossier(player)[0].rstrip().split(',')

    while ownedlist.count('') > 0:
        ownedlist.remove('') #dirty hack

    return ownedlist

def getContracted(player): #returns str list of contracted mines
    contractedlist = openDossier(player)[1].rstrip().split(',')

    while contractedlist.count('') > 0:
        contractedlist.remove('') #dirty hack

    return contractedlist

def getHeld(player): #returns list of held resources
    return openDossier(player)[2].rstrip().split(',')

def getHeldTotal(player): #returns int of current held assets
    total = 0
    for x in getHeld(player):
        total += int(x)

    return total

def getTotalMined(player): #returns int of all-time mined
    return int(openDossier(player)[3].rstrip())

def getTithed(player): #returns list of tithed resources
    return openDossier(player)[4].rstrip().split(',')

def getTithedTotal(player): #returns int of tithed total
    return int(openDossieer(player)[5].rstrip())

def getFinished(player): #returns str list of finished mines
    finishedlist = openDossier(player)[6].rstrip().split(',')

    while finishedlist .count('') > 0:
        finishedlist.remove('') #dirty hack

    return finishedlist

def getEmpressStats(player): #returns list of empress stats
    return openDossier(player)[7].rstrip().split(',')

def getAvailableMines(player): # returns int of number of free mines
    return int(getEmpressStats(player)[0])

### stats outputting

def openStats(player): # returns str list of the entire stats 
    playerfile = open('../data/'+player+'.stats', 'r')
    playerdata = []
    for x in playerfile:
        playerdata.append(x.rstrip())
    playerfile.close()

    return playerdata

def getLastStrike(player): #returns int of last strike time
    return int(openStats(player)[0])

def getTool(player): #returns str list of tool
    return openStats(player)[1].rstrip().split(',')

def getStrength(player): #returns int of strength
    return int(openStats(player)[2])

def getEndurance(player): #returns int of endurance
    return int(openStats(player)[3])

def getStrikes(player): #returns int of strike count
    return int(openStats(player)[4])

def getClearedCount(player): #returns int of cleared mines count
    return int(openStats(player)[5])

def fatigueCheck(player, time): # return remaining fatigue in seconds
    baseFatigue = 10 # hardcode bs
    return baseFatigue - int(time) - int(getLastStrike(player))

### dossier updating

def writeDossier(player, playerdata):
    playerfile = open('../data/'+player+'.dossier', 'w')
    for x in playerdata:
        playerfile.write(str(x) + "\n")
    playerfile.close()

def updateOwned(player, minelist): # overwrites previous minelist with passed in one
    playerdata = openDossier(player)
    playerdata[0] = j.join(minelist)
    writeDossier(player, playerdata)

    return mines

def updateEmpressStats(player, statlist): # overwrites previous empress stats
    playerdata = openDossier(player)
    playerdata[7] = j.join(statlist)
    writeDossier(player, playerdata)

    return statlist

def incAvailableMines(player): # increase mine permission
    statlist = getEmpressStats(player)
    statlist[0] = str(int(statlist[0]) + 1)
    updateEmpressStats(player, statlist)

    return int(statlist[0])

def decAvailableMines(player): # decrease mine permission
    statlist = getEmpressStats(player)
    statlist[0] = str(int(statlist[0]) - 1)
    updateEmpressStats(player, statlist)

    return int(statlist[0])

def incGrovel(player): # increase grovel count
    statlist = getEmpressStats(player)
    statlist[1] = str(int(statlist[1]) + 1)
    updateEmpressStats(player, statlist)

    return int(statlist[1])

def incTithe(player): # increase tithe count
    statlist = getEmpressStats(player)
    statlist[2] = str(int(statlist[2]) + 1)
    updateEmpressStats(player, statlist)

    return int(statlist[2])

def incFavor(player): # increase favor level
    statlist = getEmpressStats(player)
    statlist[3] = str(int(statlist[3]) + 1)
    updateEmpressStats(player, statlist)

    return int(statlist[3])

def decFavor(player): # decrease favor level
    statlist = getEmpressStats(player)
    statlist[3] = str(int(statlist[3]) - 1)
    updateEmpressStats(player, statlist)

    return int(statlist[3])

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

def incStrength(player): # increment strength
    playerdata = openStats(player)
    playerdata[2] = str(int(playerdata[2]) + 1)
    writeStats(player, playerdata)

    return playerdata[2]

def incEndurance(player): # increment endurance
    playerdata = openStats(player)
    playerdata[3] = str(int(playerdata[3]) + 1)
    writeStats(player, playerdata)

    return playerdata[3]

def incStrikes(player): # increment strike count
    status = '' #level up message

    playerdata = openStats(player)
    playerdata[4] = str(int(playerdata[4]) + 1)

    x = int(playerdata[2])
    if random.randrange(0,99) < 20/x: # scaling level up
        playerdata[2] = str(x+1)
        status = "You're feeling strong!  "

    writeStats(player, playerdata)

    return status

def incCleared(player): # increment cleared count
    playerdata = openStats(player)
    playerdata[5] = str(int(playerdata[5]) + 1)
    writeStats(player, playerdata)

    return int(playerdata[5])

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
    held = getHeld(player)

    return held[0]+ " tilde, "+held[1]+ " pound, "+held[2]+ " spiral, "+held[3]+ " amper, "+held[4]+ " splat, "+held[5]+ " lbrack, "+held[6]+ " rbrack, and "+held[7]+" carat, for a total of "+str(getHeldTotal(player))+" units"
