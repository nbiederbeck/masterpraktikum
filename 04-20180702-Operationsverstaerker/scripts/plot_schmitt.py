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

    trig_pos = np.argmax(ch2[1:] - ch2[:-1]) - 2
    sin_trig_pos = np.round(ch2[trig_pos], 3)
    print("Höhe des Sinus beim positiven Triggerpunkt: {}".format(sin_trig_pos))

    trig_neg = np.argmin(ch2[1:] - ch2[:-1]) - 2
    sin_trig_neg = np.round(ch2[trig_neg], 3)
    print("Höhe des Sinus beim negativen Triggerpunkt: {}".format(sin_trig_neg))

    scheitelspannung = np.round(U_B * R1 / Rp, 3)
    print("Scheitelspannung: {}".format(scheitelspannung))

    diff_scheit_triggered = np.abs(
        np.round(((sin_trig_pos - scheitelspannung) / scheitelspannung) * 100, 3)
    )
    print("Relative Abweichung Pos: {}%".format(diff_scheit_triggered))
    diff_scheit_triggered = np.abs(
        np.round(((sin_trig_neg - -scheitelspannung) / -scheitelspannung) * 100, 3)
    )
    print("Relative Abweichung Neg: {}%".format(diff_scheit_triggered))

    axr.scatter(x[trig_pos], ch2[trig_pos], marker="x", color="C0")
    axr.scatter(x[trig_neg], ch2[trig_neg], marker="x", color="C0")

    fig.legend()

    fig.tight_layout(pad=0)
    fig.savefig("build/schmitt.png", bbox_inches=0, pad_inches=0)
    fig.savefig("build/schmitt.pgf", bbox_inches=0, pad_inches=0)
    fig.savefig("build/schmitt.pdf", bbox_inches=0, pad_inches=0)


def main():
    name = "./data/scope_269.csv"
    plot(name)


if __name__ == "__main__":
    main()
