import numpy as np
import collections.abc
import abc
from operator import add
from enum import Enum
from collections import namedtuple
from functools import reduce
import pdb

class IllegalMove(Exception):
    pass


class Color(Enum):
    black = 'X'
    white = 'O'
    empty = '.'

    @classmethod
    def oppsite(cls, color):
        # TODO: 
        if color == cls.white:
            return  cls.black

        else:
            return cls.white


#Position = namedtuple('Position', ['color', 'block_id', 'is_ko'])

class Position:
    def __init__(self, color=Color.empty, block_id=None, is_ko=False):
        self.color = color
        self.block_id = block_id
        self.is_ko = is_ko


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
        self.current_color = Color.black

    def __getitem__(self, index):
        x, y = index
        return self.state[x][y]

    def _is_in_board(self, coordinate):
        # beyond board size
        x, y = coordinate
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            print("outside of the board:", coordinate)
            return False

        return True


    def _is_allowed_move(self, coordinate, neighbors_coordinate):
        '''
        warning: if neighbors_coordinate is a generator, this func will consume it
        '''
        # no empty pos
        if self[coordinate].color != Color.empty:
            return False

        # rule not allowed
        if self[coordinate].is_ko:
            return False

        # rule not allowed
        any_empty = any(self[coord].color == Color.empty
                        for coord in neighbors_coordinate)
        if not any_empty:
            friend_blocks = [self.block_dict[self[coord]]
                             for coord in neighbors_coordinate
                             if self[coord].color == self.current_color]

            enemy_blocks = [self.block_dict[self[coord]]
                            for coord in neighbors_coordinate
                            if self[coord].color != self.current_color]

            is_last_air = all(block.air_set == {coordinate} for block in friend_blocks)
            is_eatting_enemy = all(block.air_set == {coordinate} for block in enemy_blocks)

            if is_last_air and not is_eatting_enemy:
                return False

        return True

    def show_state(self):
        print("-"*37)
        for pos_list in self.state:
            print(" ".join(pos.color.value for pos in pos_list))
        print("-"*37)


    def _get_neighbors_coordinate(self, coordinate):
        x, y = coordinate
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return filter(self._is_in_board, neighbors)

    def _change_turn(self):
        self.current_color = Color.oppsite(self.current_color)


    def _generate_id(self):

        if self.block_dict:
            return max(list(self.block_dict.keys())) + 1
        else:
            return 0

    def _add_block(self, block):

        new_block_id = self._generate_id()
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


    def _reset_pos(self, pos):
        pos.color = Color.empty
        pos.block_id = None

    def _eat_block(self, block_id):
        block_to_eat = self.block_dict[block_id]
        del self.block_dict[block_id]

        for coord in block_to_eat.coordinate_set:
            pos = self[coord]
            print("eat", pos.color, "at", coord)
            self._reset_pos(pos)




    def _update_state(self, coordinate):

        neighbors_coordinate = list(self._get_neighbors_coordinate(coordinate))

        if not self._is_allowed_move(coordinate, neighbors_coordinate):
            print("rules not allowed to move:", coordinate)
            return False

        air_set = set()
        merge_block_id_list = []

        for coord in neighbors_coordinate:
            neighbor = self[coord]
            if neighbor.color == self.current_color:
                merge_block_id_list.append(neighbor.block_id)

            elif neighbor.color == Color.empty:
                air_set.add(coord)

            else:
                # reduce oppsite air
                enemy_block = self.block_dict[neighbor.block_id]
                enemy_block.air_set.remove(coordinate)
                if enemy_block.air == 0:
                    self._eat_block(neighbor.block_id)

        new_block = Block(self.current_color, set([coordinate]), air_set)
        new_block_id = self._add_block(new_block)


        if len(merge_block_id_list) > 0:
            # more than one blocks, need to merge
            merge_block_id_list.append(new_block_id)
            self._merge_blocks(merge_block_id_list)

        self[coordinate].color = self.current_color
        self[coordinate].block_id = new_block_id
        return True


    def move(self, coordinate):
        self._update_state(coordinate)
        self.show_state()
        self._change_turn()



if __name__ == "__main__":
    # TODO: need more tests
    b = Board()
    b.move((3,3))
    b.move((3,4))
    b.move((4,4))
    b.move((4,3))
    b.move((2,3))
    b.move((4,5))


    b.move((3,5))


    b.move((5,5))
    b.move((5,3))
    b.move((5,4))
