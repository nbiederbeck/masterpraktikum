import numpy as np


def calc_freq():
    C = 20.8e-9  # Farad
    R = 30.2e3  # Ohm
    R_1 = 0.1e3  # Ohm
    R_p = 1e3  # Ohm
    t = R_1 * R * C / R_p * 2.0
    T = 2.0 * t
    U_B = 14.7

    # # Ryan
    # C = 20e-9
    # R_p = 99.4e3
    # R_1 = 1e3
    # R = 99.8e3
    # t = R_1 * R * C / R_p * 2.0
    # T = 2.0 * t

    nue = 1990
    nu = 1.0 / T
    nu = np.round(nu, 0)
    dnu = (nu - nue) / nu * 100

    print(r"\nu_\text{theo} = \SI{" + f"{nu}" + r"}{\hertz}")
    print(r"\Delta \nu = " + f"{dnu}\\%")

    Ae = 1.28
    A = np.round(U_B * R_1 / R_p, 3)
    dA = np.round((A - Ae) / A * 100, 1)

    print(r"A_\text{theo} = \SI{" + f"{A}" + r"}{\volt}")
    print(r"\Delta A = " + f"{dA}\\%")


def main():
    calc_freq()


if __name__ == "__main__":
    main()
