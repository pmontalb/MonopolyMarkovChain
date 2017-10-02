from MonteCarloEngine.Simulator import Simulator, SimulatorInput
from Utility.Logger import LogLevel
from Utility.Plotter import surf, plot, plot_row, bar_plot
import numpy as np
from os import getcwd
from Utility.Profiler import profile

DATA_DIRECTORY = getcwd() + "/Data/"
MARKOV_GENERATOR_FILE = DATA_DIRECTORY + "/mg_{}.csv"


def make_markov_generator():
    n_simulations = 100000
    use_multiprocess = False
    simulator_input = SimulatorInput(n_simulations, use_multiprocess, log_level=LogLevel.NEVER)

    simulator = Simulator(simulator_input)
    simulator.run()
    np.savetxt(MARKOV_GENERATOR_FILE.format(n_simulations), simulator.markov_generator, delimiter=",")


def profile_simulator():
    n_simulations = 1000
    use_multiprocess = False
    simulator_input = SimulatorInput(n_simulations, use_multiprocess, log_level=LogLevel.NEVER)
    simulator = Simulator(simulator_input)

    profile(simulator.run, [], 10)


def plot_markov_generator():
    n_simulations = 100000
    markov_generator = np.loadtxt(MARKOV_GENERATOR_FILE.format(n_simulations), delimiter=",")
    plot_row(markov_generator, 0, show=True)


def evolve_markov_generator():
    n_simulations = 100000
    per_turn_markov_generator = np.loadtxt(MARKOV_GENERATOR_FILE.format(n_simulations), delimiter=",")
    markov_generator_transpose = np.transpose(per_turn_markov_generator)

    total_generator = np.zeros_like(markov_generator_transpose)
    total_generator[0, 0] = 1
    for i in range(100):
        total_generator = markov_generator_transpose.dot(total_generator)

    # Probability Distribution Function after 100 rolls
    pdf = np.transpose(total_generator)

    return pdf[0, :]


def histogram_steady_state_vector():
    pdf = evolve_markov_generator()

    simulator_input = SimulatorInput(1, False, log_level=LogLevel.NEVER)
    simulator = Simulator(simulator_input)
    labels = [simulator.monopoly_engine.board[i].board_item_input.item_id for i in range(40)]
    bar_plot(pdf, labels, y_label="Probability", title="Steady-State Probabilities", show=True)


if __name__ == "__main__":
    histogram_steady_state_vector()
