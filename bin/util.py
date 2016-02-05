#!/usr/bin/python

import random

def genID(digits=5):
    # makes a string of digits

    id = ""
    x  = 0
    while x < digits:
        id += str(random.randint(0,9))
        x += 1

    return id

def sum_res(res):
    # takes a dict of str res and int quantities, returns int sum

    total = 0
    for x in res:
        total += res.get(x)

    return total

