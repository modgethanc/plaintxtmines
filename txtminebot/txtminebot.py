#!/usr/bin/python
'''
This is the core response generator for txtminebot.

All speaking modules should return a list of strings that correspond to an
appropriate response. Generating that response goes to helper modules. Control
game state from here.

Currently, these responses are designed for use with the IRC class in
controllers.py. This may be modified for support with other interfaces
eventually.

plaintxtmines is a text-based multiplayer mining simulator. For more
information, see the full repository:

https://github.com/modgethanc/plaintxtmines
'''

__author__ = "Vincent Zeng (hvincent@modgethanc.com)"

import os
import random
import inflect
import time
from datetime import datetime

import formatter
import game

import players
import golems
import mines
import empress

def reset():
    '''
    Reload game dependencies.
    '''

    reload(game)
    game.reset()

## globals

p = inflect.engine()
INTERP = []
for x in open("lang/interp.txt"):
    INTERP.append(x.rstrip())

## speaking functions

def addressed(player_input):
    '''
    Returns responses to something said in a channel when directly addressed.
    If the thing said in a channel is a command, defer to the command
    processing in said(); otherwise, return a fallthrough filler statement.

    Every time this bot is addressed, this should be called.
    '''

    response = []

    randoms = ["Sorry, friend, I'm not sure how to help you here.", "Check with my lieutenant, "+player_input.bot.ADMIN+", if you need an urgent response.", "Perhaps you should just focus on your mining duties."]

    saids = said(player_input)

    if not saids:
        time.sleep(1)
        response.append(random.choice(randoms))
        return response
    else:
        return saids


def said(player_input):
    '''
    Returns responses to something said in a channel, when not directly
    addressed.

    This should be part of the main listening loop to catch commands.
    '''

    response = []

    msg = player_input.msg

    if msg.find("!info") == 0 or msg.find("!help") == 0:
        response.extend(ch_info(player_input))
    elif msg.find("!init") == 0:
        response.extend(ch_init(player_input))
    elif msg.find("!open") == 0:
        response.extend(ch_open(player_input))
    elif msg.find("!mines") == 0:
        response.extend(ch_mines(player_input))
    elif msg.find("!stats") == 0:
        response.extend(ch_stats(player_input))
    elif msg.find("!strike") == 0:
        response.extend(ch_strike(player_input))
    elif msg.find("!res") == 0:
        response.extend(ch_res(player_input))
    elif msg.find("!fatigue") == 0:
        response.extend(ch_fatigue(player_input))
    elif msg.find("!grovel") == 0:
        response.extend(ch_grovel(player_input))
    elif msg.find("!report") == 0:
        response.extend(ch_report(player_input))
    elif msg.find("!golem") == 0:
        response.extend(ch_golem(player_input))
    elif msg.find("!rankings") == 0: # !rankings
        response.extend(rankings())

    return response

## command handlers

def ch_info(player_input):
    '''
    Handles responses to !info command.
    '''

    response = []

    response.append("I am the mining assistant, here to facilitate your ventures by order of the empress.  My lieutenant is "+player_input.bot.ADMIN+", who may be able to handle inquiries beyond my availability.")
    response.append("Commands: !init, !open, !mines, !strike {mine}, !report, !stats, !fatigue, !golem {resources}, !grovel, !rankings, !info.")

    return response

def ch_init(player_input):
    '''
    Handles responses to !init command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        response.append("You already have a dossier in my records, friend.")
    else:
        game.create_dossier(player_input.nick)

        response.append("New dossier created.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with '!open'.")

    return response

def ch_open(player_input, rate = "standardrates"):
    '''
    Handlers response to !open command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        if players.getAvailableMines(player_input.nick) > 0:
             newMine = game.open_mine(player_input.nick, rate)
             response.append("Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+newMine+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts, and begin with an enthusiastic '!strike'.")
        else:
            response.append("You do not have permission to open a new mine at the moment, friend.  Perhaps in the future, the empress will allow you further ventures.")
    else:
        response.append("I can't open a mine for you until you have a dossier in my records, friend.  Request a new dossier with '!init'.")

    return response

def ch_mines(player_input):
    '''
    Handles responses to !mines command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        if len(players.getMines(player_input.nick)) == 0:
            response.append("You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.")
        else:
            response.append(mineListFormatted(player_input.nick))
    else:
        response.append("I don't have anything on file for you, friend.  Request a new dossier with '!init'.")

    return response

def ch_stats(player_input):
    '''
    Handles response to !stats command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        response.append(statsFormatted(player_input.nick))
    else:
        response.append("I don't know anything about you, friend.  Request a new dossier with '!init'.")

    return response

def ch_strike(player_input):
    '''
    Handles response to !strike command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        if len(players.getMines(player_input.nick)) == 0:
            response.append("You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.")
        else:
            response.extend(strike(player_input))
    else:
        response.append("I don't have anything on file for you, friend.  Request a new dossier with '!init'.")

    return response

def ch_res(player_input):
    '''
    Handles response to !res command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        response.append(resourcesFormatted(player_input.nick))
    else:
        response.append("I don't know anything about you, friend.  Request a new dossier with '!init'.")

    return response

def ch_fatigue(player_input):
    '''
    Handles response to !fatigue command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        response.append(fatigue(player_input))
    else:
        response.append("I don't know anything about you, friend.  Request a new dossier with '!init'.")

    return response

def ch_grovel(player_input):
    '''
    Handles response to !grovel command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        if random.randrange(1,100) < 30:
            response.append("The empress is indisposed at the moment.  Perhaps she will be open to receiving visitors in the future.  Until then, I'd encourage you to work hard and earn her pleasure.")
        else:
            response.append(grovel(player_input))
    else:
        response.append("I advise against groveling unless you're in my records, friend.  Request a new dossier with '!init'.")

    return response

def ch_report(player_input):
    '''
    Handles response to !report command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        response.extend(report(player_input))
    else:
        response.append("I don't have anything on file for you, friend.  Request a new dossier with '!init'.")

    return response

def ch_golem(player_input):
    '''
    Handles response to !golem command.
    '''

    response = []

    if game.is_playing(player_input.nick):
        parse = player_input.msg.split("!golem")
        if parse[1] == '': #no arguments
            if game.has_golem(player_input.nick):
                response.append(golemStats(player_input))
                response.append("It's holding the following resources: "+golems.heldFormatted(player_input.nick))
            else:
                response.append("You don't have a golem working for you, friend.  Create one with '!golem {resources}'.")
        else: # check for mines??
            response.append(newGolem(player_input.nick, player_input.timestamp, parse[1].lstrip()))
    else:
        response.append("I can't help you make a golem without any information on file for you, friend.  Request a new dossier with '!init'.")

    return response

class CommandHandler():
    '''
    Just dumping this structure here so I don't lose it; stubs to make more
    graceful command handling.
    '''

    def __init__(self):
        self.TRIGGERS = ["command", "alternate command"]
        self.UNKNOWN = "unknown player response"

    def catch_command(self, bot, channel, nick, timestamp, msg, interface):
        '''
        Command-catching wrapper.
        '''

        response = []

        response.extend(self.handle(
            self, bot, channel, nick, timestamp, msg, interface))

        return response

    def handle(self, bot, channel, nick, timestamp, msg, interface):
        '''
        Override this.
        '''

        return


## legacy gameplay functions

def newGolem(user, timestamp, golemstring):
    '''
    Runs checks for building a golem.

    Builds a new golem for the given user, with a given string.
    '''

    if game.has_golem(user):
        return "You can't make a new golem until your old golem finishes working!  It'll be ready in "+formatter.prettyTime(game.golem_lifespan(user, timestamp))
    else:
        if golems.calcStrength(golems.parse(golemstring)) > 0:
            if players.canAfford(user, golems.parse(golemstring)):
                rawGolem = list(golemstring)
                maxgolem = (players.getStrength(user)*3.5)
                if len(rawGolem) > maxgolem:
                  return "You're not strong enough to construct a golem that big, friend.  The most you can use is "+p.no("resource", maxgolem)
                else:

                  if game.create_golem(player_input, rawGolem):
                      logGolem(user)

                      golemstats = players.printExcavation(golems.getStats(user))+ " has been removed from your holdings.  Your new golem will last for "+formatter.prettyTime(game.golem_lifespan(user, timestamp))+".  Once it expires, you can gather all the resources it harvested for you.  "
                      golemstats += "It can excavate up to "+p.no("resource", golems.getStrength(user))+" per strike, and strikes every "+p.no("second", golems.getInterval(user))+"."
                  else:
                      golemstats = "Something went wrong when you tried to construct that golem.  I'm sorry, friend; why don't you try a different shape?"

                  return golemstats

            else:
                return "You don't have the resources to make that golem, friend."
        else:
            return "That's not a valid golem, friend.  The golem has to be constructed from resources you've acquired."

def logGolem(user):
      golemarchive = open("../data/golems.txt", 'a')
      golemtext = golems.getShape(user) + "\t"
      golemtext += str(golems.getStrength(user)) + "/" + str(golems.getInterval(user)) + "\t"
      golemtext += " ("+user+" on "+datetime.now().date().__str__()+")"
      golemarchive.write(golemtext+"\n")
      golemarchive.close()

def updateGolems(timestamp):
    response = []

    for user in game.listGolems():
        strikeDiff = int(timestamp) - golems.getLastStrike(user)
        interval = golems.getInterval(user)

        if strikeDiff >= interval and len(players.getMines(user)) > 0: # golem strike
            target = players.getMines(user)[0]
            strikeCount = strikeDiff/interval
            i = 0
            elapsed = golems.getLastStrike(user)
            while i < strikeCount:
                if mines.getTotal(target) > 0:
                    print "golemstrike"+ str(golems.strike(user, target))
                elapsed += interval
                i += 1

            golems.updateLastStrike(user, elapsed)

        if int(timestamp) > golems.getDeath(user): # golem death
            golem = golems.getShape(user)
            mined = players.printExcavation(golems.expire(user))
            golemgrave = "in front of you"
            if len(players.getMines(user)) > 0:
                golemgrave = "inside of "+players.getMines(user)[0].capitalize()

            """TODO: figure out how to make tick speak appropriately! old
            response below:

            ircsock.send("PRIVMSG "+ x +" :"+golem+" crumbles to dust "+golemgrave+" and leaves a wake of "+mined+"\n")
            """
            response.append({"msg":golem+" crumbles to dust "+golemgrave+" and leaves a wake of "+mined, "channel":user})

    return response

def strike(player_input):
    '''
    Process all strike actions, returning username as channel so these responses
    always go to PM.
    '''

    response = []

    selected = ""
    mineList = players.getMines(player_input.nick)
    target = mineList[0] #autotarget first mine

    inputs = player_input.msg.split("!strike")
    if len(inputs[-1].split(" ")) > 1:
        selected = inputs[-1].split(" ")[+1].lower()

    #check for targetted mine
    if selected != "":
        if mineList.count(selected) == 0:
            response.append({"msg":"That's not a mine you're working on, friend.  Feel free to just '!strike' to work on the same mine you last targetted.", "channel":player_input.nick})
            return response

        elif target != selected:
            target = selected
            mineList.remove(target)    #bump this to the top of the minelist
            mineList.insert(0, target)

    fatigue = players.fatigueCheck(player_input.nick, player_input.timestamp)
    if fatigue > 0:
        fatigue = min(fatigue * 2, 7200)
        timestamp = int(player_input.timestamp) + fatigue - (game.BASE_FATIGUE - players.getEndurance(player_input.nick))# still hardcoded bs
        response.append({"msg":"You're still tired from your last attempt.  You'll be ready again in "+str(fatigue)+" seconds.  Please take breaks to prevent fatigue; rushing will only lengthen your recovery.", "channel":player_input.nick})

    else: # actual mining actions
        emptyMines = []
        status = players.incStrikes(player_input.nick)
        excavation = players.strike(player_input.nick, target)
        mined = players.printExcavation(players.acquireRes(player_input.nick, excavation))
        response.append({"msg":"\x03" + random.choice(['4', '8', '9', '11', '12', '13'])+random.choice(['WHAM! ', 'CRASH!', 'BANG! ', 'KLANG!', 'CLUNK!', 'PLINK!', 'DINK! '])+"\x03  "+status+"You struck at " + target.capitalize() +" and excavated "+mined, "channel":player_input.nick})

        if mines.getTotal(target) == 0:
            emptyMines.append(target)
            players.incCleared(player_input.nick)
            players.incEndurance(player_input.nick)
            players.incAvailableMines(player_input.nick)

            response.append({"msg":"As you clear the last of the rubble from "+target.capitalize()+", a mysterious wisp of smoke rises from the bottom.  You feel slightly rejuvinated when you breathe it in.", "channel":player_input.nick})
            response.append({"msg":target.capitalize()+" is now empty.  The empress shall be pleased with your progress.  I'll remove it from your dossier now; feel free to request a new mine.", "channel":player_input.nick})
            response.append({"msg":"There's a distant rumbling as "+player_input.nick+" clears the last few resources from "+target.capitalize()+".", "channel":"MAIN", "nick":False})

        for deadMine in emptyMines:
            mineList.remove(deadMine)

    players.updateOwned(player_input.nick, mineList)
    players.updateLastStrike(player_input.nick, player_input.timestamp)

    return response

def report(player_input):
    '''
    Calls all the components of a player report and stitches them together.
    '''

    response = []

    if len(players.getMines(player_input.nick)) > 0:
        response.append(mineListFormatted(player_input.nick))

    response.append(resourcesFormatted(player_input.nick))

    if game.has_golem(player_input.nick):
        response.append(golemStats(player_input))

    response.append(statsFormatted(player_input.nick))

    return response

def grovel(player_input):
    '''
    Handles groveling.
    '''

    players.incGrovel(player_input.nick)
    statement = '\x03' + random.choice(['4', '8', '9', '11', '12', '13']) + str(empress.speak()).rstrip()

    return "The empress "+random.choice(['says', 'states', 'replies', 'snaps', 'mumbles', 'mutters'])+", \""+statement+"\x03\"  "+random.choice(INTERP)

def stirke(msg, channel, user, timestamp): #hazelnut memorial disfeature
    a = 0

def fatigue(player_input):
    '''
    Returns remaining fatigue for a player.

    ~krowbar memorial feature
    '''

    fatigue = players.fatigueCheck(player_input.nick, player_input.timestamp)
    if fatigue > 0:
        return "You'll be ready to strike again in "+formatter.prettyTime(fatigue)+".  Please rest patiently so you do not stress your body."
    else:
        return "You're refreshed and ready to mine.  Take care to not overwork; a broken body is no use to the empress."

def mineListFormatted(user):
    '''
    Returns a nicely formatted list of mines for IRC printing from the given
    user's dossier.
    '''

    plural = ''
    if len(players.getMines(user)) > 0:
        plural = 's'

    prejoin = []

    mineList = players.getMines(user)
    rawlist = []
    for x in mineList:
        depletion = int(100*float(mines.getTotal(x))/float(mines.getStarting(x)))
        prefix = ''

        if mineList.index(x) == 0: # currently targetted
            prefix= '>'

        rawlist.append([prefix+x.capitalize(), depletion])

    rawlist.sort(key=lambda entry:int(entry[1]))

    for x in rawlist:
        depletion = x[1]

        color = ''
        if depletion > 98:
            color += "\x0311"
        elif depletion > 90:
            color += "\x0309"
        elif depletion > 49:
            color += "\x0308"
        elif depletion > 24:
            color += "\x0307"
        elif depletion > 9:
            color += "\x0304"
        else:
            color += "\x0305"

        prejoin.append(x[0] + " (" + color + str(depletion) + "%\x03)")

    return "You're working on the following mine"+plural+": "+", ".join(prejoin)

def resourcesFormatted(user):
    return "You're holding the following resources: "+players.heldFormatted(user)

def statsFormatted(user):
    stats = "You can mine up to "+str(3*players.getStrength(user))+" units every strike, and strike every "+p.no("second", max(1, game.BASE_FATIGUE - players.getEndurance(user)))+" without experiencing fatigue.  "
    plural = 's'
    if players.getClearedCount(user) == 1: plural = ''
    stats += "You've cleared "+str(players.getClearedCount(user))+" mine"+plural+".  "
    stats += "You can make a golem with up to "+p.no("resource", int(3.5*players.getStrength(user)))+".  "
    stats += "Please continue working hard for the empress!"

    return stats

def golemStats(player_input):
    '''
    Helper function to construct golem stats.
    '''

    status = golems.getShape(player_input.nick)+" is hard at work!  "
    status += "It can excavate up to "+p.no("resource", golems.getStrength(player_input.nick))+" per strike, and strikes every "+p.no("second", golems.getInterval(player_input.nick))+".  It'll last another "+formatter.prettyTime(game.golem_lifespan(player_input.nick, player_input.timestamp))

    return status

def rankings():
    '''
    Calculates rankings by resources held.
    '''

    response = []
    dossiers = game.listDossiers()

    records = []
    for x in dossiers:
        records.append([x, str(players.getHeldTotal(x))])

    records.sort(key=lambda entry:int(entry[1]), reverse=True)
    response.append("The wealthiest citizens are:")

    for x in range (0, min(5, len(records))):
        entry = records[x]
        response.append(entry[0] + " with " + entry[1] + " units")

    return response

## helper functions

def tick(now):
    '''
    Called by IRC whenever a second ellapses.

    TODO: Put golem updating here!
    '''

    response = []

    response.extend(updateGolems(now))

    # debugging ticks below:
    #response.append({"msg":"tick "+str(now), "channel":"hvincent"})

    return response

print "arnold loaded."
