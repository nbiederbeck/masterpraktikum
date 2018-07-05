import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


# def fit(nu, V, nu_g):
#     return V / (np.sqrt(1 + (nu / nu_g) ** 2))
def fit(nu, V, RC):
    return V / np.sqrt(1 + (nu * RC) ** 2)


def plot(name):
    r1 = float(name[22:25])
    rn = float(name[30:33])
    u1 = float(name[38:41])

    U_A, phi, U_1, nu = np.genfromtxt(name, unpack=True)

    df = pd.DataFrame({
        r"{$\nu \:\:/\:\: \si{\kilo\hertz}$}": nu,
        r"{$\phi \:\:/\:\: \si{\degree}$}": phi,
        r"{$U_1 \:\:/\:\: \si{\milli\volt}$}": U_1,
        r"{$U_A \:\:/\:\: \si{\milli\volt}$}": U_A,
    })
    with open(name.replace("data", "build").replace(".txt", "_data.tex"), "w") as ofile:
        df.to_latex(ofile, index=False, column_format="S S S S", escape=False)

    x = np.linspace(np.min(nu), np.max(nu), 1001)

    par, cov = curve_fit(fit, nu, U_A / U_1, p0=[rn / r1, 1])
    V_ = par[0]

    rel_diff_V = np.abs(np.round(((V_ - (rn / r1)) / (rn / r1) * 100), 3))
    V = 1.0 / ((1.0 / V_) - (r1 / rn))

    print(r"V \cdot \nu_G = {}".format(V_ * par[1]))

    fig, ax = plt.subplots()
    scale = 1.0
    fig.set_size_inches(fig.get_figwidth() * scale, fig.get_figheight() * scale)

    ax.scatter(nu, U_A / U_1, c="C1", marker="x", label="Messwerte")
    ax.plot(x, fit(x, *par), label=r"Fit: $V'={}, \nu_G={}$kHz".format(*np.round(par, 3)))

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    # ax.set_ylabel(r"$U_A \:\:/\:\: \si{\milli\volt}$")
    ax.set_ylabel(r"$V$")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/{}.png".format(name[5:-4]), bbox_inches='tight', pad_inches=0)
    fig.savefig("build/{}.pgf".format(name[5:-4]), bbox_inches='tight', pad_inches=0)

    with open(name.replace("data", "build").replace("txt", "tex"), "w") as ofile:
        for n, p, c in zip(["V", "nu_g"], par, np.sqrt(np.diag(cov))):
            print("{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)), file=ofile)
            print("{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)))
        print("Rel Diff V_mess, V_theo: {}%".format(rel_diff_V))
        print("Leerlaufverstaerkung V: {}".format(V))


def plot_phase(names):
    phases = []
    nus = []
    settings = []
    U_As = []
    for name in names:
        U_As.append(np.genfromtxt(name, unpack=True)[0])
        phases.append(np.genfromtxt(name, unpack=True)[1])
        nus.append(np.genfromtxt(name, unpack=True)[3])
        settings.append(r"$r_1 = {}\,\Omega, \:\: r_N = {}\,\Omega$".format(name[22:25], name[30:33]))

    fig, ax = plt.subplots()
    axr = ax.twinx()

    for p, n, s, u in zip(phases, nus, settings, U_As):
        ax.scatter(n, p, marker="o", s=20, label=s)

        axr.scatter(n, u, marker=".", s=20)
    axr.set_ylabel(r"$U_A \:\:/\:\: \si{\milli\volt}$,  (kleine Punkte)")
    axr.set_yscale("log")

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    ax.set_ylabel(r"$\phi \:\:/\:\: \si{\degree}$,  (große Punkte)")
    ax.set_xscale("log")
    # ax.legend(loc="lower left")
    ax.legend()
    fig.tight_layout(pad=0)
    fig.savefig("build/phases.png", bbox_inches='tight', pad_inches=0)
    fig.savefig("build/phases.pgf", bbox_inches='tight', pad_inches=0)
    # r1 = float(name[22:25])
    # rn = float(name[30:33])
    # u1 = float(name[38:41])

    # U_A, phi, U_1, nu = np.genfromtxt(name, unpack=True)


def main():
    filenames = [
        "data/lin_verst_01__r1_200__rn_470__u1_100.txt",
        "data/lin_verst_02__r1_200__rn_100__u1_100.txt",
        "data/lin_verst_03__r1_100__rn_470__u1_100.txt",
        "data/lin_verst_04__r1_470__rn_100__u1_100.txt",
    ]
    for name in filenames:
        plot(name)
    plot_phase(filenames)


if __name__ == "__main__":
    main()
