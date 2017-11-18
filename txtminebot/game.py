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

def is_playing(user):
    '''
    Returns whether or not the named user has a dossier on file.
    '''

    return os.path.isfile(os.path.join(GAMEDIR,user+'.dossier'))

def is_mine(mine):
    '''
    Returns whether or not the named mine exists.
    '''
    return os.path.isfile(os.path.join(GAMEDIR,mine+'.mine'))

def has_golem(user):
    '''
    Returns whether or not the named player has a golem.
    '''
    return os.path.isfile(os.path.join(GAMEDIR,user+'.golem'))

def listPlayers():
    '''
    TODO: deprecate this with better game data handline
    '''

    gamedata = os.listdir(GAMEDIR)
    playerlist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "stats":
            playerlist.append(entry[0])
    return playerlist

def listGolems():
    '''
    TODO: deprecate this with better game data handline
    '''

    gamedata = os.listdir(GAMEDIR)
    golemlist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "golem":
            golemlist.append(entry[0])
    return golemlist

def listMines():
    '''
    TODO: deprecate this with better game data handline
    '''

    gamedata = os.listdir(GAMEDIR)
    minelist = []
    for x in gamedata:
        entry = os.path.basename(x).split('.')
        if entry[-1] == "mine":
            minelist.append(entry[0])
    return minelist

def listDossiers():
    '''
    Return a list of player names for all current dossiers in the game
    directory.
    '''

    gamedata = os.listdir(GAMEDIR)
    playerlist = []

    for filename in gamedata:
        entry = os.path.basename(filename).split('.')
        if entry[-1] == "dossier":
            playerlist.append(entry[0])

    return playerlist

def golem_lifespan(player, timestamp):
    '''
    Returns the number of seconds left in that player's golem's life.
    '''

    return GOLEMS[player].remaining_life(timestamp)

## game actions

def create_dossier(user):
    '''
    Creates a new dossier for the listed player. If they don't already have a
    stats file, also create a stats file.
    '''

    if os.path.isfile(os.path.join(GAMEDIR, user+'.stats')):
        players.newDossier(user)
    else:
        players.newPlayer(user)

def open_mine(user, rates="standardrates"):
    '''
    Opens a mine for the named user, given an optional mine rate file. Assumes
    that player has the permission to open a new mine, and decreases their
    current mine permission.
    '''

    mine = players.newMine(user, "standardrates").capitalize()
    players.decAvailableMines(user)

    return mine

def create_golem(player_input, rawGolem):
    """
    Attempts to create a golem with the given player input.  If golem creation
    succeeds, remove that res from the player's holdings and add the golem to
    the game objects.
    """

    newGolem = Golem()
    shapedGolem = golems.sift(rawGolem)

    try:
        newGolem.create(player_input, shapedGolem)
    except BaseException:
        return False

    players.removeRes(user, golems.getStats(user))
    GOLEMS.update(newGolem)

    return newGolem

## game setup

def initialize():
    '''
    Set up the game.
    '''

    return
