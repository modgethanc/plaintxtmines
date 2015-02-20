#!/usr/bin/python

import random

tilde = 40
pound = 20
spiral = 15
amper = 10
splat = 6
lbrack = 4
rbrack = 4
carat = 1

def new():
    seed = random.randrange(1,100)
    tildes = seed * tilde + random.randrange(1,100)
    pounds = seed * pound + random.randrange(1,100)
    spirals = seed * spiral + random.randrange(1,100)
    ampers = seed * amper + random.randrange(1,100)
    splats = seed * splat + random.randrange(1,100)
    lbracks = seed * lbrack + random.randrange(1,100)
    rbracks = seed * rbrack + random.randrange(1,100)
    carats = seed * carat + random.randrange(1,100)

    total = tildes + pounds + spirals + ampers + splats + lbracks + rbracks + carats

    print "tildes:  %d (%d)" % (tildes, 100*float(tildes)/float(total))
    print "pounds:  %d (%d)" % (pounds, 100*float(pounds)/float(total))
    print "spirals: %d (%d)" % (spirals, 100*float(spirals)/float(total))
    print "ampers:  %d (%d)" % (ampers, 100*float(ampers)/float(total))
    print "splats:  %d (%d)" % (splats, 100*float(splats)/float(total))
    print "lbracks: %d (%d)" % (lbracks, 100*float(lbracks)/float(total))
    print "rbracks: %d (%d)" % (rbracks, 100*float(rbracks)/float(total))
    print "carats:  %d (%d)" % (carats, 100*float(carats)/float(total))
    print "\ntotal: %d" % (total)

new()
