from MonteCarloEngine.Simulator import Simulator, SimulatorInput
from Utility.Logger import LogLevel
import numpy as np
from os import getcwd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
from pylab import *


DATA_DIRECTORY = getcwd() + "/Data/"


def surf(z, x, y):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Create X and Y data
    x_grid, y_grid = np.meshgrid(x, y)

    surf = ax.plot_surface(x_grid, y_grid, z, rstride=1, cstride=1, antialiased=True)
    plt.show()


if __name__ == "__main__":
    n_simulations = 1000
    simulator_input = SimulatorInput(n_simulations, "master", LogLevel.NEVER)

    simulator = Simulator(simulator_input)
    simulator.run()
    np.savetxt(DATA_DIRECTORY + "/mg_{}.csv".format(n_simulations), simulator.markov_generator, delimiter=",")

    surf(simulator.markov_generator, np.arange(40), np.arange(40))
