import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def plot_T1():
    # Data
    tau, U = np.genfromtxt("data/messung_T1.txt", unpack=True)
    x = np.linspace(0, 10000, 10000)

    def func(x, T_1, a, m):
        """-a * np.exp(-x / T_1) + m"""
        return -a * np.exp(-x / T_1) + m

    # Fit exp function
    weights = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 / 3, 1 / 4
    ]  # weigh last two 3 times
    p0 = [2400, 1, 1]  # known-to-be T_1, others have default value
    par, cov = curve_fit(func, tau, U, p0=p0, sigma=weights)

    print(func.__doc__)
    for n, p, c in zip(["T_1", "a", "m"], par, np.sqrt(np.diag(cov))):
        print("{}: {:.2f} +- {:.2f}".format(n, p, c))

    # plotting
    fig, ax = plt.subplots()
    fig.set_size_inches([5.73, 3.57])

    ax.plot(tau, U, "C0x", label=r"Messung $T_1$")
    ax.plot(
        x, func(x, *par), "C1-", label=r"Fit: $T_1 = ${:.2f}ms".format(par[0])
    )

    ax.set_xlabel(r"$\log_{10}(\tau \:\:/\:\: $ms)")
    ax.set_ylabel(r"$U \:\:/\:\: $mV")
    ax.set_xscale("log")

    ax.legend(loc="best")
    fig.tight_layout(pad=0)
    fig.savefig("build/messung_T1.png")


if __name__ == "__main__":
    plot_T1()
