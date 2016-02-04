#!/usr/bin/python

import gibber
import util
import inflect

import random
import os

PATH = os.path.join("..", "data")
MINES = {}
RESOURCES = ["tilde", "pound", "spiral", "amper", "splat", "lbrack", "rbrack", "carat"]
STATUS = ["new", "active", "depleted"]

p = inflect.engine()

## file i/o

def load_mines(minefile="default.json"):
    # takes a json from minefile and loads it into memory
    # returns number of mines loaded

    global MINES

    infile = open(os.path.join(PATH, minefile), "r")
    MINES = json.load(infile)
    infile.close()

    return len(MINES)

def exists(minename):
    #TODO check to see if mine has already been created
    return

def new_mine(ownerID, zoneID, minerate="standardrates"):
    # generates a new mine entry from givens

    minedata = {}

    mineID = util.genID(10)
    while mineID in MINES:
        mineID = util.genID(10)

    minename = gibber.medium().capitalize()
    while exists(minename):
        minename = gibber.medium()

    starting_res = generate_res(minerate)
    starting_total = sum_res(starting_res)

    minedata.update({"name":minename})
    minedata.update({"owner":ownerID})
    minedata.update({"location":zoneID})
    minedata.update({"status":STATUS[0]})
    minedata.update({"starting resources":starting_res})
    minedata.update({"starting total":starting_total})
    minedata.update({"current resources":starting_res})
    minedata.update({"current total":starting_total})
    minedata.update({"workers":[]})

    return {mineID:minedata}

    #### LINE OF DEATH

    minefile.close()

    return minename # for mine name confirmation

def generate_res(minerate):
    # takes a minerate file; returns a list of resource amounts for a generated mine

    ratefile = open(minerate,'r')
    rates = []
    for x in ratefile:
        rates.append(int(x.rstrip()))
    ratefile.close()

    bound = rates[8]
    seed = random.randrange(1,bound)
    #resources = [0,0,0,0,0,0,0,0]
    resources = {}

    i = 0
    while i < len(RESOURCES):
        resources.update({RESOURCES[i]: seed * rates[i] + random.randrange(1,bound)})
        i += 1

    return resources

## mine output

def openMine(mine): # returns str list of entire mine file
    minefile = open('../data/'+mine+'.mine', 'r')

    minedata = []
    for x in minefile:
        minedata.append(x.rstrip())

    minefile.close()
    return minedata

def get_res(mineID):
    # takes str mineID and returns dict of resources
    # returns None if mine doesn't exist

    if mineID in MINES:
        return MINES[mineID].get("current resources")
    else:
        return None
    minedata = openMine(mine)

    return minedata[0].rstrip().split(',')

def getStarting(mine): # return original starting res
    minedata = openMine(mine)

    return minedata[10]

def getTotal(mineID):
    # return int of res total from given str mineID

    return sum_res(get_res(mineID))

def getOwner(mine): # return str of owner
    minedata = openMine(mine)

    return minedata[2]

def getWorkers(mine): # return str list of contracted workers
    minedata = openMine(mine)

    workerlist = minedata[2].rstrip().split[',']

    while workerlist.count('') > 0:
        workerlist.remove('') #dirty hack

    return workerList

def sum_res(res):
    # takes a dict of str res and int quantities, returns int sum

    total = 0
    for x in res:
        total += res.get(x)

    return total

## mine input

def writeMine(mine, minedata):
    minefile = open('../data/'+mine+'.mine', 'w')
    for x in minedata:
        minefile.write(str(x) + "\n")
    minefile.close()

## mine actions

def excavate(mine, rate=10, width=3):
    ## TODO: getRes
    excavated = [0,0,0,0,0,0,0,0]
    res = getRes(mine)

    mineData = openMine(mine)
    veins = []

    if getTotal(mine) <= rate: # clear the mine

        excavated = getRes(mine)
        mineData[0] = "0,0,0,0,0,0,0,0"
        writeMine(mine, mineData)
        return excavated

    i = width
    mineChoices = [0,1,2,3,4,5,6,7]
    while i > 0: # pick veins
        vein = random.choice(mineChoices)
        veins.append(vein)
        mineChoices.remove(vein)
        i -= 1

    i = rate
    veinsLeft = width
    while i > 0: # strike!
        if veinsLeft > 0:
            strike = random.choice(veins)
        else:
            break

        if int(res[strike]) > excavated[strike]: # check for remaining res
            excavated[strike] += 1
            i -= 1
        else: # stop striking empy vein
            veins.remove(strike)
            veinsLeft -= 1

    i = 0
    while i < 8: # clear out res
       vein = int(res[i])
       vein -= excavated[i]
       res[i] = str(vein)
       i += 1

    j = ','
    mineData[0] = j.join(res)
    writeMine(mine, mineData)

    return excavated

######## LINE OF DEATH

def remaining(record): # REDUNDANT
    return getTotal(record.split('/')[-1].split('.')[0])

def starting(record): # REDUNDANT
    return getStarting(record.split('/')[-1].split('.')[0])

def printMine(mine):
    print(mine[-1])
    remaining = mine[-2].split(',')[0]
    if int(remaining) == 0:
        print("mine depleted")
    else:
        print("~ %d (%d%%)" % (int(mine[0]), 100*float(mine[0])/float(remaining)))
        print("# %d (%d%%)" % (int(mine[1]), 100*float(mine[1])/float(remaining)))
        print("@ %d (%d%%)" % (int(mine[2]), 100*float(mine[2])/float(remaining)))
        print("& %d (%d%%)" % (int(mine[3]), 100*float(mine[3])/float(remaining)))
        print("* %d (%d%%)" % (int(mine[4]), 100*float(mine[4])/float(remaining)))
        print("[ %d (%d%%)" % (int(mine[5]), 100*float(mine[5])/float(remaining)))
        print("] %d (%d%%)" % (int(mine[6]), 100*float(mine[6])/float(remaining)))
        print("^ %d (%d%%)" % (int(mine[7]), 100*float(mine[7])/float(remaining)))
        print("\ntotal: %s" % (remaining))

    return mine
