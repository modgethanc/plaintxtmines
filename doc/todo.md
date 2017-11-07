TODO LIST
=========

(absent access to git issues when i'm offline, dropping todo notes here)

irc-specific
------------

    * authentication: currently, txtminebot creates and accesses player data
      based on nick. obviously, this means anyone who switches nicks (whether it
      be novelty or by client bounce), will have trouble maintaining a single
      in-game existence. also, this means it's trivial to hijack someone's game
      data by jumping on their nick if they disconnect/are on a different nick.

      options:
        * aliasing: allow players to link their own frequent/current used nicks,
          and when switching nicks, re-authenticate to the bot
        * piggy-back off freenode's user identification system (obviously only
          works for instances that run on freenode)

game mechanics
--------------

    * mine veins are a little vague; especially near the end of a mine, when
      there's only one vein left and the dice-roll for targetting veins never
      picks it

      options:
        * never target empty veins
        * sprinkle the rubble message randomly through the entire mine (as in,
          sometimes you just get nothing), possibly with increasing frequency
          near the end

    * boss mines:
        * have txtminebot occasionally grant all players access to a larger
          mine, on decree of the empress
        * (or, maybe, only players in the empresses's favor)
        * only one player should get to breathe the mysterious smoke!

    * set a better fatigue limit, or have a special event trigger to clear
      fatigue (ie, grovel enough, and if you're fatigued, the empress cures you)

codebase structure
------------------

      [ui1 (player access)]---|      |---[ui3 (player access)]
      [ui2 (player access)]---|      |---[ui4 (player access)]
                              |      |
                            [txtminebot]
                                 |
                              [game]
                                 |
                 ________________|_______________
                /       /        |       \        \
            [world] [empress] [players] [mines] [golems]


    * txtminebot should only make inquiries/requests of the game engine, and
      interpret everything into human-readable responses that go back to the ui.

    * interfaces could be irc, slack, twitter, terminal-only, whatever
