#!/usr/bin/python

import random
import names

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

def writeMine(mine, record='../data/'+names.medium()+'.mine'): #returns a filename for a list of resources recorded
    recordfile = open(record, 'w')
    total = 0
    for x in mine:
        recordfile.write(str(x))
        total += x
        recordfile.write("\n")
    
    recordfile.write(str(total))
    recordfile.close()
    return record

def openMine(record): #returns a list of resources when given a file
    recordfile = open(record, 'r')
    mine = []
    for x in recordfile:
        mine.append(x)

    return mine

def printMine(mine):
    #total = 0
    #for x in mine:
    #    total += int(x)

    print "tildes:  %d (%d%%)" % (int(mine[0]), 100*float(mine[0])/float(mine[8]))
    print "pounds:  %d (%d%%)" % (int(mine[1]), 100*float(mine[1])/float(mine[8]))
    print "spirals: %d (%d%%)" % (int(mine[2]), 100*float(mine[2])/float(mine[8]))
    print "ampers:  %d (%d%%)" % (int(mine[3]), 100*float(mine[3])/float(mine[8]))
    print "splats:  %d (%d%%)" % (int(mine[4]), 100*float(mine[4])/float(mine[8]))
    print "lbracks: %d (%d%%)" % (int(mine[5]), 100*float(mine[5])/float(mine[8]))
    print "rbracks: %d (%d%%)" % (int(mine[6]), 100*float(mine[6])/float(mine[8]))
    print "carats:  %d (%d%%)" % (int(mine[7]), 100*float(mine[7])/float(mine[8]))
    print "\ntotal: %d" % (int(mine[8]))

    return mine

#testing below
print "MINE #1"
printMine(openMine(writeMine(generate("standardrates"), "../data/m1")))
print "\nNAMED MINE"
printMine(openMine(writeMine(generate("standardrates"))))
