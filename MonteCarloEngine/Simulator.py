from GameEngine.BoardGame.MonopolyGame.Monopoly import Monopoly, MonopolyInput
from GameEngine.BoardGame.MonopolyGame.Monopoly import MonopolyPlayer, MonopolyPlayerInput
from Utility.Logger import LogLevel
from Utility.MultiProcess import multiprocess_map
import numpy as np


def multiprocess_wrapper(func, __not_used):
    return func()


class MonopolyMarkovGeneratorInput(MonopolyInput):
    def __init__(self, initial_position, multiprocess=True, log_name="master", log_level=LogLevel.DEBUG):
        super(MonopolyInput, self).__init__(1, 1, "Monopoly", log_name, log_level)
        self.initial_position = initial_position
        self.multiprocess = multiprocess


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
        # 1 player only, with huge capital
        player_input = MonopolyPlayerInput(1e9, [], "Player1")
        self.players = [MonopolyPlayer(player_input)]

    def _play_turn(self):
        self.board.advance(self.players[0])
        if self.players[0].position == self.board.go_to_prison:
            raise ValueError("")
        self.markov_generator[self.initial_position, self.players[0].position] += 1


class SimulatorInput:
    def __init__(self, n_simulations, multiprocess, log_name="master", log_level=LogLevel.DEBUG):
        if n_simulations <= 0:
            raise ValueError("# Simulations must be positive")
        self.n_simulations = n_simulations
        self.multiprocess = multiprocess
        self.log_name = log_name
        self.log_level = log_level


class Simulator:
    def __init__(self, simulator_input):
        self.simulator_input = simulator_input
        mmg_input = MonopolyMarkovGeneratorInput(0, self.multiprocess, self.simulator_input.log_name, self.simulator_input.log_level)
        self.monopoly_engine = MonopolyMarkovGenerator(mmg_input)

    @property
    def n_simulations(self):
        return self.simulator_input.n_simulations

    @property
    def multiprocess(self):
        return self.simulator_input.multiprocess

    @property
    def markov_generator(self):
        return self.monopoly_engine.markov_generator

    def run(self):
        for initial_position in range(self.monopoly_engine.board.n_rows):
            if initial_position == self.monopoly_engine.board.go_to_prison:
                print("Skipping Go To Prison")
                continue
            print("Working on position {}".format(initial_position))

            self.monopoly_engine.game_input.initial_position = initial_position

            if not self.multiprocess:
                [self.__run_worker() for _ in range(self.n_simulations)]
            else:
                raise NotImplementedError()

        self.monopoly_engine.markov_generator /= self.n_simulations

    def __run_worker(self):
        self.monopoly_engine.reset()
        if self.monopoly_engine.game_input.initial_position == self.monopoly_engine.board.prison_position:
            self.monopoly_engine.players[0].turns_in_prison = 3  # TODO: remove this hardcoded number!

        self.monopoly_engine.play()
