import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


def fit(nu, V, nu_g):
    return V / (np.sqrt(1 + (nu / nu_g) ** 2))


def plot(name):
    r1 = int(name[22:25])
    rn = int(name[30:33])
    u1 = int(name[38:41])

    U_A, phi, U_1, nu = np.genfromtxt(name, unpack=True)

    df = pd.DataFrame({
        r"{$\nu \:\:/\:\: \si{\kilo\hertz}$}": nu,
        r"{$\phi \:\:/\:\: \si{\degree}$}": phi,
        r"{$U_1 \:\:/\:\: \si{\milli\volt}$}": U_1,
        r"{$U_A \:\:/\:\: \si{\milli\volt}$}": U_A,
    })
    with open(name.replace("data", "build").replace(".txt", "_data.tex"), "w") as ofile:
        df.to_latex(ofile, index=False, column_format="S S S S", escape=False)

    x = np.linspace(np.min(nu), np.max(nu))

    par, cov = curve_fit(fit, nu, U_A / U_1, p0=[rn / r1, 1])

    fig, ax = plt.subplots()
    scale = 0.8
    fig.set_size_inches(
        scale * fig.get_figwidth(), scale * fig.get_figheight()
    )

    ax.scatter(nu, U_A / U_1, c="C1", marker="x", label="Messwerte")
    ax.plot(x, fit(x, *par), label="Fit")

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    # ax.set_ylabel(r"$U_A \:\:/\:\: \si{\milli\volt}$")
    ax.set_ylabel(r"$V$")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/{}.png".format(name[5:-4]))
    fig.savefig("build/{}.pgf".format(name[5:-4]))

    with open(name.replace("data", "build").replace("txt", "tex"), "w") as ofile:
        for p, c in zip(par, np.sqrt(np.diag(cov))):
            print("{} \\pm {}".format(np.round(p, 3), np.round(c, 3)), file=ofile)


def main():
    filenames = [
        "data/lin_verst_01__r1_200__rn_470__u1_100.txt",
        "data/lin_verst_02__r1_200__rn_100__u1_100.txt",
        "data/lin_verst_03__r1_100__rn_470__u1_100.txt",
        "data/lin_verst_04__r1_470__rn_100__u1_100.txt",
    ]
    for name in filenames:
        plot(name)


if __name__ == "__main__":
    main()
