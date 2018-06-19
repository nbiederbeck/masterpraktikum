import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import uncertainties as unc

from pint import UnitRegistry

ureg = UnitRegistry()
ureg.default_format = "Lx"


def plot_D():
    tau, U = np.genfromtxt("data/messung_D.txt", unpack=True)
    x = np.linspace(0, 15, 1000)

    df = pd.DataFrame(
        data=np.array([tau, U]).transpose(),
        columns=[r"$\tau / \si{\milli\second}$", r"$U / \si{\milli\volt}$"],
    )

    with open("build/table_messung_D.tex", "w") as ofile:
        ofile.write(
            df.to_latex(
                index=False,
                escape=False,
                column_format="S[table-format=2.1] S[table-format=-3.1]",
            )
        )

    T_2 = 1.47 * ureg("second")

    def func(x, d, a, m, b):
        return a * np.exp(-x ** 3 * d) * np.exp(-b * x / T_2.magnitude) + m

    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    p0 = [0.0003, -800, 1, 1]
    par, cov = curve_fit(func, tau, U, p0=p0, sigma=weights)
    diag_cov = np.sqrt(np.diag(cov))

    par[0] = np.round(par[0], 4)
    diag_cov[0] = np.round(diag_cov[0], 4)
    par[1] = np.round(par[1], 0)
    diag_cov[1] = np.round(diag_cov[1], 0)
    par[2] = np.round(par[2], 0)
    diag_cov[2] = np.round(diag_cov[2], 0)
    par[3] = np.round(par[3], 3)
    diag_cov[3] = np.round(diag_cov[3], 3)

    with open("build/D_params.tex", "w") as ofile:
        for n, p, c in zip(["d", "a", "m", "b", "c"], par, diag_cov):
            print(
                r"{} &= ".format(n)
                + "\SI{"
                + "{:} \pm {:}".format(p, c)
                + "}"
                + "{"
                + r"{}".format(
                    r"\per\milli\second\tothe3"
                    if n == "d"
                    else r"\milli\second"
                    if n == "b"
                    else r"\milli\volt"
                )
                + ("}" if n == "c" else "} \\\\")
            )
            print(
                r"{} &= ".format(n)
                + "\SI{"
                + "{:} \pm {:}".format(p, c)
                + "}"
                + "{"
                + r"{}".format(
                    r"\per\milli\second\tothe3"
                    if n == "d"
                    else r""
                    if n == "b"
                    else r"\milli\volt"
                )
                + ("}" if n == "c" else "} \\\\"),
                file=ofile,
            )

    gammap = 2.68e8 * ureg("radians per second per tesla")
    G = 81 * ureg("millitesla per meter")
    d = unc.ufloat(par[0], diag_cov[0])
    D = d * ureg("millisecond ** -3") * 12 / (2 ** 2 * gammap ** 2 * G ** 2)
    D.ito("meter ** 2 / second")
    ureg.default_format = ""
    D_precision = 10
    D = unc.ufloat(
        np.around(D.magnitude.n, D_precision),
        np.around(D.magnitude.s, D_precision),
    ) * ureg(str(D.units))

    print(
        r"D &= {:.Lx}".format(D)
        .replace("+/-", r"\pm")
        .replace("(", "")
        .replace(")", "")
        .replace(r"\pm0", "")
    )
    with open("build/D.tex", "w") as ofile:
        print(
            r"D &= {:.Lx}".format(D)
            .replace("+/-", r"\pm")
            .replace("(", "")
            .replace(")", "")
            .replace(r"\pm0", ""),
            file=ofile,
        )

    # with open("build/D.txt", "wb") as ofile:
    # print(D.magnitude.n, file=ofile)
    # print(D.units, file=ofile)
    # np.save(ofile, D)

    np.save("build/D_magnitude", D.magnitude)
    np.save("build/D_units", D.units)

    fig, ax = plt.subplots()

    ax.plot(tau, U, "C0x", label=r"Messung $D$")
    ax.plot(x, func(x, *par), "C1-", label="Fit")

    ax.set_xlabel(r"$\tau \:\:/\:\: \si{\milli\second}$")
    ax.set_ylabel(r"$U \:\:/\:\: \si{\milli\volt}$")

    ax.legend()
    fig.savefig("build/messung_D.png")


if __name__ == "__main__":
    plot_D()
