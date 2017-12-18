#!/usr/bin/env python
"""
Using the given syllable file, create text in the empress's tongue.
"""

import random

syllablefile = open("syllables.txt", 'r')
syllables = []
for x in syllablefile:
    syllables.append(x.rstrip())

def new_word(size):
    """Creates a single word with <size> as the given number of syllables.
    """

    i = size
    name = ''
    while i > 0:
        name += random.choice(syllables)
        i -= 1

    return name

def short_word():
    """Creates a word between 1 and 3 syllables long.
    """

    return new_word(random.randrange(1,3))

def medium_word():
    """Creates a word between 3 and 5 syllables long.
    """

    return new_word(random.randrange(3,5))

def long_word():
    """Creates a word between 5 and 6 syllables long.
    """

    return new_word(random.randrange(5,6))

def excessive_word():
    """Creates a word between 6 and 10 syllables long.
    """

    return new_word(random.randrange(6,10))

def sentence(base = 5, cap = 10):
    """Creates a sentence of the given number of word caps.
    """

    i = 0
    sentence = ''
    while i < random.randrange(base, cap):
        if i == 0:
            sentence += new_word(random.randrange(1,5)).capitalize()
        else:
            sentence += random.choice(['', '', '', ','])
            sentence += " " + medium_word()
        i += 1

    sentence += random.choice(['.', '.', '.', '.', '.', '!', '?'])+ " "

    return sentence

def paragraph(base = 5, cap = 20):
    """Creates a paragraph with the given number of sentence caps.
    """

    i = 0
    paragraph = ''
    while i < random.randrange(base, cap):
        paragraph += sentence()
        i += 1

    return paragraph
