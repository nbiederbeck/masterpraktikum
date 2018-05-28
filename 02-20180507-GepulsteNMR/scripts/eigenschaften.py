from pint import UnitRegistry
from math import pi

from scipy.constants import physical_constants as phyconst

ureg = UnitRegistry()
ureg.default_format = ".2fLx"


def viskos(t, show=False):
    """Vergleiche Anleitung an der Apparatur"""
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
    """Vergleiche Seite 20 in der Anleitung"""
    k_boltzmann = 1.38e-23 * ureg("joule per kelvin")
    T *= ureg("kelvin")
    T += 273 * ureg("kelvin")
    D = 1.71e-08 * ureg("meter ** 2 per second")
    r = k_boltzmann * T / (6 * pi * eta * D)
    return r.to("angstrom")


def vergleich1_molekulargewicht():
    M = 18 * ureg("gram / mol")
    rho = 1 * ureg("gram / centimeter ** 3")
    avogadro_constant = phyconst["Avogadro constant"]
    avogadro_constant = avogadro_constant[0] * ureg(avogadro_constant[1])
    r = (M / rho / avogadro_constant) ** (1 / 3)
    return r.to("angstrom")


def vergleich2_kritischerDruck_Temperatur():
    molar_mass_water = 18 * ureg("gram per mol")
    molar_gas_constant = phyconst["molar gas constant"]
    molar_gas_constant = molar_gas_constant[0] * ureg(molar_gas_constant[1])
    avogadro_constant = phyconst["Avogadro constant"]
    avogadro_constant = avogadro_constant[0] * ureg(avogadro_constant[1])

    # https://de.wikipedia.org/wiki/Van-der-Waals-Gleichung
    a_water = 557.29 * 1e-3 * ureg("joule meter ** 3 / mol ** 2")
    b_water = 31 * 1e-6 * ureg("meter ** 3 / mol")
    p_crit_water = a_water / (27 * b_water ** 2)
    T = (22 + 273) * ureg("kelvin")

    V_crit_water = b_water / avogadro_constant
    V_crit_water = 3 * b_water / avogadro_constant
    r_crit_water = (V_crit_water / pi / (4 / 3)) ** (1 / 3)
    return r_crit_water.to("angstrom")


if __name__ == "__main__":
    t = 915 * ureg("second")
    eta = viskos(t)
    r0 = radius(eta)
    r1 = vergleich1_molekulargewicht()
    r2 = vergleich2_kritischerDruck_Temperatur()
    with open("build/radii.tex", "w") as ofile:
        print(
            r"r_\text{Viskositaet} &= " + "{}".format(r0),
            end=" \\\\\n",
            file=ofile,
        )
        print(
            r"r_\text{Molekuelradius} &= " + "{}".format(r1),
            end=" \\\\\n",
            file=ofile,
        )
        print(r"r_\text{VdW} &= " + "{}".format(r2), end="\n", file=ofile)
