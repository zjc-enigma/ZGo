import numpy as np


class IllegalMove(Exception):
    pass


class Board:
    WHITE = -1
    BLACK = 1
    EMPTY = 0

    def __init__(self, size=19):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.board.fill(self.EMPTY)
        self.turns_num = 0
        self.current_move = self.BLACK

    def _is_valid_pos(self, position):

        x, y = position
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False

        if self.board(position) != self.EMPTY:
            return False

        else:
            return True


    def _get_neighbors(self, position):
        x, y = position
        left = (x-1 , y)
        right = (x+1, y)
        up = (x, y-1)
        down = (x y+1)
        neighbors = [left, right, up, down]
        return filter(self._is_valid_pos, neighbors)

    def _calc_air(self, position, calced_pos=None):
        neighbors = self._get_neighbors(position)
        air = 0
        for pos in neighbors:
            if self.board[pos] == self.EMPTY:
                air += 1

            elif self.board[pos] == self.board[position]:
                air += self._calc_air(pos)


        return air



    def _update_state(self):
        self.current_move = -self.current_move
        self.turns_num += 1
        print(self.board)

    def move(self, position):
        """position is a (x, y) tuple

        """
        x, y = position
        if self._is_valid_pos(position):
            self.board[x][y] = self.current_move
            self._update_state()

        else:
            raise IllegalMove("Cannot place handicap on a started game")
            print("error position")



if __name__ == "__main__":
    pass
