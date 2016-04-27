#!/usr/bin/python

import inflect
import os
import json
import random
import util
import game
import imp

p = inflect.engine()
CONFIG = os.path.join("config")
DATA = os.path.join("..", "data")
CMD_DEF = "commands.json"
LANG_DEF = "lang.json"
COMMANDS = {}
LANG = {}
STRANGER = ""
UNIMP = "I'm sorry, friend, but this function is currently disabled.  I expect it to return with an improved ability to support your mining ventures."

IRC = False
p.defnoun("mine", "mines")

## file i/o

def init():
    # calls all the loading methods

    global STRANGER

    imp.reload(game)
    game.init()

    load_lang()
    load_cmd()

    STRANGER = "I don't know who you are, stranger.  If you'd like to enlist your talents in the name of the empress, you may do so with \"!join PROVINCE\".  "+provinces()

def load_lang(langfile=os.path.join(CONFIG, LANG_DEF)):
    # takes a langfile and loads into memory

    global LANG

    infile = open(langfile, "r")
    LANG = json.load(infile)
    infile.close()

def load_cmd(commandfile=os.path.join(CONFIG, CMD_DEF)):
    # takes a commandfile and loads into memory

    global COMMANDS

    infile = open(commandfile, "r")
    COMMANDS = json.load(infile)
    infile.close()

def save():
    # calls game save

    game.save()

def playerID(name):
    # returns playerID of name, or none

    return game.is_playing(name)

## base handler functions

def commands(playerID, user, now, inputs):
    # returns a list of currently valid commands

    msg = ""

    for cmd in COMMANDS:
        if IRC:
            msg += util.irc_rainbow("!"+cmd+" ")
        else:
            msg += "!"+cmd+" "

    return [msg]

def join(playerID, user, now, inputs):
    # creates a new player

    response = []

    if playerID:
        response.append("You are already registered, my friend.")
    else:
        if len(inputs) < 2:
            response.append("You must declare a province to which you call home, stranger.  "+provinces())
        else:
            zoneID = game.match_province(inputs[1])
            newID, hasSpace, zoneExists = game.new_player(make_player(user, now, zoneID))
            if newID:
                print("new player: "+newID)
                response.append("Your citizenship of the province of "+game.get_data("world", zoneID, "name")+" is now acknowledged.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with \"!new\".")
            else:
                response.append(failed_join(hasSpace, zoneExists))

    return response

def new(playerID, user, time, inputs):
    # new mine creation

    response = []

    mineID, hasSpace, mayCreate = game.new_mine(playerID)

    if mineID:
        minename = game.get_data("mines", mineID, "name")
        response.append("Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+minename+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts, and begin with an enthusiastic \'!strike\".")
    else:
        response.append(failed_new(hasSpace, mayCreate))

    return response

def grovel(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def mines(playerID, user, time, inputs):
    # returns formatted list of mines for playerID

    response = []

    response.append(player_mines(playerID))

    return response

def info(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def stats(playerID, user, now, inputs):
    # calls stat formatter and returns it

    response = []

    response.extend(player_stats(playerID, now))

    return response

def fatigue(playerID, user, now, inputs):
    # calls fatigue formatter and returns it

    response = []

    response.append(player_fatigue(playerID, now))

    return response

def report(playerID, user, now, inputs):
    # calls each formatter for full player details

    response = []

    response.append(player_mines(playerID))
    response.append(player_res(playerID))
    response.extend(player_stats(playerID, now))
    response.append(player_favors(playerID))
    response.append("Please continue working hard for the empress!")

    return response

def strike(playerID, user, now, inputs):

    response = []

    if len(game.list_mines(playerID)) < 1:
        response.append("I'm sorry, friend, but you have no mines at which to strike.  Open a new mine with \"!new\",")
        return response

    if len(inputs) < 2:
        targetID = game.get_data("players", playerID, "targetted")
    else:
        targetID = game.is_mine(inputs[1])
        if not targetID:
            targetID = game.get_data("players", playerID, "targetted")

    fatigue, permitted, depleted, reslist, lvlUp = game.strike(playerID, targetID, now)

    mineName = game.get_data("mines", targetID, "name")

    if reslist:
        lvlMsg = ""
        if lvlUp:
            lvlMsg = "  You're feeling strong!"
        if IRC:
            wham = util.irc_rainbow(random.choice(LANG.get("wham")))
        else:
<<<<<<< HEAD
            say(channel, "That's not a valid golem, friend.  The golem has to be constructed from resources you've acquired.", user)

def updateGolems(time):
    for x in game.listGolems():
        #if int(time) > golems.getDeath(x): # golem death
        if golems.getSize(x) == 0: # golem death
            golemDie(x, time)
            continue

        strikeDiff = int(time) - golems.getLastStrike(x)
        interval = golems.getInterval(x)

        if strikeDiff >= interval and len(players.getMines(x)) > 0: # golem strike
            target = players.getMines(x)[0]
            strikeCount = strikeDiff/interval
            i = 0
            elapsed = golems.getLastStrike(x)
            dead = False
            while i < strikeCount:
                if dead:
                    break
                if mines.getTotal(target) > 0:
                    if golems.getSize(x) > 0:
                        #print "golemstrike"+ str(golems.strike(x, target))
                        golems.strike(x, target)
                    else:
                        dead = golemDie(x, time)
                    elapsed += interval
                    i += 1
            if not dead:
                golems.updateLastStrike(x, elapsed)

def golemDie(user, time):
    life = formatter.prettyTime(golems.getLife(user, time))
    mined = game.itemizeRes(golems.expire(user))

    golemgrave = "in front of you"
    if len(players.getMines(user)) > 0:
        golemgrave = "inside of "+players.getMines(user)[0].capitalize()

    say(user, "After working for "+life+", your golem crumbles to dust "+golemgrave+" and leaves a wake of its mined resources: "+mined)

    return True

def golemDestroy(channel, user, time):
    life = formatter.prettyTime(golems.getLife(user, time))
    mined = game.itemizeRes(golems.destroy(user))

    say(channel, "Your golem collapsed on the spot!  Through the rubble, you manage to recover the following resources: "+mined, user)

    return True

def strike(msg, channel, user, time):
    mineList = players.getMines(user)
    target = mineList[0] #autotarget first mine

    selected = msg.split(COMMANDS[3])[-1].split(" ")[-1] #check for targetted mine
    if selected != "":
        if mineList.count(selected) == 0:
            say(user, "That's not a mine you're working on, friend.")
            return

        if target != selected:
            target = selected
            mineList.remove(target)    #bump this to the top of the minelist
            mineList.insert(0, target)

    #diff = int(time)-int(players.getLastStrike(user))
    #if diff < baseFatigue: # fatigue check
    #    left =  baseFatigue - diff
    #    fatigue = left * 2
    #    time = int(time) + fatigue - baseFatigue

    fatigue = players.fatigueCheck(user, time)
    if fatigue > 0:
        fatigue = fatigue * 2
        time = int(time) + fatigue - (baseFatigue - players.getEndurance(user))# still hardcoded bs
        say(user, "You're still tired from your last attempt.  You'll be ready again in "+str(fatigue)+" seconds.  Please take breaks to prevent fatigue; rushing will only lengthen your recovery.")

    else: # actual mining actions
        emptyMines = []
        status = players.incStrikes(user)
        excavation = players.strike(user, target)
        mined = players.printExcavation(players.acquireRes(user, excavation))
        say(user, "\x03" + random.choice(['4', '8', '9', '11', '12', '13'])+random.choice(['WHAM! ', 'CRASH!', 'BANG! ', 'KLANG!', 'CLUNK!', 'PLINK!', 'DINK! '])+"\x03  "+status+"You struck at " + target.capitalize() +" and excavated "+mined)

        if mines.getTotal(target) == 0:
            emptyMines.append(target)
            players.incCleared(user)
            players.incEndurance(user)
            players.incAvailableMines(user)
            say(user, "As you clear the last of the rubble from "+target.capitalize()+", a mysterious wisp of smoke rises from the bottom.  You feel slightly rejuvinated when you breathe it in.")
            say(user, target.capitalize()+" is now empty.  The empress shall be pleased with your progress.  I'll remove it from your dossier now; feel free to request a new mine.")
            say(config[1], "There's a distant rumbling as "+user+" clears the last few resources from "+target.capitalize()+".")

        for x in emptyMines:
            mineList.remove(x)

    players.updateOwned(user, mineList)
    players.updateLastStrike(user, time)

def report(msg, channel, user, time):
    if len(players.getMines(user)) > 0:
        say(user, game.mineListFormatted(msg, channel, user))
    say(user, game.resourcesFormatted(channel, user))
    if hasGolem(user):
        say(user, game.golemStats(channel, user, time))
    say(user, game.statsFormatted(channel, user))

def grovel(msg, channel, user, time):
    players.incGrovel(user)
    statement = '\x03' + random.choice(['4', '8', '9', '11', '12', '13']) + str(empress.speak()).rstrip()

    say(channel, "The empress "+random.choice(['says', 'states', 'replies', 'snaps', 'mumbles', 'mutters'])+", \""+statement+"\x03\"  "+random.choice(INTERP_NEU), user)

def stirke(msg, channel, user, time): #hazelnut memorial disfeature
    a = 0

def fatigue(msg, channel, user, time): #~krowbar memorial feature
    fatigue = players.fatigueCheck(user, time)
    if fatigue > 0:

        say(channel, "You'll be ready to strike again in "+formatter.prettyTime(fatigue)+".  Please rest patiently so you do not stress your body.", user)
=======
            wham = random.choice(LANG.get("wham"))

        response.append(wham + lvlMsg + "  You struck at "+ mineName + " and mined the following: "+ game.print_reslist(reslist))
        if depleted:
            response.append("As you clear the last of the rubble from "+mineName+", a mysterious wisp of smoke rises from the bottom.  You feel slightly rejuvinated when you breathe it in.")
            response.append(mineName+" is now empty.  The empress shall be pleased with your progress.  I'll remove it from your dossier now; feel free to request a new mine.")

>>>>>>> gamerefactor
    else:
        response.append(strike_failure(fatigue, permitted))

    return response

def rankings(playeID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def golem(playerID, user, time, inputs):

    response = []

    response.append(UNIMP)

    return response

def res(playerID, user, time, inputs):

    response = []

    response.append(player_res(playerID))

    return response

def alias(playerID, user, time, inputs):

    response = []

    if len(inputs) < 2:
        response.append("You need to specify at least one alias to add to your dossier, friend.")
    else:
        inputs.pop(0)
        added = []
        unadded = []
        print(inputs)
        for alias in inputs:
            if game.alias(playerID, alias):
                added.append(alias)
            else:
                unadded.append(alias)
        if added:
            response.append("I've added "+",".join(added)+" to your alias list.")
        if unadded:
            response.append(", ".join(added)+" could not be added due to conflicting records.")

    return response

def world(playerID, user, time, inputs):

    response = []

    response.append(provinces())
    response.append(players())

    return response

## helper functions

def make_player(user, now, zoneID):
    # creates new inits for a player

    playerdata = {}
    playerdata.update({"nick":user})
    playerdata.update({"home":zoneID})
    playerdata.update({"joined":now})

    return playerdata

def failed_join(hasSpace, zoneExists):
    # processes join failure

    if not zoneExists:
        return "I've never heard of that province, stranger.  "+provinces()

    if not hasSpace:
        return "I'm sorry, friend, but that province cannot support any additional residents.  Please choose a different one in order to prevent overcrowding."

def players():
    # returns list of players

    players = game.list_players()

    msg = "The following "+p.plural("worker", len(players))+" "+p.plural("is", len(players))+" registered as "+p.plural("citizen", len(players))+" of the empress's land: "
    msg += ", ".join(players)

    return msg

def provinces():
    # returns list of provinces

    zones = game.list_zones()

    msg = "The following "+p.plural("province", len(zones))+" "+p.plural("falls", len(zones))+" under the empress's rule: "
    msg += ", ".join(zones)

    return msg

def failed_new(hasSpace, mayCreate):
    # generates mine failure message

    msg = "I could not open a new mine on your behalf because"

    if not hasSpace:
        msg += " your current locale cannot support an additional mining venture"

    if not mayCreate:
        if not hasSpace:
            msg += " and"

        msg += " you do not have permission to open any more mines"

    return msg + "."

def strike_failure(fatigue, permitted):
    # generates strike failure message

    #msg = ""

    #if fatigue:
        #msg += "You're still tired from your last attempt.  You'll be ready again in "+util.pretty_time(fatigue)+".  Please take breaks to prevent fatigue; rushing will only lengthen your recovery."

    if not permitted:
        #if fatigue:
        #    msg += "  Additionally, y"
        #else:
        #    msg += "Y"

        #msg += "ou do not have permission to work on that mine, friend."
        return "You do not have permission to work on that mine, friend."

    if fatigue:
        return "You're still tired from your last attempt.  You'll be ready again in "+util.pretty_time(fatigue)+".  Please take breaks to prevent fatigue; rushing will only lengthen your recovery."

    return ""

    #return msg

def pretty_res(reslist):
    # return a string of human-readable reslist

    readable = []

    for res in reslist:
        readable.append(p.no(res, reslist.get(res)))

    return ", ".join(readable)

def player_res(playerID):
    # given playerID, generated held res list

    res = pretty_res(game.get_data("players", playerID, "held res"))

    if res:
        return "You're holding the following resources: "+res
    else:
        return "You don't have any resources in your possession.  On behalf of the empresss, I encoruage you to work on your mining endeavors."


def player_stats(playerID, now):
    # given playerID, return formatted stats

    response = []

    depth, width = game.player_strikerate(playerID)
    fatigue = game.player_fatiguerate(playerID)

    response.append("You can mine up to "+p.no("unit", depth)+" from "+p.no("vein", width)+" every strike, and strike every "+p.no("second", fatigue)+" without experiencing fatigue.")
    response.append("You've cleared "+p.no("mine", len(game.get_data("players", playerID, "mines completed"))) +".")
    # "You can make a golem with up to "+p.no("resource", int(3.5*players.getStrength(user)))+".  "


    return response

def player_favors(playerID):
    # format player favor list

    favors = game.get_data("players", playerID, "favors")

    if favors:
        return "The empress has granted you the following "+p.no("favor", len(favors))+": "+", ".join(favors)
    else:
        return "You do not have any earned favors from the empress.  She will reward your dilligence and loyalty."

def player_fatigue(playerID, now):
    # given playerID, return formatted fatigue message

    fatigue = game.fatigue_left(playerID, now)

    if fatigue:
        return "You'll be ready to strike again in "+util.pretty_time(fatigue)+".  Please rest patiently so you do not stress your body."
    else:
        return "You're refreshed and ready to mine.  Take care to not overwork; a broken body is no use to the empress."

def player_mines(playerID):
    # given playerID, return mine sentence

    minelist = pretty_minelist(game.list_mines(playerID))
    if minelist:
        msg = "You own the following "+p.plural("mines", len(minelist))+": "
        msg += ", ".join(minelist)
    else:
        msg = "You don't own any mines friend.  The empress expects all citizens to work productively; please consider making progress on your mining ventures."

    return msg

def pretty_minelist(rawlist):
    # takes a list of ["mine name", depletion] and formats for output

    minelist = []

    for mine in rawlist:
        postfix = ""
        depletion = mine[1]

        if depletion is not None:   # True if depletion has been set
            color = ""
            uncolor = ""
            if IRC:
                uncolor = "\x03"
                if depletion > 98:
                    color = "\x0311"
                elif depletion > 90:
                    color = "\x0309"
                elif depletion > 49:
                    color = "\x0308"
                elif depletion > 24:
                    color = "\x0307"
                elif depletion > 9:
                    color = "\x0304"
                else:
                    color = "\x0305"

            postfix = " ("+color+str(depletion)+"%"+uncolor+")"

<<<<<<< HEAD
        elif msg.find(":!"+COMMANDS[6]) != -1: # !grovel
            if isPlaying(user):
                grovel(msg, channel, user, time)
                #say(channel, "The empress is indisposed at the moment.  Perhaps she will be open to receiving visitors in the future.  Until then, I'd encourage you to work hard and earn her pleasure.", user)
            else:
                say(channel, "I advise against groveling unless you're in my records, friend.  Request a new dossier with '!init'.", user)
=======
        minelist.append(mine[0]+postfix)
>>>>>>> gamerefactor

    return minelist

def golem_stats(playerID):
    # copied over from old version

    #status = golems.getShape(user)+" is hard at work!  "
    #status += "It can excavate up to "+p.no("resource", golems.getStrength(user))+" per strike, and strikes every "+p.no("second", golems.getInterval(user)) + ".  "
    #status += "It's been going for "+util.pretty_time(golems.getLife(user, time))+"."

    #return status

    return
