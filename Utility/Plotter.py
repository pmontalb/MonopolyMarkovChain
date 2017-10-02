import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib


def __ax_formatter(ax, title="", x_label="", y_label="", show_legend=False):
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    if show_legend:
        ax.legend(loc='best')


def surf(z, x, y, title="", x_label="", y_label="", show_legend=False, show=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Create X and Y data
    x_grid, y_grid = np.meshgrid(x, y)

    ax.plot_surface(x_grid, y_grid, z, rstride=1, cstride=1, antialiased=True)

    __ax_formatter(ax, title, x_label, y_label, show_legend)

    if show:
        plt.show()


def plot(z, x, title="", x_label="", y_label="", show_legend=False, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(x)):
        ax.plot(z[i, :])

    __ax_formatter(ax, title, x_label, y_label, show_legend)

    if show:
        plt.show()


def plot_row(z, row, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(z[row, :])

    if show:
        plt.show()


def bar_plot(y, labels, width=.35, title="", x_label="", y_label="", show_legend=False, show=False):
    fig, ax = plt.subplots()
    x = np.arange(len(y))
    ax.bar(x, y, width)

    # add some text for labels, title and axes ticks
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(labels)
    ax.grid(True)

    for label in ax.get_xmajorticklabels() + ax.get_xmajorticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    __ax_formatter(ax, title, x_label, y_label, show_legend)

    if show:
        plt.show()