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
    completionCount: int of number of mines cleared on this dossier
    minesAvailable: int of how many mines player can currently open
    resHeld: 8-item int array of currently held resources (*)
    grovelCount: int of current grovel count
    strikeCount: int of current strike count
    playing: boolean for if player has a dossier

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

    def __init__(self):
        '''
        Initial player conditions.
        '''

        # stats
        self.name = ""
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
        self.currentCompletion = 0
        self.minesAvailable = 1
        self.resHeld = [0,0,0,0,0,0,0,0]
        self.grovelCount = 0
        self.strikeCount = 0
        self.playing = True

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
            "current completion count": self.currentCompletion,
            "mines available": self.minesAvailable,
            "res held": self.resHeld,
            "grovel count": self.grovelCount,
            "strike count": self.strikeCount,
            "playing": self.playing
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
        self.currentCompletion = playerData.get("current completion count")
        self.minesAvailable = playerData.get("mines available")
        self.resHeld = playerData.get("res held")
        self.grovelCount = playerData.get("grovel count")
        self.strikeCount = playerData.get("strike count")
        self.playing = playerData.get("playing")

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

    def set_name(self, playerName):
        '''
        Sets the name for this player, and adds name to alias list.
        '''

        self.name = playerName
        self.aliases.append(playerName)

        return self.name

    ## helper functions

    def add_mine(self, minename):
        '''
        Adds the named mine to this player's list of owned mines, then
        decrements available mines. Saves to disk afterwards.
        '''

        self.minesOwned.append(minename)
        self.minesAvailable -= 1
        self.save()
