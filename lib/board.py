import numpy as np
import collections.abc
import abc
from enum import Enum

class IllegalMove(Exception):
    pass


class Color(Enum):
    black = 1
    white = -1
    empty = 0

class Position:

    def __init__(self, x, y, color=Color.empty):
        self.x = x
        self.y = y
        self.color = color
        self.is_calced_air = False
        # default empty pos, not belong to any blocks
        self.block_id = -1
        # default empty pos, not need to calc air
        self.air = -1
        # if is ko , next cannot move here
        self.is_ko = False



class Block:

    def __init__(self, color, coordinate_set, air_set):

        self.color = color
        self.coordinate_set = coordinate_set
        self.air_set = air_set
        self.air = len(air_set)
        # TODO
        self.is_alive = True

    def __add__(self, other):
        if self.color == other.color:
            new_coordinate_set = self.coordinate_set | other.coordinate_set
            new_air_set = self.air_set | other.air_set - new_coordinate_set
            return Block(self.color, new_coordinate_set, new_air_set)



class Board:

    def __init__(self, size=19):
        self.size = size
        self.state = [[Position(i, j) for i in range(size)]
                      for j in range(size)]

        self.block_dict = {}

        self.move_num = 0
        self.current_move = Color.black


    def __getitem__(self, index):
        x, y = index
        return self.state[x][y]

    def _is_valid_pos(self, coordinate):
        pass


    def show_state(self):
        pass


    def _get_neighbors_coordinate(self, coordinate):
        x, y = coordinate
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return filter(self._is_valid_pos, neighbors)


    def _update_current_move(self):
        self.current_move = -self.current_move

    def _calc_air(self, blocks):
        pass


    def _calc_block(self, coordinate):
        neighbors_coordinate = self._get_neighbors_coordinate(coordinate)
        new_block = {coordinate}
        new_block_id = max(list(self.block_dict.keys())) + 1

        for coord in neighbors_coordinate:
            neighbor = self[coord]
            if neighbor.color == self.current_move:
                new_block |= self.block_dict[neighbor.block_id]
                del self.





    def move(self, coordinate):

        self._update_current_move()




class TestSlice:
    def __getitem__(self, index):
        return index




class Board_BAK:
    WHITE = -1
    BLACK = 1
    EMPTY = 0

    def __init__(self, size=19):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.board.fill(self.EMPTY)
        self.turns_num = 0
        self.sets = set()
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
