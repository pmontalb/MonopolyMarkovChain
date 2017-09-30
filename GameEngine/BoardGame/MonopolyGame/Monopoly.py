from GameEngine.Game import Player, PlayerInput
from GameEngine.BoardGame.BoardGame import BoardGame, BoardGameInput
from GameEngine.BoardGame.MonopolyGame.MonopolyBoard import MonopolyBoard, MonopolyBoardInput
from Utility.Logger import Logger, LogLevel


class MonopolyPlayerInput(PlayerInput):
    def __init__(self,
                 initial_capital=None,
                 initial_properties=None,
                 player_id="UnknownPlayer",
                 log_name="master", log_level=LogLevel.DEBUG):
        super(MonopolyPlayerInput, self).__init__(player_id, log_name, log_level)
        self.initial_capital = initial_capital
        self.initial_properties = initial_properties


class MonopolyPlayer(Player):
    def __init__(self, player_input):
        super(MonopolyPlayer, self).__init__(player_input)

        self.capital = self.player_input.initial_capital
        self.properties = self.player_input.initial_properties
        self.position = 0

        self.double_count = 0
        self.turns_in_prison = 0
        self.leave_prison_tickets = 0

    def __repr__(self):
        return "Player({} | $({}) | #p({}) | pos({}) | dc({}) | tip({}) | lpt({})".format(self.player_input.player_id,
                                                                                          self.capital,
                                                                                          len(self.properties),
                                                                                          self.position,
                                                                                          self.double_count,
                                                                                          self.turns_in_prison,
                                                                                          self.leave_prison_tickets)


class MonopolyInput(BoardGameInput):
    def __init__(self, n_players, max_turns=100, log_name="master", log_level=LogLevel.DEBUG):
        super(MonopolyInput, self).__init__(n_players, max_turns, "Monopoly", log_name, log_level)

    def make_board_input(self):
        self.board_input = MonopolyBoardInput()


class Monopoly(BoardGame):
    def __init__(self, game_input):
        super(Monopoly, self).__init__(game_input)

    def make_board(self):
        self.board = MonopolyBoard(self.game_input.board_input)

    def make_players(self):
        # read a config file for setting up money, properties, etc
        raise NotImplementedError()

    def _game_over(self):
        # remove players who have defaulted
        self.players = [p for p in self.players if p.capital > 0]

        # game is over if only two players are left
        return len(self.players) <= 2

    def _play_turn(self):
        for player in self.players:
            self._logger("{} is playing".format(player))
            self.board.advance(player)

        # player can now decide to buy/sell/trade
