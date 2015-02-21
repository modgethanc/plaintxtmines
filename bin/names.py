#!/usr/bin/python

import random

syllablefile = open("syllables.txt", 'r')
syllables = []
for x in syllablefile:
    syllables.append(x.rstrip())

def printSyllables():
    for x in syllables:
        print x

def new(size):
    i = size
    name = ''
    while i > 0:
        name += random.choice(syllables)
        i -= 1

    return name

def short():
    return new(random.randrange(1,3))

def medium():
    return new(random.randrange(3,5))

def long():
    return new(random.randrange(5,6))

def excessive():
    return new(random.randrange(6,10))

print short()
print medium()
print long()
print excessive()
