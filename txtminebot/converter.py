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

    oldstats = []
    playerfile = open(os.path.join(sys.argv[1], playerName+".stats"))
    for x in playerfile:
        oldstats.append(x.rstrip())
    playerfile.close()

    olddossier = []
    try:
        playerfile = open(os.path.join(sys.argv[1], playerName+".dossier"))
        for x in playerfile:
            olddossier.append(x.rstrip())
        playerfile.close()
    except BaseException:
        olddossier.append('')
        olddossier.append('')
        olddossier.append("0,0,0,0,0,0,0,0")
        olddossier.append("0")
        olddossier.append("0,0,0,0,0,0,0,0")
        olddossier.append("0")
        olddossier.append("")
        olddossier.append("1,0,0,0")

    empressStats = olddossier[7].split(",")
    mines = olddossier[0].split(",")
    minesCompleted = olddossier[6].split(",")
    if len(minesCompleted) > 1:
        minesCompleted = []
    resHeld = olddossier[2].split(",")

    for index,res in enumerate(resHeld):
        resHeld[index] = int(res)

    newPlayer = {
        "name": playerName,
        "aliases": [playerName],
        "last strike": int(oldstats[0]),
        "strength": int(oldstats[2]),
        "endurance": int(oldstats[3]),
        "lifetime strikes": int(oldstats[0]),
        "lifetime completed": int(oldstats[5]),
        "lifetime grovels": int(empressStats[1]),
        "mines owned": mines,
        "mines assigned": [],
        "mines completed": minesCompleted,
        "mines available": int(empressStats[0]),
        "res held": resHeld,
        "grovel count": int(empressStats[1]),
        "strike count": int(oldstats[0]),
        "playing": True
        }

    return vtils.write_dict_as_json(os.path.join(OUTDIR, playerName+".player"), newPlayer)

def convert_mine(mineName):
    '''
    Converts old mine data to new format.
    '''

    oldmine = []

    minefile = open(os.path.join(sys.argv[1], mineName+".mine"))
    for x in minefile:
        oldmine.append(x.rstrip())
    minefile.close()

    if oldmine[0] == "{":
        # eject if this is already a modern mine file
        return "nothing"

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

    oldgolem = []

    golemfile = open(os.path.join(sys.argv[1], golemOwner+".golem"))
    for x in golemfile:
        oldgolem.append(x.rstrip())
    golemfile.close()

    if oldgolem[0] == "{":
        # eject if this is already a modern golem file
        return "nothing"

    oldcore = oldgolem[1].split(",")

    for index,res in enumerate(oldcore):
        oldcore[index] = int(res)

    core = {
            "~": oldcore[0],
            "#": oldcore[1],
            "@": oldcore[2],
            "&": oldcore[3],
            "*": oldcore[4],
            "[": oldcore[5],
            "]": oldcore[6],
            "^": oldcore[7]
            }

    res = oldgolem[9].split(",")
    for index,item in enumerate(res):
        res[index] = int(item)

    newGolem = {
            "core": core,
            "birth": int(oldgolem[7]),
            "owner": golemOwner,
            "interval": int(oldgolem[5]),
            "height": int(oldgolem[2]),
            "width": int(oldgolem[3]),
            "strength": int(oldgolem[4]),
            "death": int(oldgolem[6]),
            "shape": oldgolem[0],
            "lastStrike": oldgolem[8],
            "res": res
            }

    return vtils.write_dict_as_json(os.path.join(OUTDIR, golemOwner+".golem"), newGolem)

if __name__ == "__main__":
    main()
