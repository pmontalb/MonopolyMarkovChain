from abc import abstractmethod, ABCMeta
from Utility.Logger import Logger, LogLevel


class GameInput:
    def __init__(self, max_turns=100, game_id="UnknownGame", log_name="master", log_level=LogLevel.DEBUG):
        self.max_turns = max_turns
        self.game_id = game_id
        self.log_name = log_name
        self.log_level = log_level


class Game(metaclass=ABCMeta):
    def __init__(self, game_input):
        self.game_input = game_input
        self.turns = 0
        self._logger = Logger(game_input.log_name, game_input.log_level)

    def __repr__(self):
        return "Game({} | {} / {})".format(self.game_input.game_id, self.turns, self.game_input.max_turns)

    def play(self):
        self._logger(self)
        self._play()

    @abstractmethod
    def _play(self):
        raise NotImplementedError()

    def game_over(self):
        is_over = self.turns >= self.game_input.max_turns
        return is_over and self._game_over()

    @abstractmethod
    def _game_over(self):
        raise NotImplementedError()


class PlayerInput:
    def __init__(self, player_id="UnknownPlayer", log_name="master", log_level=LogLevel.DEBUG):
        self.player_id = player_id
        self.log_name = log_name
        self.log_level = log_level


class Player:
    def __init__(self, player_input):
        self.player_input = player_input
        self._logger = Logger(player_input.log_name, player_input.log_level)
