import time
from board import Board
from sgfmill import sgf
import pdb


class Replay:

    def __init__(self, sgf_file):
        self._load_game(sgf_file)
        self.board = Board()

    def _load_game(self, sgf_file):
        with open(sgf_file, "rb") as rfd:
            game = sgf.Sgf_game.from_bytes(rfd.read())

        self.size = game.get_size()
        self.winner = game.get_winner()
        root_node = game.get_root()
        self.black_name = root_node.get("PB")
        self.white_name = root_node.get("PW")
        self.game_steps = game.get_main_sequence()

    def auto_play(self, delay=0):
        for step in self.game_steps:
            _, coordinate = step.get_move()
            if coordinate is None:
                continue
            self.board.move_one_step(coordinate)
            time.sleep(delay)


if __name__ == "__main__":

    r = Replay("../data/2t9d-围棋gokifu棋谱-20171025-柯洁九段-李世石九段.sgf")
    r.auto_play()
