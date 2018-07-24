import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from scipy.optimize import curve_fit
import pandas as pd


# def fit(nu, V, nu_g):
#     return V / (np.sqrt(1 + (nu / nu_g) ** 2))
def fit(nu, V_, RC, c):
    return V_ / np.sqrt(1 + (2 * np.pi * nu * RC) ** 2) + c


# def wrapper(names):
#     delta_R, V_, delta_V, V_nuG = [], [], [], []
#     for name in names:
#         a, b, c, d = plot(name)
#         delta_R.append(a)
#         V_.append(b)
#         delta_V.append(c)
#         V_nuG.append(d)
#         print(a, b, c, d)


def plot(name):
    r1 = float(name[22:25])
    rn = float(name[30:33])
    u1 = float(name[38:41])

    U_A, phi, U_1, nu = np.genfromtxt(name, unpack=True)

    df = pd.DataFrame(
        {
            r"{$\nu \:\:/\:\: \si{\kilo\hertz}$}": nu,
            r"{$\phi \:\:/\:\: \si{\degree}$}": phi,
            r"{$U_1 \:\:/\:\: \si{\milli\volt}$}": U_1,
            r"{$U_A \:\:/\:\: \si{\milli\volt}$}": U_A,
        }
    )
    with open(name.replace("data", "build").replace(".txt", "_data.tex"), "w") as ofile:
        df.to_latex(ofile, index=False, column_format="S S S S", escape=False)

    x = np.linspace(np.min(nu), np.max(nu), 1001)

    fig, ax = plt.subplots()
    scale = 1.0
    fig.set_size_inches(fig.get_figwidth() * scale, fig.get_figheight() * scale)

    # U_1 -= U_1[-1]*0.99
    # U_A -= U_A[-1]*0.99
    V_mess = U_A / U_1

    if "04" not in name:
        n = 1
        par, cov = curve_fit(fit, nu[:-n], V_mess[:-n], p0=[rn / r1, 0.1, 0])
    else:
        n = 4
        par, cov = curve_fit(fit, nu[:-n], V_mess[:-n], p0=[rn / r1, 0.1, 0])

    V_ = par[0]  # + par[-1]
    nu_g = 1.0 / par[1]

    rel_diff_V = np.abs(np.round(((V_ - (rn / r1)) / (rn / r1) * 100), 3))
    V = 1.0 / ((1.0 / V_) - (r1 / rn))

    # print(r"V_ \cdot \nu_G = {}".format(V_ * nu_g))

    ax.scatter(nu, V_mess, c="C1", marker="x", label="Messwerte")
    ax.plot(
        x,
        fit(x, *par),
        label=r"Fit: $V'_{\text{exp}}="
        + r"{}, \nu_G={}$kHz".format(*np.round([V_, nu_g], 1)),
    )

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    # ax.set_ylabel(r"$U_A \:\:/\:\: \si{\milli\volt}$")
    ax.set_ylabel(r"$V\!\left(\nu\right)$")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.yaxis.set_major_locator(tick.LogLocator(subs=(1.0, 1.9, 2.4), numticks=4))
    # ax.yaxis.set_minor_locator(tick.LogLocator(subs="all", numticks=4))

    ax.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/{}.png".format(name[5:-4]), bbox_inches="tight", pad_inches=0)
    fig.savefig("build/{}.pgf".format(name[5:-4]), bbox_inches="tight", pad_inches=0)

    with open(name.replace("data", "build").replace("txt", "tex"), "w") as ofile:
        par[1] = 1.0 / par[1]
        cov[1] = 1.0 / cov[1]
        # for n, p, c in zip(["V_", "nu_g", "c"], par, np.sqrt(np.diag(cov))):
        # print(
        #     "{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)), file=ofile
        # )
        # print("{}: {} \\pm {}".format(n, np.round(p, 3), np.round(c, 3)))

        # hier Tabellenzeilen
        p = np.round(par, 3)
        c = np.round(np.sqrt(np.diag(cov)), 3)
        print(
            "{} & ".format(np.round(rn / r1, 3))  # R_N / R_1
            + "{} \\pm {} & ".format(p[0], c[0])  # V'_exp
            + "{} & ".format(rel_diff_V)  # delta V
            + "{} \\pm {} & ".format(
                np.round(p[1], 1), np.round(0.01 * c[1], 1)
            )  # nu_G
            + "{} & ".format(np.round(V_ * nu_g, 3))  # V' * nu_G
            + "{} ".format(np.round(V, 3))  # reale verstärkung nach gleichung (10)
        )

        # print("Rel Diff V_mess, V_theo: {}%".format(rel_diff_V))
        # print("Leerlaufverstaerkung V: {}".format(V))


def plot_phase(names):
    phases = []
    nus = []
    settings = []
    U_As = []
    for name in names:
        U_As.append(np.genfromtxt(name, unpack=True)[0])
        phases.append(np.genfromtxt(name, unpack=True)[1])
        nus.append(np.genfromtxt(name, unpack=True)[3])
        settings.append(
            r"$r_1 = {}\,\Omega, \:\: r_N = {}\,\Omega$".format(
                name[22:25], name[30:33]
            )
        )

    fig, ax = plt.subplots()
    # axr = ax.twinx()

    for p, n, s, u in zip(phases, nus, settings, U_As):
        ax.scatter(n, p, marker="o", s=20, label=s)

        # axr.scatter(n, u, marker=".", s=20)
    # axr.set_ylabel(r"$U_A \:\:/\:\: \si{\milli\volt}$,  (kleine Punkte)")
    # axr.set_yscale("log")

    ax.set_xlabel(r"$\nu \:\:/\:\: \si{\kilo\hertz}$")
    ax.set_ylabel(r"$\phi \:\:/\:\: \si{\degree}$")
    ax.set_xscale("log")
    # ax.legend(loc="lower left")

    ax.legend()
    fig.tight_layout(pad=0)
    fig.savefig("build/phases.png", bbox_inches="tight", pad_inches=0)
    fig.savefig("build/phases.pgf", bbox_inches="tight", pad_inches=0)
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
