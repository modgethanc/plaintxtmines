#!/usr/bin/python

import random

def generate(minerates):
    rates = open(minerates,'r')
    tilde = int(rates.readline().rstrip('\r\n'))
    pound = int(rates.readline().rstrip('\r\n'))
    spiral = int(rates.readline().rstrip('\r\n'))
    amper = int(rates.readline().rstrip('\r\n'))
    splat = int(rates.readline().rstrip('\r\n'))
    lbrack = int(rates.readline().rstrip('\r\n'))
    rbrack = int(rates.readline().rstrip('\r\n'))
    carat = int(rates.readline().rstrip('\r\n'))
    bound = int(rates.readline().rstrip('\r\n'))

    seed = random.randrange(1,bound)
    tildes = seed * tilde + random.randrange(1,bound)
    pounds = seed * pound + random.randrange(1,bound)
    spirals = seed * spiral + random.randrange(1,bound)
    ampers = seed * amper + random.randrange(1,bound)
    splats = seed * splat + random.randrange(1,bound)
    lbracks = seed * lbrack + random.randrange(1,bound)
    rbracks = seed * rbrack + random.randrange(1,bound)
    carats = seed * carat + random.randrange(1,bound)

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


#testing below

generate("standardrates")
generate("standardrates")
generate("standardrates")
generate("standardrates")
