from MonteCarloEngine.Simulator import Simulator, SimulatorInput
from Utility.Logger import LogLevel
from Utility.Plotter import surf, plot, plot_row
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
    #surf(markov_generator, np.arange(40), np.arange(40), show=True)
    plot_row(markov_generator, np.arange(40), 0, show=True)


if __name__ == "__main__":
    plot_markov_generator()