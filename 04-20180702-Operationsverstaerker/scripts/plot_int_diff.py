import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


def plot(name):
    U_A, U_1, nu = np.genfromtxt(name, unpack=True)

    df = pd.DataFrame({
        r"{$\nu \:\:/\:\: \si{\kilo\hertz}$}": nu,
        r"{$U_1 \:\:/\:\: \si{\milli\volt}$}": U_1,
        r"{$U_A \:\:/\:\: \si{\milli\volt}$}": U_A,
    })

    with open(name.replace("data", "build").replace(".txt", "_data.tex"), "w") as ofile:
        df.to_latex(ofile, index=False, column_format="S S S", escape=False)

    x = np.linspace(np.min(nu), np.max(nu))

    fig, ax = plt.subplots()
    scale = 0.8
    fig.set_size_inches(
        scale * fig.get_figwidth(), scale * fig.get_figheight()
    )

    ax.scatter(nu, U_A, c="C1", marker="x", label="Messwerte")
    # ax.plot(x, fit(x, *par), label="Fit")

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    ax.set_ylabel(r"$U_A \:\:/\:\: \si{\milli\volt}$")
    # ax.set_ylabel(r"$V$")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/{}.png".format(name[5:-4]))
    fig.savefig("build/{}.pgf".format(name[5:-4]))


def main():
    filenames = [
        "data/integrator.txt",
        "data/differentiator.txt",
    ]
    for name in filenames:
        plot(name)


if __name__ == "__main__":
    main()
