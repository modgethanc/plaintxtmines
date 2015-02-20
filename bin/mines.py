#!/usr/bin/python

import random

def generate(minerates):
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

    print "seed: %d" % (seed)
    print "tildes:  %d (%d%%)" % (resources[0], 100*float(resources[0])/float(total))
    print "pounds:  %d (%d%%)" % (resources[1], 100*float(resources[1])/float(total))
    print "spirals: %d (%d%%)" % (resources[2], 100*float(resources[2])/float(total))
    print "ampers:  %d (%d%%)" % (resources[3], 100*float(resources[3])/float(total))
    print "splats:  %d (%d%%)" % (resources[4], 100*float(resources[4])/float(total))
    print "lbracks: %d (%d%%)" % (resources[5], 100*float(resources[5])/float(total))
    print "rbracks: %d (%d%%)" % (resources[6], 100*float(resources[6])/float(total))
    print "carats:  %d (%d%%)" % (resources[7], 100*float(resources[7])/float(total))
    print "\ntotal: %d" % (total)


#testing below

print "MINE #1"
generate("standardrates")
print "\nMINE #2"
generate("standardrates")
print "\nMINE #3"
generate("standardrates")
print "\nMINE #4"
generate("standardrates")
