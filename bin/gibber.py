#!/usr/bin/python

import random

syllablefile = open("config/syllables.txt", 'r')
syllables = []
for x in syllablefile:
    syllables.append(x.rstrip())

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

def sentence(base = 5, cap = 10):
    i = 0
    sentence = ''
    while i < random.randrange(base, cap):
        if i == 0:
            sentence += new(random.randrange(1,5)).capitalize()
        else:
            sentence += random.choice(['', '', '', ','])
            sentence += " " + medium()
        i += 1

    sentence += random.choice(['.', '.', '.', '.', '.', '!', '?'])+ " "
    return sentence

def paragraph(base = 5, cap = 20):
    i = 0
    paragraph = ''
    while i < random.randrange(base, cap):
        paragraph += sentence()
        i += 1

    return paragraph
