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

def writeMine(mine, record): #returns a filename for a list of resoureces recorded
    recordfile = open(record, 'w')
    for x in mine:
        recordfile.write(str(x))
        recordfile.write("\n")

    recordfile.close()
    return record

def openMine(record): #returns a list of resources when given a file
    recordfile = open(record, 'r')
    mine = []
    for x in recordfile:
        mine.append(x)

    return mine

def printMine(mine):
    total = 0
    for x in mine:
        total += int(x)

    print "tildes:  %d (%d%%)" % (int(mine[0]), 100*float(mine[0])/float(total))
    print "pounds:  %d (%d%%)" % (int(mine[1]), 100*float(mine[1])/float(total))
    print "spirals: %d (%d%%)" % (int(mine[2]), 100*float(mine[2])/float(total))
    print "ampers:  %d (%d%%)" % (int(mine[3]), 100*float(mine[3])/float(total))
    print "splats:  %d (%d%%)" % (int(mine[4]), 100*float(mine[4])/float(total))
    print "lbracks: %d (%d%%)" % (int(mine[5]), 100*float(mine[5])/float(total))
    print "rbracks: %d (%d%%)" % (int(mine[6]), 100*float(mine[6])/float(total))
    print "carats:  %d (%d%%)" % (int(mine[7]), 100*float(mine[7])/float(total))
    print "\ntotal: %d" % (total)

    return mine

#testing below
print "MINE #1"
printMine(openMine(writeMine(generate("standardrates"), "m1")))
print "\nMINE #2"
writeMine(printMine(generate("standardrates")), "m2")
print "\nMINE #3"
writeMine(printMine(generate("standardrates")), "m3")
print "\nMINE #4"
writeMine(printMine(generate("standardrates")), "m4")
