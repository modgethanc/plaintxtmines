#!/usr/bin/python

import random

def generate(minerates): #takes a minerate file; returns a list of resource amounts for a generated mine
    ratefile = open(minerates,'r')
    rates = []
    for x in ratefile:
        rates.append(int(x.rstrip()))

    bound = rates[8]

    seed = random.randrange(1,bound)

    resources = [0,0,0,0,0,0,0,0]
    total = 0

    i = 0

    for x in resources:
        resources[i] = seed * rates[i] + random.randrange(1,bound)
        total += resources[i]
        i += 1

    return resources

def writeMine(mine, record):
    recordfile = open(record, 'w')
    for x in mine:
        recordfile.write(str(x))
        recordfile.write("\n")

    recordfile.close()

def printMine(mine):
    total = 0
    for x in mine:
        total += x

    print "tildes:  %d (%d%%)" % (mine[0], 100*float(mine[0])/float(total))
    print "pounds:  %d (%d%%)" % (mine[1], 100*float(mine[1])/float(total))
    print "spirals: %d (%d%%)" % (mine[2], 100*float(mine[2])/float(total))
    print "ampers:  %d (%d%%)" % (mine[3], 100*float(mine[3])/float(total))
    print "splats:  %d (%d%%)" % (mine[4], 100*float(mine[4])/float(total))
    print "lbracks: %d (%d%%)" % (mine[5], 100*float(mine[5])/float(total))
    print "rbracks: %d (%d%%)" % (mine[6], 100*float(mine[6])/float(total))
    print "carats:  %d (%d%%)" % (mine[7], 100*float(mine[7])/float(total))
    print "\ntotal: %d" % (total)

    return mine

#testing below
print "MINE #1"
writeMine(printMine(generate("standardrates")), "m1")
print "\nMINE #2"
writeMine(printMine(generate("standardrates")), "m2")
print "\nMINE #3"
writeMine(printMine(generate("standardrates")), "m3")
print "\nMINE #4"
writeMine(printMine(generate("standardrates")), "m4")
