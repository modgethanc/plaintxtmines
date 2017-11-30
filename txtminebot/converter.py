#!/usr/bin/python
'''
This is a legacy data file converter.

plaintxtmines is a text-based multiplayer mining simulator. For more
information, see the full repository:

https://github.com/modgethanc/plaintxtmines
'''

import os
import vtils

GAMEDATA = os.listdir("../data")
OUTDIR = "../data/migrated"

def main():
    '''
    Main entry point.
    '''

    pass

def convert_player(playerName):
    '''
    Converts old player data to new format, combining both .stats and .dossier.
    '''

    pass

def convert_mine(mineName):
    '''
    Converts old mine data to new format.
    '''

    pass

def convert_golem(golemOwner):
    '''
    Converts old golem data to new format.
    '''

    pass

if __name__ == "__main__":
    main()
