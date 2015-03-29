#!/usr/bin/python

def itemizeRes(resources): # takes list of res and outputs as human-readable
    total = 0
    for x in resources:
        total += int(x)

    return str(resources[0])+" tilde, "+str(resources[1])+" pound, "+str(resources[2])+" spiral, "+str(resources[3])+" amper, "+str(resources[4])+" splat, "+str(resources[5])+" lbrack, "+str(resources[6])+" rbrack, and "+str(resources[7])+" carat, for a total of "+str(total)+" units"
