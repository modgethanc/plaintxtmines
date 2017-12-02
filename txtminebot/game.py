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
    Returns the count of player's currently completed mines in this session.
    '''

    return PLAYERS.get(playerName).currentCompletion

def player_held(playerName):
    '''
    Returns the player's held resources.
    '''

    return PLAYERS.get(playerName).resHeld

def player_last_strike(playerName):
    '''
    Returns the player's last strike.
    '''

    return PLAYERS.get(playerName).lastStrike

def player_total(playerName):
    '''
    Return the player's total resource count.
    '''

    total = 0

    for item in player_held(playerName):
        total += int(item)

    return total

def player_current_fatigue(player_input):
    '''
    Performs a fatigue check and returns seconds remaining in the player's
    fatigue.
    '''

    return int(player_last_strike(player_input.nick)) + BASE_FATIGUE - min(9, player_endurance(player_input.nick)) - player_input.timestamp

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
    Return a list of current player names, even if they don't have dossiers.
    '''

    return PLAYERS.keys()

def listMines():
    '''
    Return a list of current mine names.
    '''

    return MINES.keys()

def list_dossiers():
    '''
    Return a list of player names for all current dossiers in the game
    directory.
    '''

    playerlist = []

    for player in PLAYERS:
        if PLAYERS.get(player).playing:
            playerlist.append(player)

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

    if not MINES.get(mineName):
        return 0
    else:
        return MINES.get(mineName).currentTotal

def player_working_mines(player):
    '''
    Requests a list of names of mines that the player has permission to work on.
    '''

    return PLAYERS.get(player).minesOwned + PLAYERS.get(player).minesAssigned

def can_afford(playerName, cost):
    '''
    Checks if named player can afford to spend the specified resources.
    '''

    held = player_held(playerName)

    for index, res in enumerate(cost):
        if held[index] < int(res):
            return False

    return True

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

    player_remove_res(player_input.nick, newGolem.legacy_stats())
    newGolem.save()
    GOLEMS.update({player_input.nick:newGolem})

    return newGolem

def player_strike_attempt(player_input):
    '''
    Processes a strike attempt for fatigue management. If the player has
    outstanding fatigue, perform fatigue increase and return remaining fatigue
    time in seconds. Otherwise, return 0.
    '''

    fatigue = player_current_fatigue(player_input)

    if fatigue > 0:
        # todo: put fatigue increase here
        player = PLAYERS.get(player_input.nick)
        '''
        fatigue = min(fatigue * 2, 7200)
        nextStrike = int(player_input.timestamp) + fatigue - (game.BASE_FATIGUE - players.getEndurance(player_input.nick))# still hardcoded bs
        response.append({"msg":"You're still tired from your last attempt.  You'll be ready again in "+str(fatigue)+" seconds.  Please take breaks to prevent fatigue; rushing will only lengthen your recovery.", "channel":player_input.nick})
        '''
        player.save()
        return fatigue
    else:
        return 0

def player_strike(player_input, mineName):
    '''
    Processes a player's strike at the target mine, and returns excavated
    resources.
    '''

    player = PLAYERS.get(player_input.nick)
    targetMine = MINES.get(mineName)

    # perform strike
    baseDepth = 3
    strikeDepth = baseDepth * player.strength
    excavation = targetMine.excavate(strikeDepth)

    # acquire resources
    player.acquire(excavation)

    # clean up

    player.strikeCount += 1
    player.lifetimeStrikes += 1
    player.lastStrike = player_input.timestamp
    player.save()

    return excavation

def player_strength_roll(playerName):
    '''
    Perform a dice roll for player strength increase.
    '''

    player = PLAYERS.get(playerName)

    if random.randrange(0,99) < 3:
        player.strength += 1
        player.save()
        return True
    else:
        return False

def player_remove_res(playerName, cost):
    '''
    Removes given resources from player's held. Assumes player can afford it.
    '''

    player = PLAYERS.get(playerName)
    held = player_held(playerName)

    for index, res in enumerate(cost):
        held[index] -= int(res)

    player.resHeld = held
    player.save()

def player_finish_mine(playerName, mineName):
    '''
    Processes giving player credit for finishing the mine.
    '''
    player = PLAYERS.get(playerName)

    player.minesOwned.remove(mineName)
    player.minesCompleted.append(mineName)
    player.currentCompletion += 1
    player.lifetimeCompleted += 1
    player.minesAvailable += 1
    player.endurance += 1

    player.save()

    mine_clear(mineName)

def mine_clear(mineName):
    '''
    Performs mine clearing actions.
    '''

    targetMine = MINES.get(mineName)

    if targetMine.currentTotal == 0:
        deadMine = MINES.pop(mineName)
        ## hardcoded
        os.renames("../data/"+mineName+".mine", "../data/mine-archive/"+mineName+".mine")

def player_grovel(player_input):
    '''
    Process player groveling.
    '''

    player = PLAYERS.get(player_input.nick)
    player.lifetimeGrovels += 1
    player.grovelCount += 1
    player.save()

def golem_strike(playerName, targetMine, elapsed):
    '''
    Requests that a golem belonging to named player strikes at the given target
    mine.
    '''
    golem = GOLEMS.get(playerName)

    # perform strike
    baseDepth = 3
    strikeDepth = baseDepth * golem.strength
    excavation = MINES.get(targetMine).excavate(strikeDepth)

    # acquire resources
    golem.acquire(excavation)

    # clean up
    golem.lastStrike = elapsed
    golem.save()

    return excavation

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
                 and len(player_working_mines(golem.owner)) > 0):
                targetMine = player_working_mines(golem.owner)[0]
                strikesCompleted = sinceLastStrike/golem.interval
                print "owed "+str(strikesCompleted)+" golem strikes"
                strikes = 0
                strikeTime = golem.lastStrike
                while strikes < strikesCompleted:
                    excavation = [0,0,0,0,0,0,0,0]
                    strikeTime += golem.interval

                    if MINES[targetMine].currentTotal > 0:
                        excavation = golem_strike(golem.owner, targetMine, strikeTime)
                        print excavation
                    else:
                        #set last strike for blank strike at empty mine
                        golem.lastStrike = strikeTime

                    strikes += 1

    return deadGolems

def golem_expire(playerName, timestamp):
    '''
    Facilitates the expirations of a golem for the given player.

    (Don't use player_input here because this sometimes happens without player
    input)
    '''

    if GOLEMS[playerName].is_alive(timestamp):
        return False
    else:
        deadGolem = GOLEMS.pop(playerName)
        drops = deadGolem.expire()

        # for legacy player acquireRes needs
        #dropList = drops.split(",")

        PLAYERS.get(playerName).acquire(drops)

        return drops

## helpers

def pretty_reslist(reslist):
    '''
    Takes an int list representation of resources and formats it visually. If
    there's nothing there, display rubble; if there's too much, display 'lots'.

    Assumes the standard convention for reslist:
        reslist[0]: ~
        reslist[1]: @
        reslist[2]: #
        reslist[3]: &
        reslist[4]: *
        reslist[5]: [
        reslist[6]: ]
        reslist[7]: ^
    '''

    total = 0

    for x in reslist:
        total += int(x)

    if total == 0:
        return "nothing but rubble."

    if total > 100:
        return "a lot of resources!"

    mined = ''
    y = 0
    for x in reslist:
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

## game setup

def initialize():
    '''
    Set up the game.
    '''

    gamedata = os.listdir(GAMEDIR)

    for filename in gamedata:
        entry = os.path.basename(filename).split('.')

        if not entry[0]:
            # skip blank files
            continue

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
