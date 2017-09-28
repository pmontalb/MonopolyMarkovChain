from abc import abstractmethod, ABCMeta


class GameInput:
    def __init__(self, max_turns=100, game_id="UnknownGame"):
        self.max_turns = max_turns
        self.game_id = game_id


class Game(metaclass=ABCMeta):
    def __init__(self, game_input):
        self.game_input = game_input
        self.turns = 0

    @abstractmethod
    def play(self):
        raise NotImplementedError()

    def game_over(self):
        is_over = self.turns >= self.game_input.max_turns
        return is_over and self._game_over()

    @abstractmethod
    def _game_over(self):
        raise NotImplementedError()


class PlayerInput:
    def __init__(self, player_id="UnknownPlayer"):
        self.player_id = player_id


class Player:
    def __init__(self, player_input):
        self.player_input = player_input
