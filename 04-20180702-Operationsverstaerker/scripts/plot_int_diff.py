import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from scipy.optimize import curve_fit
import pandas as pd


def fit(x, m, b):
    return np.exp(np.log(2 * np.pi * x) * m + b)


def plot(name):
    R, C = 9.6e3, 20.8e-9
    RC = R * C
    omega_theo = 1 / RC
    omega_theo /= 1000  # von hertz in kilohertz
    omega_theo = np.log(omega_theo)
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
        df.to_latex(
            ofile,
            index=False,
            column_format="S[zero-decimal-to-integer=true,  table-format=0.3, zero-decimal-to-integer=true]"
            + "S[zero-decimal-to-integer=true, table-format=3.0]"
            + "S[zero-decimal-to-integer=true, round-mode=places, table-format=2.2]",
            escape=False,
        )

    x = np.linspace(np.min(nu), np.max(nu), 1001)

    par, cov = curve_fit(fit, nu, U_A / U_1)

    with open(name.replace("data", "build").replace("txt", "tex"), "w") as ofile:
        print("omega_theo: {}".format(omega_theo))
        for n, p, c in zip(["omega", "V_0"], par, np.sqrt(np.diag(cov))):
            print(
                "{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)), file=ofile
            )
            print("{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)))
            # print("{}: {} \\pm {}".format(n, p, c))

    fig, ax = plt.subplots()

    ax.scatter(nu, U_A / U_1, c="C1", marker="x", label="Messwerte")

    ax.plot(x, fit(x, *par), label="Fit")
    # ax.yaxis.set_major_locator(tick.LogLocator(numticks=2))

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    ax.set_ylabel(r"$V_\text{exp}$")
    # ax.set_ylabel(r"$V$")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_ylim([1e-4, 9e-2])

    ax.legend()

    fig.tight_layout(pad=0)
    # fig.savefig("build/{}.png".format(name[5:-4]))
    # fig.savefig("build/{}.pgf".format(name[5:-4]))
    fig.savefig("build/{}.pdf".format(name[5:-4]))


def main():
    filenames = ["data/integrator.txt", "data/differentiator.txt"]
    for name in filenames:
        plot(name)


if __name__ == "__main__":
    main()
