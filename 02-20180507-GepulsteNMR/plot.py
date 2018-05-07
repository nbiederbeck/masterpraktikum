import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


def plot():
    fig = plt.figure()

    ax = fig.add_subplot(111)

    x = np.arange(-6, 6, 101)
    y = x ** 2

    ax.plot(x, y)
    fig.savefig("build/plot.png")


def get_diffusion():
    fig, ax = plt.subplots()
    x = np.log(M_y / M_0) + t / T_2
    y = t ** 3
    ax.plot(x, y, label="Diffusion")
    fig.savefig("build/diffusion.png")


def plot_mg():
    df1 = pd.read_csv('data/scope_2_1.csv', header=[0,1])
    df2 = pd.read_csv('data/scope_3_1.csv', header=[0,1])
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    df1.plot('x-axis', '1',
            # marker='x',
            ax=ax1)
    df2.plot('x-axis', '1',
            # marker='x',
            ax=ax2)
    fig.savefig('build/mg.png')


def plot_T1():
    tau, U = np.genfromtxt("data/messung_T1.txt", unpack=True)
    U += 1000
    x = np.linspace(0, 10000, 10000)

    def func(x, a, b, m):
        return -b * np.exp(-x / a) - m

    par, cov = curve_fit(func, tau, U)
    fig, ax = plt.subplots()
    ax.plot(tau, U, "C0x", label=r"Messung $T_1$")
    ax.plot(
        x, func(x, *par), "C1-", label=r"Fit: $T_1 = ${:.2f}ms".format(par[0])
    )
    ax.set_xlabel(r"$\tau / $ms")
    ax.set_ylabel(r"$U / $mV")
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    ax.legend(loc="best")
    fig.tight_layout(pad=0)
    fig.savefig("build/messung_T1.png")

def plot_D():
    tau, U = np.genfromtxt('data/messung_D.txt', unpack=True)
    x = np.linspace(0, 15, 1000)
    fig, ax = plt.subplots()
    ax.plot(tau, U, "C0x", label=r"Messung $D$")
    ax.set_xlabel(r"$\tau / $ms")
    ax.set_ylabel(r"$U / $mV")
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    ax.legend(loc="best")
    fig.tight_layout(pad=0)
    fig.savefig("build/messung_D.png")



def printer():
    OFILE = "build/helloworld.tex"
    with open(OFILE, "w") as ofile:
        for c1, c2 in zip("Hallo", "Welt!"):
            print(c1, c2, sep=" & ", end=" \\\\\n", file=ofile)


def main():
    plot_T1()
    plot_mg()
    plot_D()


if __name__ == "__main__":
    main()
