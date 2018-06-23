import numpy as np
import collections.abc
import abc
from operator import add
from enum import Enum
from collections import namedtuple
from functools import reduce
import copy
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


class Position:

    def __init__(self, color=Color.empty, block_id=None):
        self.color = color
        self.block_id = block_id

    def __repr__(self):
        return ('<color: %s>' % self.color)



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
            # | 求并集的优先级很低, 需要加括号否则会出错
            new_air_set = (self.air_set | other.air_set) - new_coordinate_set
            # new_air_set = self.air_set | other.air_set
            # for i in new_coordinate_set:
            #     if i in new_air_set:
            #         new_air_set.remove(i)
            return Block(self.color, new_coordinate_set, new_air_set)


class Board:

    def __init__(self, size=19):
        self.size = size
        self.game_stack = []
        self.ko_coordinate = None
        self.state = np.array([
            [
                Position(Color.empty, None)
                for i in range(size)
            ]
            for j in range(size)])

        self._renew_update_set(None, self.state)
        self.block_dict = {}
        self.move_num = 0
        self.current_color = Color.black
        self._save_game()

    def _save_game(self):
        self.game_stack.append(
            dict(
                state=copy.deepcopy(self.state),
                block_dict=copy.deepcopy(self.block_dict),
                move_num=self.move_num,
                current_color=self.current_color,
                ko_coordinate=self.ko_coordinate))

    def _load_game(self):
        game_record = self.game_stack.pop()
        self.state = game_record['state']
        self.block_dict = game_record['block_dict']
        self.current_color = game_record['current_color']
        self.move_num = game_record['move_num']
        self.ko_coordinate = game_record['ko_coordinate']

    def __getitem__(self, index):
        x, y = index
        return self.state[x][y]

    def __position_to_str(self, pos):
        return pos.color.value

    def _inside_board(self, coordinate):
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

        # ko not allowed
        if self.ko_coordinate == coordinate:
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

            # all friend blocks have no air
            is_last_air = all(block.air_set == {coordinate} for block in friend_blocks)
            # at least eat one enemy block
            is_eatting_enemy = any(block.air_set == {coordinate} for block in enemy_blocks)

            if is_last_air and not is_eatting_enemy:
                return False

        return True

    def show_state(self):
        print("-"*37)
        # for pos_list in self.state:
        #     print(" ".join(pos.color.value for pos in pos_list))

        for row in range(self.size):
            pos_str_list = []
            for pos in self.state[:, row]:
                pos_str_list.append(self.__position_to_str(pos))

            row_string = " ".join(pos_str_list)
            print(row_string)

        print("-"*37)


    def _get_neighbors_coordinate(self, coordinate):
        x, y = coordinate
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return filter(self._inside_board, neighbors)

    def _change_color(self):
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
        # 可能出现重复, 一定要先去重
        block_id_list = list(set(block_id_list))
        if len(block_id_list) == 0:
            raise Exception("No block to merge!")

        if len(block_id_list) == 1:
            return block_id_list[0]

        merged_block = reduce(add, [self.block_dict[block_id]
                                    for block_id in block_id_list])

        for block_id in block_id_list:
            del self.block_dict[block_id]

        new_block_id = self._add_block(merged_block)
        for coord in merged_block.coordinate_set:
            pos = self[coord]
            pos.block_id = new_block_id

        return new_block_id

    def _reset_pos(self, pos):
        pos.color = Color.empty
        pos.block_id = None

    def _eat_block(self, block_id):
        block_to_eat = self.block_dict[block_id]
        del self.block_dict[block_id]

        eat_set = block_to_eat.coordinate_set
        if len(eat_set) == 1:
            self[eat_set[0]].is_ko = True

        for coord in eat_set:
            pos = self[coord]
            print("eat", pos.color, "at", coord)
            self._reset_pos(pos)
            neighbors_coordinate = list(self._get_neighbors_coordinate(coord))
            for neighbor in neighbors_coordinate:
                neighbor_blk_id = self[neighbor].block_id
                if neighbor_blk_id is not None:
                    self.block_dict[neighbor_blk_id].air_set.add(coord)

    def _state_to_set(self, state):

        if state is None or len(state) == 0:
            return set()

        state_set = {
            (i, j, pos.color)
            for i, row in enumerate(state)
            for j, pos in enumerate(row)
        }

        return state_set

    def _renew_update_set(self, old_state, new_state):

        prev_set = self._state_to_set(old_state)
        current_set = self._state_to_set(new_state)
        diff = current_set ^ prev_set
        self.update_set = current_set & diff

    def _update_state(self, coordinate):

        old_state = copy.deepcopy(self.state)

        neighbors_coordinate = list(self._get_neighbors_coordinate(coordinate))

        if not self._is_allowed_move(coordinate, neighbors_coordinate):
            print("rules not allowed to move:", coordinate)
            return False

        air_set = set()
        merge_block_id_list = []
        enemy_block_list = []

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
                #if enemy_block.air == 0:
                #    self._eat_block(enemy_block.block_id)
                enemy_block_list.append(enemy_block)

        new_block = Block(self.current_color, set([coordinate]), air_set)
        new_block_id = self._add_block(new_block)

        if len(merge_block_id_list) > 0:
            # more than one blocks, need to merge
            merge_block_id_list.append(new_block_id)
            self._merge_blocks(merge_block_id_list)

        self[coordinate].color = self.current_color
        self[coordinate].block_id = new_block_id

        for item in enemy_block_list:
            if item.air == 0:
                self._eat_block(item.block_id)

        self._renew_update_set(old_state, self.state)
        return True




    def _check_position(self, coordinate):
        # 顺序有讲究
        # 不在棋盘内
        if not self._inside_board(coordinate):
            return False

        # 落子位置为空
        if self[coordinate].color != Color.empty:
            return False

        # 打劫位置
        if coordinate == self.ko_coordinate:
            return False

        return True

    def _prompt_coordinate(self):
        while True:
            input_str = input(
                'Please input {} stone coordinate X,Y: '
                .format(self.current_color))
            x, y = input_str.split(",")
            x = int(x)
            y = int(y)
            #if not isinstance(x, int) or not isinstance(y, int):
            #    continue
            if (x < 0 or x >= self.size) or (y < 0 or y >= self.size):
                continue

            return (x, y)


    def _calc_block(self, coordinate):
        new_block = Block(self.current_color, set([coordinate]), set())
        new_block_id = self._add_block(new_block)
        self[coordinate].block_id = new_block_id
        self[coordinate].color = self.current_color

        neighbors = self._get_neighbors_coordinate(coordinate)

        merge_list = [new_block_id]
        for neighbor in neighbors:
            if self[neighbor].color == self.current_color:
                merge_list.append(self[neighbor].block_id)

        self._merge_blocks(merge_list)

    def _calc_air(self, coordinate):

        current_block_id = self[coordinate].block_id
        current_block = self.block_dict[current_block_id]
        neighbors = self._get_neighbors_coordinate(coordinate)
        eating_list = []
        removed_air_list = []
        for neighbor in neighbors:
            if self[neighbor].color == self.current_color:
                pass

            elif self[neighbor].color == Color.empty:
                current_block.air_set.add(neighbor)

            else:
                neighbor_block_id = self[neighbor].block_id
                neighbor_block = self.block_dict[neighbor_block_id]
                if neighbor_block_id in eating_list \
                   or neighbor_block_id in removed_air_list:
                    pass
                else:
                    neighbor_block.air_set.remove(coordinate)
                    removed_air_list.append(neighbor_block_id)
                    if neighbor_block.air == 0:
                        eating_list.append(neighbor_block_id)

        if current_block.air == 0 and len(eating_list) == 0:
            return False, eating_list

        return True, eating_list

    def _update_status(self):
        self.ko_coordinate = None
        self.move_num += 1
        self._change_color()

    def _remove_eaten_stone(self, eating_list):
        eat_num = len(eating_list)
        # remove dup blocks
        eating_list = list(set(eating_list))
        while eating_list:
            block_id = eating_list.pop()
            block = self.block_dict[block_id]
            del self.block_dict[block_id]

            if len(block.coordinate_set) == 1 and eat_num == 1:
                # 只吃一个子, 打劫的情况
                self.ko_coordinate = min(block.coordinate_set)
                print('ko coordinate : {}'.format(self.ko_coordinate))

            for coordinate in block.coordinate_set:

                neighbors = self._get_neighbors_coordinate(coordinate)

                for neighbor in neighbors:
                    # 先处理提子的邻接棋块, 若先把提子点置为empty, 下面这个if就没有意义
                    if self[neighbor].color == Color.empty \
                       or self[neighbor].color == self[coordinate].color:
                        pass
                    else:
                        neighbor_block_id = self[neighbor].block_id
                        neighbor_block = self.block_dict[neighbor_block_id]
                        neighbor_block.air_set.add(coordinate)
                # 应后面再处理提子点
                position = self[coordinate]
                position.color = Color.empty
                position.block_id = None





    def move(self):
        # 压栈
        while True:

            self._save_game()
            while True:
                coordinate = self._prompt_coordinate()
                if self._check_position(coordinate):
                    break

            self._calc_block(coordinate)
            status, eating_list = self._calc_air(coordinate)
            if status == False:
                print("Invalid coordinate due to the air rule")
                self._load_game()
                continue

            self._update_status()
            self._remove_eaten_stone(coordinate, eating_list)
            break

        self.show_state()


    def move_one_step(self, coordinate):
        self._save_game()
        print("input {} coordinate is {}".format(self.current_color, coordinate))
        if not self._check_position(coordinate):
            print("Invalid coordinate")
            self._load_game()
            return False

        self._calc_block(coordinate)
        status, eating_list = self._calc_air(coordinate)
        if status == False:
            print("Invalid coordinate due to the air rule")
            self._load_game()
            return False

        self._update_status()
        self._remove_eaten_stone(eating_list)
        self.show_state()




if __name__ == "__main__":
    # TODO: need more tests
    b = Board()
    b.move_one_step((3,3))
    b.move_one_step((3,4))
    b.move_one_step((4,4))
    b.move_one_step((4,3))
    b.move_one_step((2,3))
    b.move_one_step((4,5))
    b.move_one_step((3,5))
    b.move_one_step((5,5))
    b.move_one_step((5,3))
    b.move_one_step((5,4))
    b.move_one_step((4,4))
    b.move_one_step((4,2))
    #pdb.set_trace()
    b.move_one_step((4,4))
