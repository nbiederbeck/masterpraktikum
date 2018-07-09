import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit


def fit(x, m, b):
    return np.log(m) * np.log(x) + b


def fit(t, U0, w, tau, b, phi):
    return U0 * np.exp(-t / tau) * np.sin(t * w + phi) + b


def plot(name):
    x, ch1, ch2 = np.genfromtxt(
        name, delimiter=",", skip_header=3, unpack=True
    )

    start_index = np.where(x >= 1e-3)[0][0]
    x = x[start_index:]
    ch1 = ch1[start_index:]

    peaks, _ = find_peaks(ch1[ch1 > 0], distance=15)
    peakx, peaky = x[ch1 > 0][peaks], ch1[ch1 > 0][peaks]
    peakx, peaky = x, ch1

    par, cov = curve_fit(fit, peakx, peaky, p0=[1.6, 1 / 0.01, 0.01, 1, 0.0])
    lin = np.linspace(np.min(x), np.max(peakx) * 1.3, 1001)

    R = 10e3
    C = 20.8e-9
    T = 2 * np.pi * R * C
    tau_theo = 20 * R * C
    f = 1.0 / T
    omega = f * 2 * 3.1415962
    print("tau_theo / s", tau_theo)
    print("Delta tau / %", 100 * np.abs(1 - par[2] / tau_theo))
    print("f_theo / Hz", f)
    print("omega_theo / Hz", omega)
    print("Delta omega / %", 100 * np.abs(1 - par[1] / omega))

    for n, p, c in zip(
        ["U_0", "w", "tau", "b", "phi"],
        np.round(par, 4),
        np.round(np.sqrt(np.diag(cov)), 4),
    ):
        print("{}: {} \\pm {}".format(n, p, c))

    fig, ax = plt.subplots()

    ax.scatter(x, ch1, marker="x", label="Gedämpfte Schwingung, Messung")
    ax.plot(lin, fit(lin, *par), color="C1", label="Fit")

    ax.set_xlabel(r"$t \:\:/\:\: \si{\second}$")
    ax.set_ylabel(r"$U \:\:/\:\: \si{\volt}$")

    ax.set_xscale("log")

    ax.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/gedaempfte_schwingung.png")
    fig.savefig("build/gedaempfte_schwingung.pgf")


def main():
    name = "data/scope_274.csv"
    plot(name)


if __name__ == "__main__":
    main()
