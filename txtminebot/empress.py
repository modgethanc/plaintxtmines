#!/usr/bin/python
"""
This contains the class and functions for the empress.

The empress is a single, autonomous unit that players must work to please.

Empress attributes:
    (mutable)
    mood: int representing empress's current mood
    grovels: int of total times empress has been groveled to
    favorite: string of the empress's favorite player's name

"""

import os
import random
import time

import vtils
import gibber

class Empress():
    """Implements an empress object.
    """

    def __init__(self):
        """Initial conditions.
        """

        ## given
        self.name = None
        self.birth = None

        ## mutables
        self.mood = 0
        self.grovels = 0
        self.favorite = None

    def load(self, empress):
        """Loads an empress from the given empress filename.
        """

        filename = empress + ".empress"

        # hardcode bs
        empress_data = vtils.open_json_as_dict("../data/"+filename)

        ## given
        self.name = empress_data["name"]
        self.birth = empress_data["birth"]

        ## mutables
        self.mood = empress_data["mood"]
        self.grovels = empress_data["grovels"]
        self.favorite = empress_data["favorite"]

    def create(self):
        """Creates a new empress, returning her name.
        """

        empress_name = gibber.excessive_word()

        while os.path.isfile('../data/'+empress_name+'.empress'):
            empress_name = gibber.excessive()

        ## given
        self.name = empress_name
        self.birth = int(time.time())

        ## mutables
        self.mood = 0
        self.grovels = 0
        self.favorite = None

        return empress_name.capitalize()

    def save(self):
        '''
        Write self to disk.
        '''

        # hardcode bs
        filename = "../data/" + self.name+ ".empress"
        vtils.write_dict_as_json(filename, self.to_dict())

        return filename

    def __str__(self):
        """Returns a string representation of data.
        """

        return str(self.name).capitalize()

    def to_dict(self):
        """Returns a dict representation of data.
        """

        return {
                "name": self.name,
                "birth": self.birth,
                "mood": self.mood,
                "grovels": self.grovels,
                "favorite": self.favorite
                }

    def speak(self):
        return gibber.sentence()
