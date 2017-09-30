from GameEngine.Game import Game, GameInput
from Utility.Logger import LogLevel
from abc import ABCMeta, abstractmethod


class BoardGameInput(GameInput, metaclass=ABCMeta):
    def __init__(self, n_players, max_turns, game_id, log_name="master", log_level=LogLevel.DEBUG):
        super(BoardGameInput, self).__init__(max_turns, game_id, log_name, log_level)

        self.board_input = None
        self.make_board_input()

        self.n_players = n_players

    @abstractmethod
    def make_board_input(self):
        raise NotImplementedError()

    @property
    def n_rows(self):
        return self.board_input.n_rows

    @property
    def n_cols(self):
        return self.board_input.n_cols


class BoardGame(Game, metaclass=ABCMeta):
    def __init__(self, board_game_input):
        super(BoardGame, self).__init__(board_game_input)

        self.board = None
        self.make_board()

        self.players = [None for _ in range(self.game_input.n_players)]
        self.make_players()

    @abstractmethod
    def make_board(self):
        raise NotImplementedError()

    @property
    def n_players(self):
        return self.game_input.n_players

    @abstractmethod
    def make_players(self):
        raise NotImplementedError()