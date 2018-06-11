import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd


def plot_T1():
    # Data

    tau, U = np.genfromtxt("data/messung_T1.txt", unpack=True)
    x = np.linspace(0, 10000, 10000)

    df = pd.DataFrame(
        data=np.array([tau, U]).transpose(),
        columns=[r"$\tau / \si{\milli\second}$", r"$U / \si{\milli\volt}$"],
    )

    with open("build/table_messung_T1.tex", "w") as ofile:
        ofile.write(
            df.to_latex(
                index=False,
                escape=False,
                column_format="S[table-format=5.1] S[table-format=-3.1]",
            )
        )

    def func(x, T_1, a, m):
        """-a * np.exp(-x / T_1) + m"""
        return -a * np.exp(-x / T_1) + m

    # Fit exp function
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 2, 1 / 4]  # weigh last two 3 times
    p0 = [2400, 1, 1]  # known-to-be T_1, others have default value
    par, cov = curve_fit(func, tau, U, p0=p0, sigma=weights)

    print(func.__doc__)
    for n, p, c in zip(["T_1", "a", "m"], par, np.sqrt(np.diag(cov))):
        print(r"{} = {:.2f} \pm {:.2f}".format(n, p, c))

    # plotting
    fig, ax = plt.subplots()
    # fig.set_size_inches([5.73, 3.57])

    ax.plot(tau, U, "C0x", label=r"Messung $T_1$")
    ax.plot(
        x,
        func(x, *par),
        "C1-",
        label=r"Fit: $T_1 = \SI{" + r"{:.2f}".format(par[0]) + r"}{\milli\second}$",
    )

    ax.set_xlabel(r"$\log_{10}(\tau \:\:/\:\: \si{\milli\second})$")
    ax.set_ylabel(r"$U \:\:/\:\: \si{\milli\volt}$")
    ax.set_xscale("log")

    ax.legend()
    fig.savefig("build/messung_T1.png")


if __name__ == "__main__":
    plot_T1()
