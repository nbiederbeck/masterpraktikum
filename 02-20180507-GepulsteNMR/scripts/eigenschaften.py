from pint import UnitRegistry
from math import pi

ureg = UnitRegistry()
ureg.default_format = "Lx"


def viskos(t, show=False):
    alpha = 1.024e-9 * ureg("meter ** 2 / second ** 2")
    delta = 0.5 * ureg("second")
    rho = 1 * ureg("gram / centimeter ** 3")
    eta = alpha * rho * (t - delta)
    if show:
        print(r"$\alpha = {}$".format(alpha))
        print(r"$\delta = {}$".format(delta))
        print(r"$\rho = {}$".format(rho))
        print(eta.to("millipascal second"))
    return eta


def radius(eta, T=22):
    k_boltzmann = 1.38e-23 * ureg('joule per kelvin')
    T *= ureg('kelvin')
    T += 273 * ureg('kelvin')
    D = 1.71e-17 * ureg('meter ** 2 per second')
    r = k_boltzmann * T / (6 * pi * eta * D)
    return r.to_base_units()


def vergleich1_molekulargewicht():
    M = 18 * ureg('gram')
    rho = 1 * ureg("gram / centimeter ** 3")
    r = (M / rho) ** (1/3)
    return r.to_base_units()


if __name__ == "__main__":
    t = 915 * ureg("second")
    eta = viskos(t)
    print(eta)
    r0 = radius(eta)
    print(r0)
    r1 = vergleich1_molekulargewicht()
    print(r1)
