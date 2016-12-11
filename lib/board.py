import numpy as np
import collections.abc
import abc
from operator import add
from enum import Enum
from collections import namedtuple

class IllegalMove(Exception):
    pass


class Color(Enum):
    black = 1
    white = -1
    empty = 0
    black_sig = 'O'
    white_sig = 'X'
    empty_sig = '.'



Position = namedtuple('Position', ['color', 'block_id', 'is_ko'])

# class Position:
#     def __init__(self, x, y, color=Color.empty):
#         self.x = x
#         self.y = y
#         self.color = color
#         # default empty pos, not belong to any blocks
#         self.block_id = None
#         # if is ko , next cannot move here
#         self.is_ko = False


class Block:

    def __init__(self, color, coordinate_set, air_set, block_id=None):
        self.block_id = block_id
        self.color = color
        self.coordinate_set = coordinate_set
        self.air_set = air_set
        # TODO
        self.is_alive = True

    @property
    def air(self):
        return len(self.air_set)

    def __add__(self, other):
        if self.color == other.color:
            new_coordinate_set = self.coordinate_set | other.coordinate_set
            new_air_set = self.air_set | other.air_set - new_coordinate_set
            return Block(self.color, new_coordinate_set, new_air_set)


class Board:

    def __init__(self, size=19):
        self.size = size
        self.state = [
            [
                Position(Color.empty, None, False)
                for i in range(size)
            ]
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


    def _add_block(self, block):

        new_block_id = max(list(self.block_dict.keys())) + 1
        block.block_id = new_block_id
        self.block_dict[new_block_id] = block
        return new_block_id


    def _merge_blocks(self, block_id_list):
        merged_block = reduce(add, [self.block_dict[block_id]
                                    for block_id in block_id_list])

        for block_id in block_id_list:
            del self.block_dict[block_id]

        new_block_id = self._add_block(merged_block)
        return new_block_id


    def _eat_block(self, block_id):
        block_to_eat = self.block_dict[block_id]
        del self.block_dict[block_id]

        for coord in block_to_eat.coordinate_set:
            pos = self[coord]
            pos.color = Color.empty
            pos.block_id = None


    def _calc_block(self, coordinate):
        neighbors_coordinate = self._get_neighbors_coordinate(coordinate)

        air_set = set()
        merge_block_id_list = []

        for coord in neighbors_coordinate:

            neighbor = self[coord]
            if neighbor.color == self.current_move:
                merge_block_list.append(neighbor.block_id)

            elif neighbor.color == Color.empty:
                air_set.add(coord)

            else:
                # reduce oppsite air
                enemy_block = self.block_dict[neighbor.block_id]
                enemy_block.air_set.remove(coord)
                if enemy_block.air == 0:
                    self._eat_block(neighbor.block_id)


        new_block = Block(self.current_move, set([coordinate]), air_set)
        new_block_id = self._add_block(new_block)

        if len(merge_block_id_list) > 0:
            # more than one blocks, need to merge
            merge_block_list.append(new_block_id)
            self._merge_blocks(merge_block_id_list)






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
