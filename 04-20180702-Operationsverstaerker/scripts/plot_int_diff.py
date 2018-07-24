import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


def fit(x, m, b):
    return np.exp(np.log(2 * np.pi * x) * m + b)


def plot(name):
    U_A, U_1, nu = np.genfromtxt(name, unpack=True)
    # nu *= 1000
    U_A /= 1000  # von milliVolt in Volt

    df = pd.DataFrame(
        {
            r"{$\nu \:\:/\:\: \si{\kilo\hertz}$}": nu,
            r"{$U_1 \:\:/\:\: \si{\milli\volt}$}": U_1,
            r"{$U_A \:\:/\:\: \si{\volt}$}": U_A,
        }
    )

    with open(name.replace("data", "build").replace(".txt", "_data.tex"), "w") as ofile:
        df.to_latex(ofile, index=False, column_format="S S S", escape=False)

    x = np.linspace(np.min(nu), np.max(nu), 1001)

    par, cov = curve_fit(fit, nu, U_A / U_1)

    with open(name.replace("data", "build").replace("txt", "tex"), "w") as ofile:
        for n, p, c in zip(["m", "b"], par, np.sqrt(np.diag(cov))):
            print(
                "{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)), file=ofile
            )
            print("{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)))

    fig, ax = plt.subplots()

    ax.scatter(nu, U_A / U_1, c="C1", marker="x", label="Messwerte")
    ax.plot(x, fit(x, *par), label="Fit")

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    ax.set_ylabel(r"$V'_\text{exp}$")
    # ax.set_ylabel(r"$V$")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/{}.png".format(name[5:-4]))
    fig.savefig("build/{}.pgf".format(name[5:-4]))


def main():
    filenames = ["data/integrator.txt", "data/differentiator.txt"]
    for name in filenames:
        plot(name)


if __name__ == "__main__":
    main()
