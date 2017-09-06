#!/usr/bin/env python3

from pelita.player import SimpleTeam
from .YahooPlayer import YahooPlayer

# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def factory():
    return SimpleTeam("Yahoo Team", YahooPlayer(), YahooPlayer())

# For testing purposes, one may use alternate factory methods::
#
#     def alternate_factory():
#          return SimpleTeam("Our alternate Team", AlternatePlayer(), AlternatePlayer())
#
# To be used as follows::
#
#     $ pelita path_to/groupN/:alternate_factory
