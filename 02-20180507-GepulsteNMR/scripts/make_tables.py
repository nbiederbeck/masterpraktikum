"""Make LaTeX Tables from TXT Data Files."""
from numpy import genfromtxt


def make_table(filename):
    x, y = genfromtxt("data/{}.txt".format(filename), unpack=True)
    with open("build/table_{}.tex".format(filename), "w") as ofile:
        for x, y in zip(x, y):
            print(x, y, sep=" & ", end=" \\\\\n", file=ofile)


if __name__ == "__main__":
    make_table("messung_D")
    make_table("messung_T1")
