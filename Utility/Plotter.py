import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib


def surf(z, x, y, show=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Create X and Y data
    x_grid, y_grid = np.meshgrid(x, y)

    ax.plot_surface(x_grid, y_grid, z, rstride=1, cstride=1, antialiased=True)

    if show:
        plt.show()


def plot(z, x, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(x)):
        ax.plot(z[i, :])

    if show:
        plt.show()


def plot_row(z, x, row, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(z[row, :])

    if show:
        plt.show()