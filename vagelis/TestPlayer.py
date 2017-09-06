from pelita import datamodel
from pelita.player import AbstractPlayer, SimpleTeam


class RandomPlayer(AbstractPlayer):
    """ A player that makes moves at random. """

    def get_move(self):
        return self.rnd.choice(list(self.legal_moves.keys()))
