import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


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

    def func(x, D, a, m):
        """-a * np.exp(-x / D) + m"""
        return -a * np.exp(-x / D) + m

    # Fit exp function
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # weigh last two 3 times
    p0 = [1, 1, 1]
    par, cov = curve_fit(func, tau, U, p0=p0, sigma=weights)

    print(func.__doc__)
    for n, p, c in zip(["D", "a", "m"], par, np.sqrt(np.diag(cov))):
        print("{}: {:.2f} +- {:.2f}".format(n, p, c))

    fig, ax = plt.subplots()

    ax.plot(tau, U, "C0x", label=r"Messung $D$")
    ax.plot(x, func(x, *par), "C1-", label="")
    ax.set_xlabel(r"$\tau \:\:/\:\: \si{\milli\second}$")
    ax.set_ylabel(r"$U \:\:/\:\: \si{\milli\volt}$")

    ax.legend()
    fig.savefig("build/messung_D.png")


def printer():
    OFILE = "build/helloworld.tex"
    with open(OFILE, "w") as ofile:
        for c1, c2 in zip("Hallo", "Welt!"):
            print(c1, c2, sep=" & ", end=" \\\\\n", file=ofile)


if __name__ == "__main__":
    plot_D()
