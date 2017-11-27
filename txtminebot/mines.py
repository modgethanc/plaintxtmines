#!/usr/bin/python

'''
This contains the class and functions for mines.

Mines contain veins of resources, and are generated on demand when a new mine is
opened.

Mine attributes:
    (given stats)
    startingRes: 8-item int array of starting res count
    startingTotal: int of initial total
    owner: string of owner's name (based on dossier ID)
    name: stirng of mine's name
    (mutable)
    currentRes: 8-item int array of current res counts
    currentTotal: int of current res total
    workers: string array of every dossier ID permitted to strike

By convention, we use reslist as an array of ints, each item corresponding to
the number of resources assuming the following order:
    reslist[0]: ~
    reslist[1]: @
    reslist[2]: #
    reslist[3]: &
    reslist[4]: *
    reslist[5]: [
    reslist[6]: ]
    reslist[7]: ^

Future versions should use a dict for resources.

plaintxtmines is a text-based multiplayer mining simulator. For more
information, see the full repository:

https://github.com/modgethanc/plaintxtmines
'''

import os
import random

import vtils
import gibber

class Mine():
    '''
    Implements a mine object.
    '''

    def __init__(self):
        '''
        Initial mine conditions.
        '''

        ## given stats
        self.startingRes = [0,0,0,0,0,0,0,0]
        self.startingTotal = 0
        self.owner = None
        self.name = None

        ## mutables
        self.currentRes = [0,0,0,0,0,0,0,0]
        self.currentTotal = 0
        self.workers = []

    def save(self):
        '''
        Write self to disk.
        '''

        # hardcode bs
        filename = "../data/" + self.name+ ".mine"
        mineData = self.to_dict()
        vtils.write_dict_as_json(filename, mineData)

        return filename

    def to_dict(self):
        '''
        Turns all data into a dict.
        '''

        mineData = {
                "starting res": self.startingRes,
                "starting total": self.startingTotal,
                "owner": self.owner,
                "name": self.name,
                "current res": self.currentRes,
                "current total": self.currentTotal,
                "workers": self.workers
                }

        return mineData

    def load(self, mineName):
        '''
        Loads a mine from file for the named mine, then returns own name for
        verification.
        '''

        filename = mineName + ".mine"

        # hardcode bs
        mineData = vtils.open_json_as_dict("../data/"+filename)

        ## given stats
        self.startingRes = mineData["starting res"]
        self.startingTotal = mineData["starting total"]
        self.owner = mineData["owner"]
        self.name = mineData["name"]

        ## mutables
        self.currentRes = mineData["current res"]
        self.currentTotal = mineData["current total"]
        self.workers = mineData["workers"]

        return self.name

    def create(self, player, minerate="standardrates"):
        '''
        Generate a new mine for a given player with optional minerate. If no
        minerate is given, pass standard minerates down.

        Mine name is created with the gibber function, and checks against all
        previously created mines for name collisions.
        '''

        # generate name
        minename = gibber.medium()
        while os.path.isfile('../data/'+minename+'.mine'): # check for mine colision
            minename = gibber.medium()

        reslist = roll_resources(minerate)
        total = sum_resources(reslist)

        ## given stats
        self.startingRes = reslist
        self.startingTotal = total
        self.owner = player
        self.name = minename

        ## mutables
        self.currentRes = reslist
        self.currentTotal = total
        self.workers = [player]

        self.save()

        return minename

    def excavate(self, rate=10, width=3):
        '''
        Given optional strike rate and width, return an excavation from this
        mine. Those resources are moved from this mine's data.
        '''

        excavated = [0,0,0,0,0,0,0,0]
        reslist = self.currentRes

        veins = []

        if self.currentTotal <= rate:
            # clear the mine right away if mine has less than strikerate

            excavated = reslist
            self.currentRes = [0,0,0,0,0,0,0,0]
            self.save()
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
        while i > 0:
            # strike, and count res extracted
            if veinsLeft > 0:
                strike = random.choice(veins)
            else:
                break

            if int(reslist[strike]) > excavated[strike]:
                # check for remaining res
                excavated[strike] += 1
                i -= 1
            else:
                # stop striking empty vein
                veins.remove(strike)
                veinsLeft -= 1

        i = 0
        while i < 8:
           # remove resources from mine
           vein = int(reslist[i])
           vein -= excavated[i]
           reslist[i] = vein
           i += 1

        # record mine actions
        self.currentRes = reslist
        self.currentTotal = sum_resources(reslist)
        self.save()

        return excavated

## mine helper functions

def roll_resources(minerate):
    '''
    Takes a minerate file; returns a list of resource amounts for a
    generated mine.
    '''

    # open minerate file and process
    ratefile = open(minerate,'r')
    rates = []
    for x in ratefile:
        rates.append(int(x.rstrip()))
    ratefile.close()

    # roll according to rate bounds
    bound = rates[8]
    seed = random.randrange(1,bound)
    resources = [0,0,0,0,0,0,0,0]

    i = 0
    for x in resources:
        resources[i] = str(seed * rates[i] + random.randrange(1,bound))
        i += 1

    return resources

def sum_resources(reslist):
    '''
    Takes a given resource list and returns a sum of its total.
    '''

    total = 0
    for x in reslist:
        total += int(x)

    return total

## legacy functions below

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
