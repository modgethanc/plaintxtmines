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

## globals

## speaking functions

def addressed(bot, channel, nick, time, msg, interface):
    '''
    Returns responses to something said in a channel when directly addressed.
    Every time this bot is addressed, this should be called.
    '''

    response = []

    response.append("hi")

    return response

def said(bot, channel, nick, time, msg, interface):
    '''
    Returns responses to something said in a channel, when not directly
    addressed. This should catch everything that addressed() misses.
    '''

    response = []

    if msg.find("!info") == 0: # !info
        response.append("I am the mining assistant, here to facilitate your ventures by order of the empress.  My lieutenant is "+bot.ADMIN+", who can handle inquiries beyond my availability.")
        response.append("Commands: !init, !open, !mines, !strike {mine}, !report, !stats, !fatigue, !golem {resources}, !grovel, !rankings, !info.\n")
        #ircsock.send("PRIVMSG "+ channel +" :"+ user + ": I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike {mine}, !report, !stats, !fatigue, !golem {resources}, !grovel, !rankings, !info.\n")

    """   LINE OF DEATH

    elif msg.find(":!"+COMMANDS[0]) != -1: # !init
        if isPlaying(user):
            ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You already have a dossier in my records, friend.\n")
        else:
            newPlayer(channel, user)

    elif msg.find(":!"+COMMANDS[1]) != -1: # !open
        if isPlaying(user):
            if players.getAvailableMines(user) > 0:
                 newMine(channel, user)
            else:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You do not have permission to open a new mine at the moment, friend.  Perhaps in the future, the empress will allow you further ventures.\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I can't open a mine for you until you have a dossier in my records, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[2]) != -1: # !mines
        if isPlaying(user):
            if len(players.getMines(user)) == 0:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else:
                ircsock.send("PRIVMSG "+channel+" :" + user + ": "+mineListFormatted(msg, channel, user)+"\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[9]) != -1: # !stats
        if isPlaying(user):
            ircsock.send("PRIVMSG "+channel+" :" + user + ": "+statsFormatted(channel, user)+"\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[11]) != -1: # !res
        if isPlaying(user):
            ircsock.send("PRIVMSG "+channel+" :" + user + ": "+resourcesFormatted(channel, user)+"\n")
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[3]) != -1: # !strike
        if isPlaying(user):
            if len(players.getMines(user)) == 0:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else:
                strike(msg, channel, user, time)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[5]) != -1: # !fatigue
        if isPlaying(user):
            fatigue(msg, channel, user, time)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[6]) != -1: # !grovel
        if isPlaying(user):
            if random.randrange(1,100) < 30:
                ircsock.send("PRIVMSG "+ channel + " :" + user + ": The empress is indisposed at the moment.  Perhaps she will be open to receiving visitors in the future.  Until then, I'd encourage you to work hard and earn her pleasure.\n")
            else:
                grovel(msg, channel, user, time)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I advise against groveling unless you're in my records, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[4]) != -1: # !report
        if isPlaying(user):
            report(msg, channel, user, time)
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[10]) != -1: # !golem
        if isPlaying(user):
            parse = msg.split("!"+COMMANDS[10])
            if parse[1] == '': #no arguments
                if hasGolem(user):
                    ircsock.send("PRIVMSG "+ channel + " :" + user + ": "+golemStats(channel, user, time)+".\n")
                    ircsock.send("PRIVMSG "+ channel + " :" + user + ": It's holding the following resources: "+golems.heldFormatted(user)+".\n")
                    #ircsock.send("PRIVMSG "+ channel + " :" + user + ": "+golems.getShape(user)+" is hard at work!  It'll last for another "+p.no("second", golems.getLifeRemaining(user, time))+".\n")
                else:
                    ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have a golem working for you, friend.  Create one with '!golem {resources}'.\n")
            else: # check for mines??
                newGolem(channel, user, time, parse[1].lstrip())
        else:
            ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[8]) != -1: # !rankings
        rankings(msg, channel, user)
    """
    return response

## command handlers

## helper functions

def tick(now):
    '''
    Called by IRC whenever a second ellapses.

    TODO: Put golem updating here!
    '''

    return
