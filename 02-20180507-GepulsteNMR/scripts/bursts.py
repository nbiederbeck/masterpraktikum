import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


def plot_burst_sequences():

    meiboom_gill = pd.read_csv("data/scope_2_1.csv", header=[0, 1])
    carr_purcell = pd.read_csv("data/scope_3_1.csv", header=[0, 1])

    fig = plt.figure()
    ax_mg = fig.add_subplot(211)
    ax_cp = fig.add_subplot(212)

    ax_mg.plot(meiboom_gill["x-axis"], meiboom_gill["1"], label="Meiboom-Gill")
    ax_cp.plot(carr_purcell["x-axis"], carr_purcell["1"], label="Carr-Purcell")

    ax_mg.legend(loc="best")
    ax_cp.legend(loc="best")
    ax_mg.set_xticks([])
    ax_mg.set_yticks([])
    ax_cp.set_xticks([])
    ax_cp.set_yticks([])

    fig.set_size_inches([5.73, 3.57])
    fig.tight_layout(pad=0)
    fig.savefig("build/burst_sequences.png")


if __name__ == "__main__":
    plot_burst_sequences()
