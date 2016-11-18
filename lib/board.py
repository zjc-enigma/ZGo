# -*- coding: utf-8 -*-

import numpy as np

class Board(object):
    WHITE = -1
    BLACK = 1
    EMPTY = 0

    def __init__(self, size=19):
        self.size = size
        self.board = np.zeros((size, size))
        self.board.fill(self.EMPTY)
        self.turns_num = 0
        self.current_move = self.BLACK


    def _is_valid_pos(position):
        return True

    def move(self, position):
        """position is a (x, y) tuple

        """
        x, y = position
        if self._is_valid_pos(position):
            self.board[x][y] = self.current_move

        else:
            print "error position"

if __name__ == "__main__":
    pass
