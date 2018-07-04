import numpy as np
import matplotlib.pyplot as plt


def plot(name):
    U_B = 14.7
    R1 = 0.1  # kOhm
    Rp = 9.6  # kOhm

    x, ch1, ch2 = np.genfromtxt(name, delimiter=",", skip_header=3, unpack=True)
    x += x[-1]
    x *= 1000

    fig, ax = plt.subplots()
    axr = ax.twinx()
    ax.plot(x, ch1, "-", c="C1", label="Schmitt-Trigger")
    axr.plot(x, ch2, ":", label="Eingangsspannung")

    ax.set_ylabel(r"$U \:\:/\:\: \si{\volt}$")
    axr.set_ylabel(r"$U \:\:/\:\: \si{\volt}$")
    ax.set_xlabel(r"$t \:\:/\:\: \si{\milli\second}$")

    trigger_point = np.argmax(ch2[1:] - ch2[:-1]) - 2
    sin_at_trigger = np.round(ch2[trigger_point], 3)
    print("Höhe des Sinus beim Triggerpunkt: {}".format(sin_at_trigger))

    scheitelspannung = np.round(U_B * R1 / Rp, 3)
    print("Scheitelspannung: {}".format(scheitelspannung))

    diff_scheit_triggered = np.abs(np.round(((sin_at_trigger - scheitelspannung) / scheitelspannung) * 100, 3))
    print("Relative Abweichung: {}%".format(diff_scheit_triggered))

    axr.scatter(x[trigger_point], ch2[trigger_point], marker="x")

    fig.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/schmitt.png", bbox_inches=0, pad_inches=0)
    fig.savefig("build/schmitt.pgf", bbox_inches=0, pad_inches=0)


def main():
    name = "./data/scope_269.csv"
    plot(name)


if __name__ == "__main__":
    main()
