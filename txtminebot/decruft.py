import players
import mines
import os


gamedata = os.listdir("../data")

liveMines = []

for filename in gamedata:
    entry = os.path.basename(filename).split('.')

    if not entry[0]:
        # skip blank files
        continue

    if entry[-1] == "player":
        incomingPlayer = players.Player()
        incomingPlayer.load(entry[0])
        liveMines.extend(incomingPlayer.minesOwned)

print liveMines

for filename in gamedata:
    entry = os.path.basename(filename).split('.')

    if not entry[0]:
        # skip blank files
        continue

    if entry[-1] == "mine":
        if entry[0] not in liveMines:
            print "archiving " + entry[0]
            os.renames("../data/"+entry[0]+".mine", "../data/mine-archive/"+entry[0]+".mine")
