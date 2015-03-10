#!/usr/bin/python

import os
import random
import gibber

def newEmpress():
    empressfile = open('../data/empress/txt', 'w+')

    empressfile.write('0\n') # 0 next grovel window
    empressfile.write("0,0,0,0,0,0,0,0\n") # 1 tithed total
    empressfile.write('\n') # 2 favorite

### output

def openEmpress():
    return

def getGrovel():
    return

def getTithed():
    return

def getFavorite():
    return

def speak():
    return gibber.sentence()

if not os.path.isfile("../data/empress.txt"):
    newEmpress()
