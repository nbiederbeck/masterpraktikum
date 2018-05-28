import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

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

    def func(x, d, a, m):
        """a * np.exp(- x**3 * d) + m"""
        return a * np.exp(-x ** 3 * d) + m

    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    p0 = [1, 1, 1]
    par, cov = curve_fit(func, tau, U, p0=p0, sigma=weights)

    print(func.__doc__)
    for n, p, c in zip(["d", "a", "m"], par, np.sqrt(np.diag(cov))):
        print(r"{} &= {} \pm {}".format(n, p, c))

    T_2 = 1.47 * ureg("second")
    gammap = 2.68e8 * ureg("radians per second per tesla")
    G = 8.1e-5 * ureg("tesla per millimeter per radians")
    D = par[0] * ureg("millisecond") ** -3 * 12 / (gammap ** 2 * G ** 2)
    print(r"D = {}".format(D.to(ureg("meter ** 2 / second"))))
    with open("build/D.tex", "w") as ofile:
        print(
            r"D &= {:.2fLx}".format(D.to(ureg("micrometer ** 2 / second"))),
            file=ofile,
        )

    fig, ax = plt.subplots()

    ax.plot(tau, U, "C0x", label=r"Messung $D$")
    ax.plot(x, func(x, *par), "C1-", label="Fit")

    ax.set_xlabel(r"$\tau \:\:/\:\: \si{\milli\second}$")
    ax.set_ylabel(r"$U \:\:/\:\: \si{\milli\volt}$")

    ax.legend()
    fig.savefig("build/messung_D.png")


if __name__ == "__main__":
    plot_D()
