#!/usr/bin/python

import random
import gibber
import os

def generate(minerates): #takes a minerate file; returns a list of resource amounts for a generated mine
    ratefile = open(minerates,'r')
    rates = []
    for x in ratefile:
        rates.append(int(x.rstrip()))
    ratefile.close()

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

def writeMine(mine, record='../data/'+gibber.medium()+'.mine'): #returns a mine name for a list of resources recorded
    totals = [0,0]
    totalseek = []

    if os.path.isfile(record):
      recordfile = open(record, 'r')
      for x in recordfile:
        totalseek.append(x)
      recordfile.close()

      totals = totalseek[-1].rstrip().split(',')
      new = False
    else:
      new = True

    recordfile = open(record, 'w')
    totals[0] = 0
    i = 0
    for x in mine:
        if i < 8:
            recordfile.write(str(x)+'\n')
            totals[0] += int(x)
            i += 1

    if new:
      totals[1] = str(totals[0])
    totals[0] = str(totals[0])

    #print totals
    j = ','
    total = j.join(totals)
    recordfile.write(total+'\n')
    recordfile.close()

    return record.split('/')[-1].split('.')[0]

def openMine(record): #returns a list of mine data plus name given a filename
    recordfile = open(record, 'r')
    mine = []
    for x in recordfile:
        mine.append(x)

    mine.append(record.split('/')[-1].split('.')[0])

    return mine

def remaining(record):
    return int(openMine(record)[-2].rstrip().split(',')[0])

def starting(record):
    return int(openMine(record)[-2].rstrip().split(',')[1])

def excavate(record, rate=10, types=3):
    excavated = [0,0,0,0,0,0,0,0]
    mineData = openMine(record)
    mined = []
    mine = []

    i = 0
    while i < 9:
        mine.append(mineData[i])
        i += 1

    if remaining(record) <= rate:
        i = 0
        while i < 8:
            excavated[i] = int(mine[i])
            mine[i] = 0
            i += 1
        writeMine(mine, record)
        return excavated

    mineChoices = [0,1,2,3,4,5,6,7]
    i = types
    while i > 0:
        mineHere = random.choice(mineChoices)
        mined.append(mineHere)
        mineChoices.remove(mineHere)
        i -= 1

    i = rate
    minesLeft = types
    while i > 0:
        if minesLeft > 0:
            mineHere = random.choice(mined)
        else:
            break
        if int(mine[mineHere]) > excavated[mineHere]:
            excavated[mineHere] += 1
            i -= 1
        else:
            mined.remove(mineHere)
            minesLeft -= 1
    i = 0
    while i < 8:
       res = int(mine[i])
       res -= excavated[i]
       mine[i] = res
       i += 1

    writeMine(mine, record)

    return excavated

def printMine(mine):
    print mine[-1]
    remaining = mine[-2].split(',')[0]
    if int(remaining) == 0:
        print "mine depleted"
    else:
        print "~ %d (%d%%)" % (int(mine[0]), 100*float(mine[0])/float(remaining))
        print "# %d (%d%%)" % (int(mine[1]), 100*float(mine[1])/float(remaining))
        print "@ %d (%d%%)" % (int(mine[2]), 100*float(mine[2])/float(remaining))
        print "& %d (%d%%)" % (int(mine[3]), 100*float(mine[3])/float(remaining))
        print "* %d (%d%%)" % (int(mine[4]), 100*float(mine[4])/float(remaining))
        print "[ %d (%d%%)" % (int(mine[5]), 100*float(mine[5])/float(remaining))
        print "] %d (%d%%)" % (int(mine[6]), 100*float(mine[6])/float(remaining))
        print "^ %d (%d%%)" % (int(mine[7]), 100*float(mine[7])/float(remaining))
        print "\ntotal: %s" % (remaining)

    return mine
