import numpy as np


def calc_freq():
    C = 20.8e-9  # Farad
    R = 30.2e3  # Ohm
    T = 2 * np.pi * R * C
    nu = 2 * np.pi / (R * C)
    nu = 1.0 / T
    nu = np.round(nu, 0)
    print(r"\nu_\text{theo} = \SI{" + f"{nu}" + r"}{\hertz}")


def main():
    calc_freq()


if __name__ == "__main__":
    main()
