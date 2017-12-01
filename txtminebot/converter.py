#!/usr/bin/python
'''
This is a legacy data file converter.

plaintxtmines is a text-based multiplayer mining simulator. For more
information, see the full repository:

https://github.com/modgethanc/plaintxtmines
'''

import os
import sys
import vtils

GAMEDATA = ""
OUTDIR = ""

def main():
    '''
    Main entry point.
    '''

    global GAMEDATA
    global OUTDIR

    try:
        GAMEDATA = os.listdir(sys.argv[1])
    except OSError:
        print "not a valid game directory. quitting."
        return

    OUTDIR = os.path.join(sys.argv[1], "updated")

    if not os.path.isdir(OUTDIR):
        os.mkdir(OUTDIR)

    print "outputting to " + OUTDIR 

    for filename in GAMEDATA:
        print "checking: " + filename
        entry = os.path.basename(filename).split('.')

        if not entry[0]:
            # skip blank files
            continue

        if entry[-1] == "golem":
            print "converted: " + convert_golem(entry[0])
        elif entry[-1] == "mine":
            print "converted: " + convert_mine(entry[0])
        elif entry[-1] == "stats":
            print "converted: " + convert_player(entry[0])


def convert_player(playerName):
    '''
    Converts old player data to new format, combining both .stats and .dossier.
    '''

    return "nothing"

def convert_mine(mineName):
    '''
    Converts old mine data to new format.
    '''

    oldmine = []

    minefile = open(os.path.join(sys.argv[1], mineName+".mine"))
    for x in minefile:
        oldmine.append(x.rstrip())
    minefile.close()

    oldres = oldmine[0].split(",")

    total = 0
    for index, res in enumerate(oldres):
        total += int(res)
        oldres[index] = int(res)

    newmine = {
            "starting res": oldres,
            "starting total": oldmine[1],
            "owner": oldmine[2],
            "name": mineName,
            "current res": oldres,
            "current total": total,
            "workers": oldmine[2]
            }

    return vtils.write_dict_as_json(os.path.join(OUTDIR, mineName+".mine"), newmine)

def convert_golem(golemOwner):
    '''
    Converts old golem data to new format.
    '''

    return "nothing"

if __name__ == "__main__":
    main()
