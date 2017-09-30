from GameEngine.BoardGame.MonopolyGame.Monopoly import Monopoly, MonopolyInput
from GameEngine.BoardGame.MonopolyGame.Monopoly import MonopolyPlayer, MonopolyPlayerInput


class MonopolyMarkovGenerator(Monopoly):
    def __init__(self, board_input):
        super(Monopoly, self).__init__(board_input)

    def make_players(self):
        # 1 player only
        player_input = MonopolyPlayerInput(0, [], "Player1")
        self.players = [MonopolyPlayer(player_input)]


if __name__ == "__main__":
    mmg_input = MonopolyInput(1, 1)
    mmg = MonopolyMarkovGenerator(mmg_input)

    mmg.play()