from GameEngine.BoardGame.MonopolyGame.Monopoly import Monopoly, MonopolyInput
from GameEngine.BoardGame.MonopolyGame.Monopoly import MonopolyPlayer, MonopolyPlayerInput
from Utility.Logger import LogLevel
import numpy as np


class MonopolyMarkovGeneratorInput(MonopolyInput):
    def __init__(self, initial_position, log_name="master", log_level=LogLevel.DEBUG):
        super(MonopolyInput, self).__init__(1, 1, "Monopoly", log_name, log_level)
        self.initial_position = initial_position


class MonopolyMarkovGenerator(Monopoly):
    def __init__(self, game_input):
        super(Monopoly, self).__init__(game_input)

        self.markov_generator = np.zeros((self.board.n_rows, self.board.n_rows))

    @property
    def initial_position(self):
        return self.game_input.initial_position

    def reset(self):
        super(MonopolyMarkovGenerator, self).reset()
        for player in self.players:
            player.position = self.initial_position

    def make_players(self):
        # 1 player only
        player_input = MonopolyPlayerInput(0, [], "Player1")
        self.players = [MonopolyPlayer(player_input)]

    def _play_turn(self):
        self.board.advance(self.players[0])
        self.markov_generator[self.initial_position, self.players[0].position] += 1


class SimulatorInput:
    def __init__(self, n_simulations, log_name="master", log_level=LogLevel.DEBUG):
        if n_simulations <= 0:
            raise ValueError("# Simulations must be positive")
        self.n_simulations = n_simulations
        self.log_name = log_name
        self.log_level = log_level


class Simulator:
    def __init__(self, simulator_input):
        self.simulator_input = simulator_input
        mmg_input = MonopolyMarkovGeneratorInput(0, self.simulator_input.log_name, self.simulator_input.log_level)
        self.monopoly_engine = MonopolyMarkovGenerator(mmg_input)

    @property
    def n_simulations(self):
        return self.simulator_input.n_simulations

    @property
    def markov_generator(self):
        return self.monopoly_engine.markov_generator

    def run(self):
        for initial_position in range(self.monopoly_engine.board.n_rows):
            print("Working on position {}".format(initial_position))
            self.monopoly_engine.game_input.initial_position = initial_position

            for sim in range(self.n_simulations):
                self.monopoly_engine.reset()
                self.monopoly_engine.play()

        self.monopoly_engine.markov_generator /= self.n_simulations
