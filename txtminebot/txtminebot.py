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

def addressed(channel, nick, time, msg, interface):
    '''
    Returns responses to something said in a channel when directly addressed.
    Every time this bot is addressed, this should be called.
    '''

    response = []

    response.append("hi")

    return response

def said(channel, nick, time, msg, interface):
    '''
    Returns responses to something said in a channel, when not directly
    addressed. This should catch everything that addressed() misses.
    '''

    response = []

    response.append("i heard you")

    return response

## command handlers

## helper functions
