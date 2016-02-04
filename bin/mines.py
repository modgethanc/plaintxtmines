#!/usr/bin/python

import gibber
import util
import inflect

import json
import random
import os

DATA = os.path.join("..", "data")
CONFIG = os.path.join("config")
MINES = {}
RESOURCES = {}
STATUS = ["new", "active", "depleted"]

p = inflect.engine()

## file i/o

def load_mines(minefile=os.path.join(DATA,"mineautosave.json")):
    # takes a json from minefile and loads it into memory
    # returns number of mines loaded

    global MINES

    infile = open(minefile, "r")
    MINES = json.load(infile)
    infile.close()

    return len(MINES)

def load_res(resfile=os.path.join(CONFIG, "resources.json")):
    # takes a json from resfile and loads into memory
    # returns number of different kinds of res

    global RESOURES

    infile = open(resfile, "r")
    RESOURCES = json.load(infile)
    infile.close()

    return len(RESOURCES)

def load_rate(ratefile=os.path.join(CONFIG, "baserate.json")):
    # takes a json from ratefile and returns dict of it

    infile = open(ratefile, "r")
    rates = json.load(infile)
    infile.close()

    return rates

def save(savefile=os.path.join(DATA, "mineautosave.json")):
    # save current MINES to savefile, returns save location

    outfile = open(savefile, "w")
    outfile.write(json.dumps(MINES, sort_keys=True, indent=2, separators=(',', ':')))
    outfile.close()

    return savefile

def new_mine(ownerID, zoneID, minerate=load_rate()):
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

## mine output

def mine(mineID):
    # takes str mineID and returns mine data, or none

    if mineID in MINES:
        return {mineID:MINES[mineID]}
    else:
        return None

def get(mineID, field):
    # takes str mineID and field and returns whatever it is
    # returns None if mine or field doesn't exist

    if mineID in MINES:
        return MINES[mineID].get(field)
    else:
        return None

def find(searchdict):
    # returns a list of str IDs that match search dict

    matches = []

    for x in MINES:
        found = True
        mine = MINES[x]

        for y in searchdict:
            if mine.get(y) == searchdict.get(y):
                found = True
            else:
                found = False
                break

        if found:
            matches.append(x)

    return matches

def exists(minename):
    # check to see if mine has already been created

    for x in MINES:
        if MINES[x].get("name") == minename:
            return True

    return False

## meta helpers

def generate_res(resrate): # takes a resrate dict; returns a dict of resource amounts for a generated mine

    bound = resrate.get("size")
    seed = random.randrange(1,bound)

    resources = {}

    for x in resrate:
        if x != "size":
            spawn = seed * resrate[x] + random.randrange(1,bound)
            resources.update({x: spawn})

    return resources


def sum_res(res):
    # takes a dict of str res and int quantities, returns int sum

    total = 0
    for x in res:
        total += res.get(x)

    return total

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

def test():
    global MINES

    load_mines()
    load_res()

    print("mines: ", MINES)
    MINES.update(new_mine("001", "003"))
    MINES.update(new_mine("001", "003"))
    MINES.update(new_mine("001", "003"))
    MINES.update(new_mine("001", "003"))
    MINES.update(new_mine("001", "003"))
    print("mines: ", MINES)

    return
