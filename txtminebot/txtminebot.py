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
        response.append("Commands: !init, !open, !mines, !strike {mine}, !report, !stats, !fatigue, !golem {resources}, !grovel, !rankings, !info.")
        #ircsock.send("PRIVMSG "+ channel +" :"+ user + ": I am the mining assistant, here to facilitate your ventures by order of the empress.  Commands: !init, !open, !mines, !strike {mine}, !report, !stats, !fatigue, !golem {resources}, !grovel, !rankings, !info.\n")

    elif msg.find(":!"+COMMANDS[0]) != -1: # !init
        if isPlaying(user):
            response.append("You already have a dossier in my records, friend.")
            #ircsock.send("PRIVMSG "+ channel +" :"+ user + ": You already have a dossier in my records, friend.\n")
        else:
            response.append(newPlayer(channel, user))

    elif msg.find(":!"+COMMANDS[1]) != -1: # !open
        if isPlaying(user):
            if players.getAvailableMines(user) > 0:
                 response.append(newMine(channel, user))
            else:
                response.append("You do not have permission to open a new mine at the moment, friend.  Perhaps in the future, the empress will allow you further ventures.")
                #ircsock.send("PRIVMSG "+ channel + " :" + user + ": You do not have permission to open a new mine at the moment, friend.  Perhaps in the future, the empress will allow you further ventures.\n")
        else:
            response.append("I can't open a mine for you until you have a dossier in my records, friend.  Request a new dossier with '!init'.\n")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I can't open a mine for you until you have a dossier in my records, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[2]) != -1: # !mines
        if isPlaying(user):
            if len(players.getMines(user)) == 0:
                response.append("You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.")
                #ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else:
                response.append(mineListFormatted(msg, channel, user))
                #ircsock.send("PRIVMSG "+channel+" :" + user + ": "+mineListFormatted(msg, channel, user)+"\n")
        else:
            response.append("I don't have anything on file for you, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[9]) != -1: # !stats
        if isPlaying(user):
            response.append(statsFormatted(channel, user))
            #ircsock.send("PRIVMSG "+channel+" :" + user + ": "+statsFormatted(channel, user)+"\n")
        else:
            response.append("I don't know anything about you, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[11]) != -1: # !res
        if isPlaying(user):
            response.append(resourcesFormatted(channel, user))
            #ircsock.send("PRIVMSG "+channel+" :" + user + ": "+resourcesFormatted(channel, user)+"\n")
        else:
            response.append("I don't know anything about you, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[3]) != -1: # !strike
        if isPlaying(user):
            if len(players.getMines(user)) == 0:
                response.append("You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.")
                #ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have any mines assigned to you yet, friend.  Remember, the empress has genrously alotted each citizen one free mine.  Start yours with '!open'.\n")
            else:
                strike(msg, channel, user, time)
        else:
            response.append("I don't have anything on file for you, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[5]) != -1: # !fatigue
        if isPlaying(user):
            fatigue(msg, channel, user, time)
        else:
            response.append("I don't know anything about you, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[6]) != -1: # !grovel
        if isPlaying(user):
            if random.randrange(1,100) < 30:
                response.append("The empress is indisposed at the moment.  Perhaps she will be open to receiving visitors in the future.  Until then, I'd encourage you to work hard and earn her pleasure.")
                #ircsock.send("PRIVMSG "+ channel + " :" + user + ": The empress is indisposed at the moment.  Perhaps she will be open to receiving visitors in the future.  Until then, I'd encourage you to work hard and earn her pleasure.\n")
            else:
                grovel(msg, channel, user, time)
        else:
            response.append("I advise against groveling unless you're in my records, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I advise against groveling unless you're in my records, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[4]) != -1: # !report
        if isPlaying(user):
            report(msg, channel, user, time)
        else:
            response.append("I don't have anything on file for you, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't have anything on file for you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[10]) != -1: # !golem
        if isPlaying(user):
            parse = msg.split("!"+COMMANDS[10])
            if parse[1] == '': #no arguments
                if hasGolem(user):
                    response.append(golemStats(channel, user, time))
                    response.append("It's holding the following resources: "+golems.heldFormatted(user))
                    #ircsock.send("PRIVMSG "+ channel + " :" + user + ": "+golemStats(channel, user, time)+".\n")
                    #ircsock.send("PRIVMSG "+ channel + " :" + user + ": It's holding the following resources: "+golems.heldFormatted(user)+".\n")

                    #ircsock.send("PRIVMSG "+ channel + " :" + user + ": "+golems.getShape(user)+" is hard at work!  It'll last for another "+p.no("second", golems.getLifeRemaining(user, time))+".\n")
                else:
                    response.append("You don't have a golem working for you, friend.  Create one with '!golem {resources}'.")
                    #ircsock.send("PRIVMSG "+ channel + " :" + user + ": You don't have a golem working for you, friend.  Create one with '!golem {resources}'.\n")
            else: # check for mines??
                response.append(newGolem(channel, user, time, parse[1].lstrip()))
        else:
            response.append("I don't know anything about you, friend.  Request a new dossier with '!init'.")
            #ircsock.send("PRIVMSG "+ channel + " :" + user + ": I don't know anything about you, friend.  Request a new dossier with '!init'.\n")

    elif msg.find(":!"+COMMANDS[8]) != -1: # !rankings
        rankings(msg, channel, user)

    return response

## command handlers

## legacy gameplay functions

def newPlayer(channel, user):
    if os.path.isfile('../data/'+user+'.stats'):
        players.newDossier(user)
    else:
        players.newPlayer(user)

    global dossierList
    dossierList.append(user)

    return "New dossier created.  By order of the empress, each citizen is initially alotted one free mine.  Request your mine with '!open'."

def newMine(channel, user, rates="standardrates"):
    mine = players.newMine(user, "standardrates").capitalize()
    players.decAvailableMines(user)

    return "Congratulations on successfully opening a new mine.  In honor of your ancestors, it has been named "+mine+".  I wish you fortune in your mining endeavors.  Always keep the empress in your thoughts, and begin with an enthusiastic '!strike'."

def newGolem(channel, user, time, golemstring):
    if hasGolem(user):
        return "You can't make a new golem until your old golem finishes working!  It'll be ready in "+formatter.prettyTime(golems.getLifeRemaining(user, time))
    else:
        if golems.calcStrength(golems.parse(golemstring)) > 0:
            if players.canAfford(user, golems.parse(golemstring)):
                golemfilter = list(golemstring)
                maxgolem = (players.getStrength(user)*3.5)
                if len(golemfilter) > maxgolem:
                  return "You're not strong enough to construct a golem that big, friend.  The most you can use is "+p.no("resource", maxgolem)
                else:
                  golemshape = []
                  for x in golemfilter:
                      if x in ['~', '@', '#', '^', '&', '*', '[', ']']:
                          golemshape.append(x)

                  golem = golems.newGolem(user, ''.join(golemshape), time)
                  players.removeRes(user, golems.getStats(user))
                  logGolem(user)

                  return players.printExcavation(golems.getStats(user))+ " has been removed from your holdings.  Your new golem will last for "+formatter.prettyTime(golems.getLifeRemaining(user, time))+".  Once it expires, you can gather all the resources it harvested for you."
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

def updateGolems(time):
    for x in listGolems():
        strikeDiff = int(time) - golems.getLastStrike(x)
        interval = golems.getInterval(x)

        if strikeDiff >= interval and len(players.getMines(x)) > 0: # golem strike
            target = players.getMines(x)[0]
            strikeCount = strikeDiff/interval
            i = 0
            elapsed = golems.getLastStrike(x)
            while i < strikeCount:
                if mines.getTotal(target) > 0:
                    print "golemstrike"+ str(golems.strike(x, target))
                elapsed += interval
                i += 1

            golems.updateLastStrike(x, elapsed)

        if int(time) > golems.getDeath(x): # golem death
            golem = golems.getShape(x)
            mined = players.printExcavation(golems.expire(x))
            golemgrave = "in front of you"
            if len(players.getMines(x)) > 0:
                golemgrave = "inside of "+players.getMines(x)[0].capitalize()

            """TODO: figure out how to make tick speak appropriately! old
            response below:

            ircsock.send("PRIVMSG "+ x +" :"+golem+" crumbles to dust "+golemgrave+" and leaves a wake of "+mined+"\n")
            """

""" LINE OF DEATH """

def strike(msg, channel, user, time):
    mineList = players.getMines(user)
    target = mineList[0] #autotarget first mine

    selected = msg.split(COMMANDS[3])[-1].split(" ")[-1] #check for targetted mine
    if selected != "":
        if mineList.count(selected) == 0:
            ircsock.send("PRIVMSG "+ user +" : That's not a mine you're working on, friend.\n")
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
        ircsock.send("PRIVMSG "+ user +" :You're still tired from your last attempt.  You'll be ready again in "+str(fatigue)+" seconds.  Please take breaks to prevent fatigue; rushing will only lengthen your recovery.\n")

    else: # actual mining actions
        emptyMines = []
        status = players.incStrikes(user)
        excavation = players.strike(user, target)
        mined = players.printExcavation(players.acquireRes(user, excavation))
        ircsock.send("PRIVMSG "+ user +" :\x03" + random.choice(['4', '8', '9', '11', '12', '13'])+random.choice(['WHAM! ', 'CRASH!', 'BANG! ', 'KLANG!', 'CLUNK!', 'PLINK!', 'DINK! '])+"\x03  "+status+"You struck at " + target.capitalize() +" and excavated "+mined+"\n")

        if mines.getTotal(target) == 0:
            emptyMines.append(target)
            players.incCleared(user)
            players.incEndurance(user)
            players.incAvailableMines(user)
            ircsock.send("PRIVMSG "+ user +" :As you clear the last of the rubble from "+target.capitalize()+", a mysterious wisp of smoke rises from the bottom.  You feel slightly rejuvinated when you breathe it in.\n")
            ircsock.send("PRIVMSG "+ user +" :"+target.capitalize()+" is now empty.  The empress shall be pleased with your progress.  I'll remove it from your dossier now; feel free to request a new mine.\n")
            ircsock.send("PRIVMSG "+config[1]+" :There's a distant rumbling as "+user+" clears the last few resources from "+target.capitalize()+".\n")

        for x in emptyMines:
            mineList.remove(x)

    players.updateOwned(user, mineList)
    players.updateLastStrike(user, time)

def report(msg, channel, user, time):
    if len(players.getMines(user)) > 0:
        ircsock.send("PRIVMSG "+ user +" :"+mineListFormatted(msg, channel, user)+"\n")
    ircsock.send("PRIVMSG "+ user +" :"+resourcesFormatted(channel, user)+"\n")
    if hasGolem(user):
        ircsock.send("PRIVMSG "+ user +" :"+golemStats(channel, user, time)+".\n")
    ircsock.send("PRIVMSG "+ user +" :"+statsFormatted(channel, user)+"\n")

def grovel(msg, channel, user, time):
    players.incGrovel(user)
    statement = '\x03' + random.choice(['4', '8', '9', '11', '12', '13']) + str(empress.speak()).rstrip()

    ircsock.send("PRIVMSG "+ channel + " :" + user +": The empress "+random.choice(['says', 'states', 'replies', 'snaps', 'mumbles', 'mutters'])+", \""+statement+"\x03\"  "+random.choice(INTERP_NEU)+"\n")

def stirke(msg, channel, user, time): #hazelnut memorial disfeature
    a = 0

def fatigue(msg, channel, user, time): #~krowbar memorial feature
    fatigue = players.fatigueCheck(user, time)
    if fatigue > 0:

        ircsock.send("PRIVMSG "+ channel + " :" + user +": You'll be ready to strike again in "+formatter.prettyTime(fatigue)+".  Please rest patiently so you do not stress your body.\n")
    else:
        ircsock.send("PRIVMSG "+ channel + " :" + user +": You're refreshed and ready to mine.  Take care to not overwork; a broken body is no use to the empress.\n")

def mineListFormatted(msg, channel, user):
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

    return "You're working on the following mine"+plural+": "+j.join(prejoin)

def resourcesFormatted(channel, user):
    return "You're holding the following resources: "+players.heldFormatted(user)

def statsFormatted(channel, user):
    stats = "You can mine up to "+str(3*players.getStrength(user))+" units every strike, and strike every "+p.no("second", baseFatigue - players.getEndurance(user))+" without experiencing fatigue.  "
    plural = 's'
    if players.getClearedCount(user) == 1: plural = ''
    stats += "You've cleared "+str(players.getClearedCount(user))+" mine"+plural+".  "
    stats += "You can make a golem with up to "+p.no("resource", int(3.5*players.getStrength(user)))+".  "
    stats += "Please continue working hard for the empress!"

    return stats

def golemStats(channel, user, time):
    status = golems.getShape(user)+" is hard at work!  "
    status += "It can excavate up to "+p.no("resource", golems.getStrength(user))+" per strike, and strikes every "+p.no("second", golems.getInterval(user))+".  It'll last another "+formatter.prettyTime(golems.getLifeRemaining(user, time))

    return status

def rankings(msg, channel, user):
    dossiers = dossierList
    #playerlist = open("../data/players.txt", 'r')
    #for x in playerlist:
    #   dossiers.append(x.rstrip())
    #playerlist.close()

    records = []
    for x in dossiers:
        records.append([x, str(players.getHeldTotal(x))])

    records.sort(key=lambda entry:int(entry[1]), reverse=True)
    ircsock.send("PRIVMSG " + channel + " :The wealthiest citizens are:\n")

    for x in range (0, min(5, len(records))):
        entry = records[x]
        ircsock.send("PRIVMSG " + channel + " :" + entry[0] + " with " + entry[1] + " units\n")

## helper functions

def tick(now):
    '''
    Called by IRC whenever a second ellapses.

    TODO: Put golem updating here!
    '''

    updateGolems(now)

    return
