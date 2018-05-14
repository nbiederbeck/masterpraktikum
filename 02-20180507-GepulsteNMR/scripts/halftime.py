import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


def plot_halftime_sequence():
    halftime = pd.read_csv("data/scope_4_1.csv", header=[0, 1])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(halftime["x-axis"], halftime["1"], label="Burst Sequenz")

    ax.legend()
    ax.set_xticks([])
    ax.set_yticks([])

    fig.savefig("build/halftime_sequence.png")


if __name__ == "__main__":
    plot_halftime_sequence()
