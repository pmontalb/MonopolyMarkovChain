from GameEngine.Game import Player, PlayerInput
from GameEngine.BoardGame.BoardGame import BoardGame, BoardGameInput
from GameEngine.BoardGame.MonopolyGame.MonopolyBoard import MonopolyBoard, MonopolyBoardInput


class MonopolyPlayerInput(PlayerInput):
    def __init__(self, initial_capital=None, initial_properties=None, player_id="UnknownPlayer"):
        super(MonopolyPlayerInput, self).__init__(player_id)
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


class MonopolyInput(BoardGameInput):
    def __init__(self, n_players):
        super(MonopolyInput, self).__init__(n_players, "Monopoly")

    def make_board_input(self):
        self.board_input = MonopolyBoardInput()


class Monopoly(BoardGame):
    def __init__(self, board_input):
        super(Monopoly, self).__init__(board_input)

    def make_board(self):
        self.board = MonopolyBoard(self.game_input)

    def make_players(self):
        if self.n_players > 1:
            raise NotImplementedError()

        # 1 player is only for testing/non-game purposes
        player_input = MonopolyPlayerInput(0, 0, "Player1")
        self.players = [MonopolyPlayer(player_input)]

    def _game_over(self):
        n_remaining = self.n_players
        for player in self.players:
            if player.capital <= 0:
                n_remaining -= 1

        return n_remaining <= 2

    def play(self):
        while not self.game_over():
            for player in self.players:
                self.board.advance(player)

            # player can now decide to buy/sell/trade