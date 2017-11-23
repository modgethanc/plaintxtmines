#!/usr/bin/python

'''
vtils.py: frequently used terminal and text processing utilities
copyright (c) 2017 vincent zeng (hvincent@modgethanc.com)

DEPENDENCIES:
    inflect
    colorama
    os
    json

i have no idea why anyone else in their right mind would touch this bs, but in
case you do, you have the following unrestricted permissions: use, copy, modify,
merge, publish, distribute

if you do any of those things in a way that people who aren't you might see
it, i would appreciate my bs facerolling credited to "vincent zeng
(hvincent@modgethanc.com)". i probably can't do anything about it if you
don't, but you'd be kind of a jerk.

i do not guarantee the safety of anything in your life, should you choose to
touch my stupid keysmashing. please be careful out there.
'''

import inflect
import time
import random
import colorama
import os
import json

## misc globals
BACKS = ['back', 'b', 'q']

## color stuff
colorama.init()
textcolors = [ colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW,
        colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.WHITE,
        colorama.Fore.CYAN]
lastcolor = colorama.Fore.RESET

p = inflect.engine()

def set_rainbow():
    '''
    prints a random terminal color code
    '''

    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color

    print(color)

def reset_color():
    '''
    prints terminal color code reset.
    '''

    print(colorama.Fore.RESET)

def attach_rainbow():
    '''
    returns a random terminal color code, presumably to be 'attached' to a
    string.
    '''

    global lastcolor

    color = lastcolor
    while color == lastcolor:
        color = random.choice(textcolors)

    lastcolor = color
    return color

def attach_reset():
    '''
    returns terminal color code reset, presumably to be 'attached' to a string.
    '''

    return colorama.Style.RESET_ALL

def hilight(text):
    '''
    takes a string and returns it wrapped in a hilight style.
    '''

    return colorama.Style.BRIGHT+text+colorama.Style.NORMAL

def rainbow(txt):
    '''
    takes a string and makes every letter a different color.
    '''

    rainbow = ""
    for letter in txt:
        rainbow += attach_rainbow() + letter

    rainbow += attach_reset()

    return rainbow

def pretty_time(time):
    '''
    human-friendly time formatter.

    takes an integer number of seconds and returns a phrase that describes it,
    using the largest possible figure, rounded down (ie, time=604 returns '10
    minutes', not '10 minutes, 4 seconds' or '604 seconds')
    '''

    m, s = divmod(time, 60)
    if m > 0:
        h, m = divmod(m, 60)
        if h > 0:
            d, h = divmod(h, 24)
            if d > 0:
                w, d = divmod(d, 7)
                if w > 0:
                    mo, w = divmod(w, 4)
                    if mo > 0:
                        return p.no("month", mo)
                    else:
                        return p.no("week", w)
                else:
                    return p.no("day", d)
            else:
                return p.no("hour", h)
        else:
            return p.no("minute", m)
    else:
        return p.no("second", s)

def genID(digits=5):
    '''
    returns a string-friendly string of digits, which can start with 0.
    defaults to 5 digits if length not specified.
    '''

    id = ""
    x  = 0
    while x < digits:
        id += str(random.randint(0,9))
        x += 1

    return id

def print_menu(menu, rainbow=False):
    '''
    a pretty menu handler that takes an incoming lists of
    options and prints them nicely.

    set rainbow=True for colorized menus.
    '''

    i = 0
    for x in menu:
        line = []
        if rainbow:
            line.append(attach_rainbow())
        line.append("\t[ ")
        if i < 10:
            line.append(" ")
        line.append(str(i)+" ] "+x)
        line.append(attach_reset())
        print("".join(line))
        i += 1

def list_select(options, prompt):
    '''
    given a list and query prompt, returns either False as an
    cancel flag, or an integer index of the list

    catches cancel option from list defined by BACKS; otherwise, retries on
    ValueError or IndexError.
    '''

    ans = ""
    invalid = True

    choice = raw_input("\n"+prompt)

    if choice in BACKS:
        return False

    try:
        ans = int(choice)
    except ValueError:
        return list_select(options, prompt)

    try:
        options[ans]
    except IndexError:
        return list_select(options, prompt)

    return ans

def input_yn(query):
    '''
    given a query, returns boolean True or False by processing y/n input.
    repeatedly queries until valid 'y' or 'n' is entered.
    '''

    try:
        ans = raw_input(query+" [y/n] ")
    except KeyboardInterrupt:
        input_yn(query)

    while ans not in ["y", "n"]:
        ans = raw_input("'y' or 'n' please: ")

    if ans == "y":
        return True
    else:
        return False

def open_json_as_dict(filename):
    '''
    Opens filename.json file and returns dict (blank if no file)
    '''

    if not os.path.isfile(filename):
        return {}
    else:
        return json.load(open(filename))

def write_dict_as_json(filename, j):
    '''
    Overwrites filename.json file with dict j
    '''

    datafile = open(filename, 'w')
    datafile.write(json.dumps(j, sort_keys=True, indent=2, separators=(',', ':')))

    return filename

