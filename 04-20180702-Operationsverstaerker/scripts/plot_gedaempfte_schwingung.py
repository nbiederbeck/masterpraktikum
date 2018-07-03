import numpy as np
import matplotlib.pyplot as plt


def plot(name):
    x, ch1, ch2 = np.genfromtxt(name, delimiter=",", skip_header=2, unpack=True)

    fig, ax = plt.subplots()
    scale = 0.8
    fig.set_size_inches(
        scale * fig.get_figwidth(), scale * fig.get_figheight()
    )

    ax.plot(x, ch1)
    fig.tight_layout(pad=0)
    fig.savefig("build/gedaempfte_schwingung.png")
    fig.savefig("build/gedaempfte_schwingung.pgf")


def main():
    name = "data/scope_274.csv"
    plot(name)


if __name__ == "__main__":
    main()
