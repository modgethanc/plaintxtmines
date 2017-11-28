#!/usr/bin/python
'''
This contains the class and functions for players.

On creation, a player is given a file with stats and a dossier. It's possible
for a player to exist without a dossier; players that burn their file can
restart the game with a clean state, but maintain all their physical stats.

Player attributes:
    (stats)
    name: name that the mining assistant addresses them
    aliases: list of strings for valid aliases
    lastStrike: int of timestamp of last strike
    strength: int of strength
    endurance: int of endurance
    lifetimeStrikes: int of total lifetime strikes
    lifetimeCompleted : int of total lifetime completed mines
    lifetimeGrovels: int of total lifetime grovels

    (dossier)
    minesOwned : list of strings of mine names the player owns
    minesAssigned: list of strings of mine names the player has additional
        permission to work on
    minesCompleted : list of strings of mine names the player has completed
    minesAvailable: int of how many mines player can currently open
    resHeld: 8-item int array of currently held resources (*)
    grovelCount: int of current grovel count
    strikeCount: int of current strike count

(*): see documentation for mines for note about reslist

plaintxtmines is a text-based multiplayer mining simulator. For more
information, see the full repository:

https://github.com/modgethanc/plaintxtmines
'''

import random
import os

import vtils
import mines
import gibber

j = ','

class Player():
    '''
    Implements a player object.
    '''

    def __init__(self, player_input):
        '''
        Initial player conditions.
        '''

        # stats
        self.name = player_input.nick
        self.aliases = []
        self.lastStrike = 0
        self.strength = 1
        self.endurance = 0
        self.lifetimeStrikes = 0
        self.lifetimeCompleted = 0
        self.lifetimeGrovels = 0

        # dossier
        self.minesOwned = []
        self.minesAssigned = []
        self.minesCompleted = []
        self.minesAvailable = 1
        self.resHeld = [0,0,0,0,0,0,0,0]
        self.grovelCount = 0
        self.strikeCount = 0

        self.save()

    def save(self):
        '''
        Write self to disk.
        '''

        filename = "../data/" + self.name+ ".player"
        vtils.write_dict_as_json(filename, self.to_dict())

        return filename


    def to_dict(self):
        '''
        Turns all data into a dict.
        '''

        playerData = {
            "name": self.name,
            "aliases": self.aliases,
            "last strike": self.lastStrike,
            "strength": self.strength,
            "endurance": self.endurance,
            "lifetime strikes": self.lifetimeStrikes,
            "lifetime completed": self.lifetimeCompleted,
            "lifetime grovels": self.lifetimeGrovels,
            "mines owned": self.minesOwned,
            "mines assigned": self.minesAssigned,
            "mines completed": self.minesCompleted,
            "mines available": self.minesAvailable,
            "res held": self.resHeld,
            "grovel count": self.grovelCount,
            "strike count": self.strikeCount
            }

        return playerData


    def load(self, playerName):
        '''
        Loads a player from file for the named player, then returns own name for
        verification.
        '''

        filename = playerName + ".player"

        playerData = vtils.open_json_as_dict("../data/"+filename)

        self.name = playerData.get("name")
        self.aliases = playerData.get("aliases")
        self.lastStrike = playerData.get("last strike")
        self.strength = playerData.get("strength")
        self.endurance = playerData.get("endurance")
        self.lifetimeStrikes = playerData.get("lifetime strikes")
        self.lifetimeCompleted = playerData.get("lifetime completed")
        self.lifetimeGrovels = playerData.get("lifetime grovels")
        self.minesOwned = playerData.get("mines owned")
        self.minesAssigned = playerData.get("mines assigned")
        self.minesCompleted = playerData.get("mines completed")
        self.minesAvailable = playerData.get("mines available")
        self.resHeld = playerData.get("res held")
        self.grovelCount = playerData.get("grovel count")
        self.strikeCount = playerData.get("strike count")

        return self.name

    def burn(self):
        '''
        Removes player's dossier info.
        '''

        pass

    def create(self):
        '''
        Creates a new dossier for this player.
        '''

        pass


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
    return (baseFatigue - min(9, getEndurance(player))) - (int(time) - int(getLastStrike(player)))

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

def removeRes(player, reslist): # subtracts reslist from player
    held = getHeld(player)
    res = int(getTotalMined(player))

    i = 0
    for x in reslist:
        r = int(held[i]) - int(x)
        res -= int(x)
        held[i] = str(r)
        i += 1

    playerdata = openDossier(player)
    playerdata[2] = j.join(held)
    playerdata[3] = res

    writeDossier(player, playerdata)

    return reslist

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

def newMine(player, minename):

    currentMines = getOwned(player)
    currentMines.append(minename)

    updateOwned(player, currentMines)

    return minename

def getMines(player):
    minelist = getOwned(player)

    for x in getContracted(player):
        minelist.append(x)

    return minelist

def strike(player, mine): # performs mining action
    baseDepth = 3
    strikeDepth = baseDepth * getStrength(player)

    return mine.excavate(strikeDepth)

def acquireRes(player, excavation): # adds res to held
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

def canAfford(player, cost): # checks list of res against held
    held = getHeld(player)
    i = 0
    while i < 8:
        if int(held[i]) < int(cost[i]):
            return False
        i += 1

    return True

def printExcavation(excavation):
    total = 0

    for x in excavation:
        total += int(x)

    if total == 0:
        return "nothing but rubble."

    if total > 100:
        return "a lot of resources!"

    mined = ''
    y = 0
    for x in excavation:
        if y == 0: item = '~'
        elif y == 1: item = '#'
        elif y == 2: item = '@'
        elif y == 3: item = '&'
        elif y == 4: item = '*'
        elif y == 5: item = '['
        elif y == 6: item = ']'
        elif y == 7: item = '^'

        i = 0
        while i < int(x):
            mined += item
            i += 1

        y += 1

    return mined

def heldFormatted(player):
    held = getHeld(player)

    return held[0]+ " tilde, "+held[1]+ " pound, "+held[2]+ " spiral, "+held[3]+ " amper, "+held[4]+ " splat, "+held[5]+ " lbrack, "+held[6]+ " rbrack, and "+held[7]+" carat, for a total of "+str(getHeldTotal(player))+" units"
