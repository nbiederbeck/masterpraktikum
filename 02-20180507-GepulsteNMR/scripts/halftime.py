import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from pint import UnitRegistry
ureg = UnitRegistry()
ureg.default_format = 'Lx'

mpl.rcParams["text.latex.preamble"] = r"\usepackage{xfrac}\usepackage{siunitx}"


def plot_halftime_sequence():
    halftime = pd.read_csv("data/scope_4_1.csv", header=[0, 1])

    fig = plt.figure()
    ax = fig.add_subplot(211)

    ax.plot(halftime["x-axis"], halftime["1"], label="Burst Sequenz")

    ax.legend()
    ax.set_xlabel(r"$t \:\:/\:\: \si{\second}$")
    ax.set_ylabel(r"$U \:\:/\:\: \si{\volt}$")

    peak = halftime[25000:29500]
    peak["1"] -= peak["1"].values[0]

    mask = peak["1"] <= peak["1"].min() / 2

    halftimes_x = peak["x-axis"].values[mask][[0, -1]]
    halftimes_y = peak["1"].values[mask][[0, -1]]

    ax = fig.add_subplot(212)

    ax.plot(peak["x-axis"], peak["1"], label="Peak")

    halftime_t = halftimes_x[-1] - halftimes_x[0]
    print("Halbwertszeit = {}s".format(halftime_t))

    ax.plot(
        halftimes_x,
        halftimes_y,
        "C1x-",
        label=r"$t_{\sfrac{1}{2}} = \SI{"
        + "{:.2f}".format(1e6 * halftime_t)
        + "}{\micro\second}$",
    )

    ax.legend()
    ax.set_xlabel(r"$t \:\:/\:\: \si{\second}$")
    ax.set_ylabel(r"$U \:\:/\:\: \si{\volt}$")

    fig.savefig("build/halftime_sequence.png")

    return halftime_t


def feldgradient(halftime):
    halftime *= ureg.second
    gammap = 2.68e8 * ureg('radians per second per tesla')
    d = 4.4 * ureg.millimeter
    G = 8.8 / (d * gammap * halftime)
    print("G = {}".format(G))


if __name__ == "__main__":
    halftime = plot_halftime_sequence()
    feldgradient(halftime)
