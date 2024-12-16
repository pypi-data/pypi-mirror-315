import matplotlib.pyplot as plt
from lumpur.num.polynomial import Polynomial

def plot_polynomial(
    x,
    p : Polynomial,
    label=None,
    axis_labels=['x', 'y'],
    show_grid=True):

    y = p.evaluate(x)
    plt.plot(x, y, label=label)
    if label is not None:
        plt.legend()
    plt.gca().grid(show_grid)
    plt.xlabel(axis_labels[0])
    plt.ylabel(axis_labels[1])
