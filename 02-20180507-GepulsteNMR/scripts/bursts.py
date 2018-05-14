import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt
from scipy.optimize import curve_fit


def read():
    meiboom_gill = pd.read_csv("data/scope_2_1.csv", header=[0, 1])
    carr_purcell = pd.read_csv("data/scope_3_1.csv", header=[0, 1])
    return meiboom_gill, carr_purcell


def plot_burst_sequences(
    meiboom_gill, carr_purcell, peakinds_meiboom_gill, peakinds_carr_purcell
):
    fig = plt.figure()
    ax_mg = fig.add_subplot(211)
    ax_cp = fig.add_subplot(212)

    ax_mg.plot(meiboom_gill["x-axis"], meiboom_gill["1"], label="Meiboom-Gill")
    ax_mg.plot(
        meiboom_gill["x-axis"].values[peakinds_meiboom_gill],
        meiboom_gill["1"].values[peakinds_meiboom_gill],
        "C1x-",
    )

    ax_cp.plot(carr_purcell["x-axis"], carr_purcell["1"], label="Carr-Purcell")
    ax_cp.plot(
        carr_purcell["x-axis"].values[peakinds_carr_purcell],
        carr_purcell["1"].values[peakinds_carr_purcell],
        "C1x-",
    )

    ax_mg.legend(loc="best")
    ax_cp.legend(loc="best")
    ax_mg.set_xticks([])
    ax_mg.set_yticks([])
    ax_cp.set_xticks([])
    ax_cp.set_yticks([])

    # fig.set_size_inches([5.73, 3.57])
    # fig.tight_layout(pad=0)
    fig.savefig("build/burst_sequences.png")


def find_peaks(data):
    x = data["1"].values.reshape(-1)
    peakinds = find_peaks_cwt(x, [100])
    if len(peakinds) == 0:  # catch if no peakinds are found
        peakinds = [0]
    return peakinds


def expo_fit_meiboom_gill(data, peakinds):
    x = data["x-axis"].values[peakinds].reshape(-1)
    y = data["1"].values[peakinds].reshape(-1)
    xs = np.linspace(np.min(x), np.max(x), 1000)

    def func(x, T_2, a, m):
        """a * np.exp(-x / T_2) + m"""
        return a * np.exp(-x / T_2) + m

    # Fit exp function
    par, cov = curve_fit(func, x, y)
    print(func.__doc__)
    for n, p, c in zip(["T_2", "a", "m"], par, np.sqrt(np.diag(cov))):
        print(r"{} = {:.2f} \pm {:.2f}".format(n, p, c))

    fig, ax = plt.subplots()

    ax.plot(x, y, "C0x", label="Peaks Meiboom-Gill")
    ax.plot(
        xs, func(xs, *par), "C1-",
        label=r"Fit: $T_2 = \SI{" + "{:.2f}".format(par[0]) + "}{\second}$"
    )

    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$\log_{10}(U \:\:/\:\: \text{div})$")

    ax.set_yscale("log")
    ax.legend()

    fig.savefig("build/burst_peaks_mg.png")


if __name__ == "__main__":
    meiboom_gill, carr_purcell = read()

    peakinds_mg = find_peaks(meiboom_gill)
    peakinds_cp = find_peaks(carr_purcell)

    plot_burst_sequences(meiboom_gill, carr_purcell, peakinds_mg, peakinds_cp)

    expo_fit_meiboom_gill(meiboom_gill, peakinds_mg)
