import numpy as np
import matplotlib.pyplot as plt


def main():
    fig, ax = plt.subplots()
    x = np.linspace(-1, 1, 101)
    ax.plot(x, x ** 2)
    ax.grid()
    fig.tight_layout()
    fig.savefig("build/plot.png")
    fig.savefig("build/plot.pgf")


if __name__ == "__main__":
    main()
