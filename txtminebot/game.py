#!/usr/bin/python
'''
This is the core game engine that handles processing all game actions, including
maintaining world state.

plaintxtmines is a text-based multiplayer mining simulator. For more
information, see the full repository:

https://github.com/modgethanc/plaintxtmines
'''

__author__ = "Vincent Zeng (hvincent@modgethanc.com)"

import os
import random
import time

import players
import golems
import mines
import gibber
import empress

def reset():
    '''
    Reload game dependencies.
    '''

    reload(players)
    reload(golems)
    reload(mines)
    reload(gibber)
    reload(empress)

## globals

GAMEDIR = os.path.join("..", "data")
BASE_FATIGUE = 10

## game objects

GOLEMS = {}
PLAYERS = {}
MINES = {}
EMPRESS = None

## game inquiries

def is_playing(playerName):
    '''
    Returns whether or not the named user has a dossier on file.
    '''

    player = PLAYERS.get(playerName)

    if not player:
        return False
    else:
        return player.playing

def is_mine(mineName):
    '''
    Returns whether or not the named mine exists.
    '''

    return MINES.has_key(mineName)

def player_may_open(playerName):
    '''
    Returns whether or not the named player has permission to open a new mine.
    '''

    return PLAYERS.get(playerName).minesAvailable > 0

def player_strength(playerName):
    '''
    Returns the player's strength attribute.
    '''

    return PLAYERS.get(playerName).strength

def player_endurance(playerName):
    '''
    Returns the player's endurance attribute.
    '''

    return PLAYERS.get(playerName).endurance

def player_cleared(playerName):
    '''
    Returns the player's number of cleared mines.
    '''

    return PLAYERS.get(playerName).minesCompleted

def player_held(playerName):
    '''
    Returns the player's held resources.
    '''

    return PLAYERS.get(playerName).resHeld

def player_total(playerName):
    '''
    Return the player's total resource count.
    '''

    total = 0

    for item in player_held(playerName):
        total += int(item)

    return total

def has_golem(player):
    '''
    Returns whether or not the named player has a golem by searching for that
    player in the loaded golems.
    '''

    return GOLEMS.has_key(player)

def golem_living(player, timestamp):
    '''
    Requests golems status for the given player at the time of inquiry.

    (Don't use player_input here because this sometimes happens without player
    input)
    '''

    return GOLEMS[player].is_alive(timestamp)

def listPlayers():
    '''
    TODO: deprecate this with better game data handling

    gamedata = os.listdir(GAMEDIR)
    playerlist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "stats":
            playerlist.append(entry[0])
    return playerlist
    '''

    return PLAYERS.keys()

def listMines():
    '''
    TODO: deprecate this with better game data handline

    gamedata = os.listdir(GAMEDIR)
    minelist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "mine":
            minelist.append(entry[0])
    return minelist
    '''

    return MINES.keys()

def listDossiers():
    '''
    Return a list of player names for all current dossiers in the game
    directory.

    gamedata = os.listdir(GAMEDIR)
    playerlist = []

    for filename in gamedata:
        entry = os.path.basename(filename).split('.')
        if entry[-1] == "dossier":
            playerlist.append(entry[0])

    return playerlist
    '''

    playerlist = []

    for player in PLAYERS:
        if player.playing:
            playerlist.append(player.name)

    return playerlist

def golem_lifespan(player, timestamp):
    '''
    Requests the number of seconds left in that player's golem's life.
    '''

    return GOLEMS[player].remaining_life(timestamp)

def golem_shape(player):
    '''
    Requests the shape of the given player's golem.
    '''

    return GOLEMS[player].shape

def golem_stats(player):
    '''
    Requests the golem's stats, using legacy stat format (string list of
    resources).
    '''

    return GOLEMS[player].legacy_stats()

def golem_strength(player):
    '''
    Requests the strength of player's golem.
    '''

    return GOLEMS[player].strength

def golem_interval(player):
    '''
    Requests the strike interval of player's golem.
    '''

    return GOLEMS[player].interval

def golem_holdings(player):
    '''
    Requests a human-readable string of the golem's held resources.
    '''

    return GOLEMS[player].readable_holdings()

def golem_last_strike(player):
    '''
    Requests the timestamp of the golem's last strike.
    '''

    return GOLEMS[player].lastStrike

def mine_depletion(mineName):
    '''
    Returns the percentage depletion of a mine as an int (out of 100).
    '''

    mine = MINES[mineName]

    return int(100*float(mine.currentTotal)/float(mine.startingTotal))

def mine_total_res(mineName):
    '''
    Requests the total remaining resources in named mine.
    '''

    return MINES[mineName].currentTotal

def player_working_mines(player):
    '''
    Requests a list of names of mines that the player has permission to work on.
    '''

    return PLAYERS.get(player).minesOwned + PLAYERS.get(player).minesAssigned

## game actions

def create_dossier(playerName):
    '''
    Creates a new dossier for the listed player. If they don't already have a
    stats file, also create a stats file.

    if os.path.isfile(os.path.join(GAMEDIR, user+'.stats')):
        players.newDossier(user)
    else:
        players.newPlayer(user)

    Creates a new dossier for the named player. If that player has a previous
    stat file, just add to that; otherwise, create a new stat file with initial
    conditions.
    '''

    player = PLAYERS.get(playerName)

    if player:
        player.create()
    else:
        newPlayer = players.Player()
        newPlayer.set_name(playerName)
        PLAYERS.update({playerName:newPlayer})

def open_mine(playerName, rates="standardrates"):
    '''
    Opens a mine for the named player, given an optional mine rate file. Assumes
    that player has the permission to open a new mine, and decreases their
    current mine permission.
    '''

    newMine = mines.Mine()
    minename = newMine.create(playerName, rates)

    PLAYERS.get(playerName).add_mine(minename)

    MINES.update({minename:newMine})

    return minename.capitalize()

def create_golem(player_input, rawGolem):
    '''
    Attempts to create a golem with the given player input.  If golem creation
    succeeds, remove that res from the player's holdings and add the golem to
    the game objects.
    '''

    newGolem = golems.Golem()
    shapedGolem = golems.sift(rawGolem)

    try:
        print "making " + shapedGolem
        newGolem.create(player_input, shapedGolem)
    except BaseException:
        return False

    players.removeRes(player_input.nick, newGolem.legacy_stats())
    newGolem.save()
    GOLEMS.update({player_input.nick:newGolem})

    return newGolem

def player_strike(player, targetMineName):
    '''
    Requests a player strike at the target mine, and returns excavated
    resources.
    '''

    return players.strike(player, MINES[targetMineName])

def golem_strike(player, targetMine, elapsed):
    '''
    Requests that a golem belonging to named player strikes at the given target
    mine.
    '''

    return GOLEMS[player].strike(targetMine, elapsed)

def tick_golems(timestamp):
    '''
    Goes through golem ticks, and returns a list of player names with expired
    golems.
    '''

    deadGolems = []

    for golem in GOLEMS.values():
        print "updating "+ golem.owner +"'s golem at " + str(timestamp)

        if not golem.is_alive(timestamp): #process golem death
            print "golem expired"
            deadGolems.append(golem.owner)
        else:
            # process golem striking
            sinceLastStrike = int(timestamp) - golem.lastStrike
            print "next strike at "+str(golem.lastStrike) + str(golem.interval)

            if (sinceLastStrike >= golem.interval 
                 and len(players.getMines(golem.owner)) > 0):
                targetMine = players.getMines(golem.owner)[0]
                strikesCompleted = sinceLastStrike/golem.interval
                print "owed "+str(strikesCompleted)+" golem strikes"
                strikes = 0
                strikeTime = golem.lastStrike
                while strikes < strikesCompleted:
                    excavation = [0,0,0,0,0,0,0,0]
                    strikeTime += golem.interval

                    if MINES[targetMine].currentTotal > 0:
                        excavation = golem_strike(golem.owner, MINES[targetMine], strikeTime)
                        print excavation
                        #print "golemstrike"+ str(golems.strike(user, target))
                    else:
                        #set last strike for blank strike at empty mine
                        golem.lastStrike = strikeTime

                    strikes += 1

    return deadGolems

def golem_expire(player, timestamp):
    '''
    Facilitates the expirations of a golem for the given player.

    (Don't use player_input here because this sometimes happens without player
    input)
    '''

    if GOLEMS[player].is_alive(timestamp):
        return False
    else:
        deadGolem = GOLEMS.pop(player)
        drops = deadGolem.expire()

        # for legacy player acquireRes needs
        #dropList = drops.split(",")

        players.acquireRes(player, drops)

        return drops

## game setup

def initialize():
    '''
    Set up the game.
    '''

    gamedata = os.listdir(GAMEDIR)

    for filename in gamedata:
        entry = os.path.basename(filename).split('.')

        if entry[-1] == "golem":
            ## load golems
            incomingGolem = golems.Golem()
            GOLEMS.update({incomingGolem.load(entry[0]):incomingGolem})
        elif entry[-1] == "mine":
            ## load mines
            incomingMine = mines.Mine()
            MINES.update({incomingMine.load(entry[0]):incomingMine})

        elif entry[-1] == "player":
            ## load players
            incomingPlayer = players.Player()
            PLAYERS.update({incomingPlayer.load(entry[0]):incomingPlayer})

    print GOLEMS
    print MINES
    print PLAYERS

    return

initialize()
