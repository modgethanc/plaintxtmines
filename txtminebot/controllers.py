#!/usr/bin/python
'''
This module contains classes for frontend handlers for txtminebot.

Currently, this module only supports an IRC frontend. The IRC handler was
patched together from various bits of tilde.town and other references.

plaintxtmines is a text-based multiplayer mining simulator. For more
information, see the full repository:

https://github.com/modgethanc/plaintxtmines
'''

import os
import sys
import random
import re
import time
import importlib
import imp

import socket

import ircformatter
import vtils

import txtminebot

__version__ = "1.0"
__author__ = "Vincent Zeng <hvincent@modgethanc.com>"

## globals

DEFAULT_CONFIG = "irc.conf"

## classes

class IRC():
    '''
    IRC handler.

    Takes an optional specific configuration file of format:
        IRC.SERVERNAME.NET
        #DEFAULTCHAN,#DEFAULTCHAN2,#DEFAULTCHAN3
        BOTNAME
        ADMINNAME
    '''

    def __init__(self, configfile = DEFAULT_CONFIG):
        self.BOTNAME = ""
        self.ADMIN = ""
        self.SERVER = ""
        self.DEFAULTCHANS = []
        self.MAINCHAN = ""
        self.CHANNELS = []
        self.LASTCHECK = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.load(configfile):
            print "Successfully loaded configuration file! Hi, "+self.ADMIN+", I'm "+self.BOTNAME+"!"
           
        else:
            print "There was a problem with the config file, ["+configfile+"]. Either it doesn't exist, or the format was not as expected. See documentation for details."

    ## structural functions

    def load(self, configfile=DEFAULT_CONFIG):
        '''
        Parse a config file, if given full file path. Otherwise, parses a config
        file at the default location. Quits if no valid config file.

        Expected format:
        IRC.SERVERNAME.NET
        #DEFAULTCHAN,#DEFAULTCHAN2,#DEFAULTCHAN3
        BOTNAME
        ADMINNAME
        '''

        if not os.path.isfile(configfile):
            return False

        # TODO: validate config file

        configfile = open("irc.conf", "r")
        config = []
        for x in configfile:
            config.append(x.rstrip())
        configfile.close()

        self.BOTNAME = config[2]
        self.ADMIN  = config[3]
        self.SERVER = config[0]
        self.DEFAULTCHANS = config[1].split(',')
        # assumes first channel listed is main game channel
        self.MAINCHAN = self.DEFAULTCHANS[0]

        return configfile

    def start(self, configfile = DEFAULT_CONFIG):
        '''
        Loads the specified config file (or uses system default if not given),
        then connects to the server.
        '''

        if self.load(configfile):
            self.connect(self.SERVER, self.DEFAULTCHANS, self.BOTNAME)
        return "Connected to "+self.SERVER+"!"

    def reload(self):
        '''
        Calls reload on txtminebot module.
        '''

        reload(txtminebot)

    ### irc functions

    def send(self, msg):
        '''
        Wraps the message by encoding it to bytes, then sends it to current
        socket.
        '''

        # TODO: option for toggling echo

        print ">>" + msg
        self.sock.send(msg.encode('ascii'))

    def ping(self, pingcode):
        '''
        Pongs the server.
        '''

        self.send("PONG :"+pingcode+"\n")
        print("PONG! " + pingcode)

    def joinchan(self, chan):
        '''
        Joins named channel, and adds it to global channel list.
        '''

        self.CHANNELS.append(chan)
        self.send("JOIN "+ chan +"\n")
        print(self.CHANNELS)

    def part(self, chan, partmsg=""):
        '''
        Leaves named channel, and removes it from the global channel list.
        Optionally, includes a part message.
        '''

        print(self.CHANNELS)
        self.CHANNELS.remove(chan)
        self.send("PART "+ chan +" :"+partmsg+"\n")

    def connect(self, server, channel, botnick):
        '''
        Connects to server, naming itself and owner, and automatically joins list
        of channels.
        '''

        print "I'm about to connect to "+str(self.DEFAULTCHANS)+"@"+self.SERVER +"!"
        self.sock.connect((server, 6667))
        #self.send("USER ~"+botnick+" 0 * :"+self.ADMIN+"'s bot\n")
        self.send("USER "+botnick+" "+botnick+" "+botnick+" :"+self.ADMIN+"'s bot\n")
        self.send("NICK "+botnick+"\n")

        #time.sleep(5)

        while 1:
            # wait for mode set before joining channels
            msg = self.sock.recv(2048)

            if msg:
                print(msg)

                if msg.find("PING :") == 0:
                    pingcode = msg.split(":")[1]
                    print "[pinged] with "+pingcode
                    self.ping(pingcode)

                elif msg.find("MODE") != -1:

                    for chan in self.DEFAULTCHANS:
                        self.joinchan(chan)
                    return

                elif msg.find("ERROR") == 0:
                    print "connection error :("
                    return

    def disconnect(self, quitmsg=""):
        '''
        Disconnects from server and closes the socket. Optionally, includes a
        quit message.
        '''

        self.send("QUIT " + quitmsg + "\n")
        self.sock.close()

    def say(self, channel, msg, nick=""):
        '''
        Sends message to single channel, with optional nick addressing.
        '''

        if nick == channel: #don't repeat nick if in PM
          nick = ""
        elif nick:
          nick += ": "

        self.send("PRIVMSG "+channel+" :"+nick+msg+"\n")

    def multisay(self, channel, msglist, nick=""):
        '''
        Takes a list of messages to send to a single channel processes them,
        calling self.say() on each one.

        Also provides the option of processing a dict from an individual
        message, extracting "msg" and "channel" appropriately.
        '''

        for line in msglist:
            msg = ""
            chan_target = ""
            nick_target = ""

            if isinstance(line, dict):
                # message metadata handling

                msg = line.get("msg")
                chan_target = line.get("channel")
                nick_target = line.get("nick")

                if chan_target:
                    if chan_target == "MAIN":
                        channel = self.MAINCHAN
                    else:
                        channel = chan_target

                if not nick_target:
                    nick = ""
                else:
                    nick = nick_target
            else:
                msg = line

            self.say(channel, msg, nick)

    def wall(self, msg, nick=""):
        '''
        Sends a single message to all connected channels, and optional nick
        addressing.
        '''

        for x in self.CHANNELS:
            self.say(x, msg, nick)

    def multiwall(self, msglist, nick=""):
        '''
        Takes a list of messages to send, and sends them to all channels, with
        optional nick addressing.
        '''
        for x in msglist:
            self.wall(x, nick)

    def is_pm(self, parsed):
        '''
        Checks if parsed message is a PM.
        '''
        return parsed.get("channel") == parsed.get("nick")

    def admin_panel(self, channel, user, time, msg):
        '''
        Various admin-only commands.
        '''

        #print("admin")

        if msg.find("!join") == 0:
            self.say(channel, "k", user)
            split = msg.split(" ")
            for x in split:
                if x.find("#") != -1:
                    self.joinchan(x)
                    return "join"

        elif msg.find("!brb") == 0:
            self.say(channel, "k bye", user)
            self.part(channel)
            return "part"

        elif msg.find("get out") == 0:
            self.say(channel, "k bye", user)
            self.part(channel)
            return "part"

        elif msg.find("!gtfo") == 0:
            self.say(channel, "ollie outie broski")
            self.disconnect()
            return "die"

        elif msg.find("!names") == 0:
            self.send("NAMES "+channel+"\n")
            return "names"

        elif msg.find("!channels") == 0:
            chanlist = " ".join(self.CHANNELS)
            self.say(channel, "i'm in "+chanlist)
            return "names"

        elif msg.find("!wall") == 0:
            split = msg.split("!wall ")
            wallmsg = "".join(split[1])
            self.wall(wallmsg)
            return "wall"

        elif msg.find("!say") == 0:
            splitter = msg.split("!say ")[1]
            parse = splitter.split(" ")
            self.say(parse[0], " ".join(parse[1:]))
            return "say"

    def tick(self, now):
        '''
        Gets called every time one second elapses, to handle all the time-based
        actions.
        '''

        self.multisay("",txtminebot.tick(now))

        return

    def listen(self):
        '''
        A loop for listening for messages.
        '''

        self.LASTCHECK = int(time.time())

        while 1:
            now = int(time.time())

            if now - self.LASTCHECK > 0:
                self.LASTCHECK = now
                self.tick(now)

            msg = self.sock.recv(2048)
            if msg:
                if re.match("^PING", msg):
                    print "[pinged]"
                    pingcode = msg.split(":")[1]
                    self.ping(pingcode)

                try:
                    self.handle(msg.decode('ascii'))
                except UnicodeDecodeError:
                    continue

    def handle(self, msg):
        '''
        main message handler. reponds to ping if server pings; otherwise,
        parses incoming message and handles it appropriately.

        if the message was a pm, responds in that pm.

        if the message was from the bot owner, call admin_panel() before
        proceeding.

        current responses:
        join: greets newcomer and attempts to give them ops.
        privmsg: calls bot core for either said or addressed, depending on if the
        bot was addressed in the message.
        '''

        msg = msg.strip('\n\r')

        ## TODO: toggle message echo

        print(msg)

        if re.match("^PING", msg):
            print "[pinged]"
            pingcode = msg.split(":")[1]
            return self.ping(pingcode)

        msg = msg.strip('\n\r')

        parsed = ircformatter.parse_dict(msg)
        #print(parsed)

        ## actions on join
        if parsed.get("command") == "JOIN":
            self.join_handler(parsed)
        if parsed.get("command") == "MODE":
            self.mode_handler(parsed)

        ## actions on privmsg
        if parsed.get("command") == "PRIVMSG":
            ## if this is a PM, switch channel for outgoing message
            if parsed.get("channel") == self.BOTNAME:
                #print("PM with "+parsed.get("nick"))
                parsed.update({"channel":parsed.get("nick")})

            ## detect if this is an admin command
            if parsed.get("nick") == self.ADMIN:
                #print("admin")
                code = self.admin_panel(parsed.get("channel"), parsed.get("nick"), parsed.get("time"), parsed.get("message"))
                if code:
                   return

            if parsed.get("message").find(self.BOTNAME+": ") != -1 or self.is_pm(parsed):
                # responses when directly addressed
                self.multisay(parsed.get("channel"),
                        txtminebot.addressed(self, parsed.get("channel"), parsed.get("nick"), parsed.get("time"), parsed.get("message"), "irc"), parsed.get("nick"))
            else:
                # general responses

                self.multisay(parsed.get("channel"), txtminebot.said(self, parsed.get("channel"), parsed.get("nick"), parsed.get("time"), parsed.get("message"), "irc"), parsed.get("nick"))

        sys.stdout.flush()

    ## handler helper funcions

    def join_handler(self, parsed):
        '''Handles actions when someone joins the channel.'''

        return

    def mode_handler(self, parsed):
        '''Handles actions when mode changes happen. Acknowledges receiving
        ops.'''

        # TODO: ops acknowledgement text

        if re.match("\+o "+self.BOTNAME, parsed.get("message")):
            self.say(parsed.get("channel"), "")


### MAIN IRC BOT CONTROL

def irc_start():
    '''Create an instance of txtminebot's IRC mouth and start it.'''

    txtminebot = IRC()
    txtminebot.start()
    irc_loop(txtminebot)

def irc_loop(head):
    '''Main loop to allow for hot-reloading txtminebot core code without
    dropping the IRC connection.'''

    try:
        head.listen()
    except KeyboardInterrupt:
        print ""
        proceed = vtils.input_yn("reload?")

        if proceed:
            # juggle existing socket and channels
            sock = head.sock
            chans = head.CHANNELS
            head.reload()

            head = IRC()
            head.sock = sock
            head.CHANNELS = chans
            irc_loop(head)
        else:
            # TODO: fire clean bot shutdown

            head.disconnect("Rest for now, until I return, citizens.")

            print "bot going down!"

if __name__ == "__main__":
    '''Hardcoded to fire an IRC instance.'''

    irc_start()
