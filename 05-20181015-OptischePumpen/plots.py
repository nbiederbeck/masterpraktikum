import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, constants
from scipy.optimize import curve_fit
from glob import glob
import pickle
from uncertainties import ufloat, unumpy


class spulen:
    def __init__(self):
        self.spulen = {
            "sweep": {"radius": 16.39e-2, "N": 11, "R": 1.0},
            "horizontal": {"radius": 15.79e-2, "N": 154, "R": 0.5},
            "vertical": {"radius": 11.735e-2, "N": 20, "R": 0.5},
        }

    def calc_b_helmoltz(self, spule, U):
        return (
            constants.mu_0
            * 8
            * (U / self.spulen[spule]["R"])
            * self.spulen[spule]["N"]
            / (np.sqrt(125) * self.spulen[spule]["radius"])
        )

    def calc_b_gesamt(self, U_sweep, U_horiz):
        B_Sweep = self.calc_b_helmoltz("sweep", U_sweep)
        B_Horiz = self.calc_b_helmoltz("horizontal", U_horiz)
        return B_Sweep + B_Horiz


class static_experiment:
    def __init__(self):
        self.nu, self.p1_s, self.p1_h, self.p2_s, self.p2_h = np.genfromtxt(
            "data/task_c.txt", unpack=True
        )
        self.nu *= 1e3
        self.spu = spulen()

    def calc_earth_b_static(self):
        s = self.spu.calc_b_helmoltz("sweep", 0.32)
        v = self.spu.calc_b_helmoltz("vertical", 0.12)
        print("Magnetfeld der Erde")
        print("Verticale komponente : ", v, "T")
        print("Horizontale komponente : ", s, "T")
        return s, v

    def frequenz_B_fit(self):
        B1 = self.spu.calc_b_gesamt(self.p1_s, self.p1_h)
        B2 = self.spu.calc_b_gesamt(self.p2_s, self.p2_h)

        df = pd.DataFrame(
            {
                r"$\nu$ / \si{\kilo\hertz}": self.nu / 1e3,
                r"$B_{85}$ / \si{\micro\tesla}": np.round(B1 * 1e6, 2),
                r"$B_{87}$ / \si{\micro\tesla}": np.round(B2 * 1e6, 2),
            }
        )
        with open("build/b_nu.tex", "w") as tf:
            tf.write(
                df.to_latex(
                    column_format="S[zero-decimal-to-integer=true,table-format=4.0]SS",
                    escape=False,
                    index=False,
                    sparsify=True,
                )
            )
        self.params = []
        self.std = []

        def f(x, m, b):
            return m * x + b

        for B, nu in zip([B1, B2], [self.nu, self.nu]):
            popt, pcov = curve_fit(f, nu, B)
            cov = np.sqrt(np.diag(pcov))
            self.std.append(cov)
            self.params.append(popt)
        df = pd.DataFrame(
            {
                r"a / Ts": [self.params[0][0], self.params[1][0]],
                r"$\Delta$ a / Ts": [self.std[0][0], self.std[1][0]],
                r"b / T": [self.params[0][1], self.params[1][1]],
                r"$\Delta$ b / T": [self.std[0][1], self.std[1][1]],
            }
        )
        with open("build/lin_params.tex", "w") as tf:
            tf.write(
                df.to_latex(
                    column_format="SSS[scientific-notation =true]S",
                    escape=False,
                    index=False,
                    sparsify=True,
                )
            )
        return nu, [B1, B2], self.params, self.std

    def horizontal_E_Feld(self):
        self.frequenz_B_fit()
        B_Erde = []
        for x in range(2):
            B_Erde.append(ufloat(self.params[x][1], self.std[x][1]))
        print("Das Magnetfeld der Erde beträgt: ", np.mean(B_Erde), " T")
        return np.mean(B_Erde)

    def lande_Faktoren(self):
        self.frequenz_B_fit()
        self.lande = []
        for x in range(2):
            quot = ufloat(self.params[x][0], self.std[x][0])
            self.lande.append(4 * np.pi * constants.m_e / (constants.e * quot))
        print("Die Landefaktoren betragen:")
        print("Rb^87: ", self.lande[0])
        print("Rb^85: ", self.lande[1])
        df = pd.DataFrame(
            {
                "": [r"Rb$_{87}$", r"Rb$_{85}$"],
                r"$g_\text{theo}$": [r"$\sfrac{1}{2}$", r"$\sfrac{1}{3}$"],
                r"$g_\text{exp}$": [
                    self.lande[0].nominal_value,
                    self.lande[1].nominal_value,
                ],
                r"$\Delta g_\text{exp}$": [
                    self.lande[0].std_dev,
                    self.lande[1].std_dev,
                ],
            }
        )
        with open("build/lande.tex", "w") as tf:
            tf.write(
                df.to_latex(
                    column_format="SS[table-format=2.0]S[round-mode=places,round-precision=3,table-format=0.3]S[round-mode=places,round-precision=3,table-format=0.3]",
                    escape=False,
                    index=False,
                    sparsify=True,
                )
            )

        return self.lande[0], self.lande[1]

    def kernspins(self):
        self.J = 1 / 2
        self.g_j = 2.0023

        def kernspin(lande):
            return self.J * (self.g_j / lande - 1)

        lande_87, lande_85 = self.lande_Faktoren()
        I_85 = kernspin(lande_85)
        I_87 = kernspin(lande_87)
        print("Der Kernspin ist: ", I_85, " und ", I_87)
        df = pd.DataFrame(
            {
                "": [r"Rb$_{87}$", r"Rb$_{85}$"],
                r"$I_\text{theo}$": [r"$\sfrac{3}{2}$", r"$\sfrac{5}{2}$"],
                r"$I_\text{exp}$": [I_85.nominal_value, I_87.nominal_value],
                r"$\Delta I_\text{exp}$": [I_85.std_dev, I_87.std_dev],
            }
        )
        with open("build/kernspin.tex", "w") as tf:
            tf.write(
                df.to_latex(
                    column_format="SS[table-format=2.0]S[round-mode=places,round-precision=3,table-format=0.3]S[round-mode=places,round-precision=3,table-format=0.3]",
                    escape=False,
                    index=False,
                    sparsify=True,
                )
            )
        return I_85, I_87

    def isotopen_ratio(self):
        self.amplitude_85 = 13
        self.amplitude_87 = 7
        self.ratio = np.round(self.amplitude_85 / self.amplitude_87, 2)
        print("Das Verhätniss 85/87 ist: ", self.ratio)
        return self.ratio

    def squared_zee(self):
        delta_E = 2e-24
        B = 1e-3
        M_F = 1
        lin_zee = self.lande[0] * constants.physical_constants["Bohr magneton"][0] * B
        squared_zee = lin_zee ** 2 * (1 - 2 * M_F) / delta_E
        print("Zeemann linear: ", lin_zee)
        print("Zeemann squared: ", squared_zee)
        print("Zeemann quotient: ", 100 * squared_zee / lin_zee)
        return lin_zee, squared_zee


class larmor_sweep:
    def __init__(self, csvPath, spulenU, upperTLim=2.5e-3, lowerTLim=-1e-5):
        df = pd.read_csv(csvPath)
        data = pd.DataFrame(df.loc[18:].values[:, 3:5], columns=["time", "voltage"])
        # self.timescale = float(df.loc[10].values[1])
        # data.time = data.time.values / self.timescale
        self.mask = (data.time > lowerTLim) & (data.time < upperTLim)
        self.data = data[self.mask].reset_index()
        self.lowerTLim = lowerTLim
        self.upperTLim = upperTLim
        self.spulenU = spulenU

    def find_peaks(self, distance=None):
        if distance == None:
            distance = sum(self.mask) / 8
        self.uMean = np.mean(self.data["voltage"])
        peaks, _ = signal.find_peaks(
            self.data["voltage"], height=self.uMean, distance=sum(self.mask) / 20
        )
        self.tPeaks = self.data["time"][peaks]
        self.uPeaks = self.data["voltage"][peaks]
        self.tDist = self.tPeaks.values[1:] - self.tPeaks.values[:-1]
        self.tDist = ufloat(np.mean(self.tDist), np.std(self.tDist))
        return self.tDist.nominal_value, self.tDist.std_dev

    def save_info(self, path, find_peaks_dict={}):
        # self.find_peaks(*find_peaks_dict)
        df = {
            "lowerTLim": self.lowerTLim,
            "upperTLim": self.upperTLim,
            "uMean": self.uMean,
            "tPeaks": self.tPeaks,
            "uPeaks": self.uPeaks,
            "tDist": self.tDist,
            "time": self.data.time.values,
            "voltage": self.data.voltage,
            "spulenU": self.spulenU,
        }
        pickle.dump(df, open(path + str(int(self.spulenU)) + ".pkl", "wb"))


class plotter:
    def __init__(self):
        self.df = None
        pass

    def load_data(self, path):
        self.df = pickle.load(open(path, "rb"))

    def plot_nu_b(self, nu, b, params, figPath="build/static_B.pdf"):
        def f(x, m, b):
            return m * x + b

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x_sample = np.linspace(0, max(nu), 3)
        label = [r"Rb$^{87}$", r"Rb$^{85}$"]
        for x in range(2):
            ax.plot(nu/1e3, b[x]*1e6, 'x')
            ax.plot(x_sample/1e3, f(x_sample, *params[x])*1e6, label=label[x])
        ax.set_xlim(xmin=0)
        # ax.set_ylim(0.05*min(b.flatten()), 1.05*max(b.flatten()))
        ax.set_xlabel(r'$\nu$ / kHz')
        ax.set_ylabel('B / $\si{\micro \\tesla}$')
        ax.legend(loc='best')
        fig.savefig(figPath)
        plt.close()

    def plot_peaks(self, figPath):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.df["time"], self.df["voltage"])
        ax.axhline(self.df["uMean"], linestyle="--", color="r")
        ax.scatter(self.df["tPeaks"], self.df["uPeaks"], label="detected peak")
        ax.set_xlim(self.df["lowerTLim"], self.df["upperTLim"])
        ax.set_xlabel("Zeit / s")
        ax.set_ylabel("Spannung / U")
        ax.set_title("T = " + str(self.df["tDist"] * 1e3) + " ms")
        plt.legend(loc="best")
        fig.savefig(figPath)
        plt.close()

    def f_hyp(self, U, a, b, c):
        return a + b / (U + c)

    def fit_hyperbel(self, U, T):
        print("U: ", U)
        print("T: ", T)
        popt, pcov = curve_fit(self.f_hyp, U, T)
        return popt, np.sqrt(np.diag(pcov))

    def plot_U_T(self, U, T, figPath):
        mT = np.array(T) * 1000
        popt, cov = self.fit_hyperbel(U, mT)
        fig = plt.figure(figsize=(3,2))
        ax = fig.add_subplot(111)
        ax.plot(U, mT, "x")
        ax.plot(np.linspace(1, 10, 50), self.f_hyp(np.linspace(1, 10, 50), *popt))
        ax.set_xlabel("U / V")
        ax.set_ylabel("T / ms")
        plt.tight_layout()
        fig.savefig(figPath)
        plt.close()
        return popt, cov


def statisch():
    stc = static_experiment()
    stc.calc_earth_b_static()
    nu, B, params, stds = stc.frequenz_B_fit()
    stc.horizontal_E_Feld()
    # stc.lande_Faktoren()
    stc.kernspins()
    stc.isotopen_ratio()
    stc.squared_zee()

    plttr = plotter()
    plttr.plot_nu_b(nu, B, params)


def sweep(isotope, TLim, selectedU):
    plttr = plotter()
    csvPath = "data/" + isotope + "/"
    T = []
    Std_t = []
    for U in selectedU:
        uStr = str(int(U))

        print("Processing U=: ", U)
        lam = larmor_sweep(csvPath + uStr + "V.CSV", U, upperTLim=TLim[U - 1])
        t, std_t = lam.find_peaks()
        T.append(t)
        Std_t.append(std_t)
        lam.save_info(csvPath)

        print("Plotting U=: ", U)
        plttr.load_data(csvPath + uStr + ".pkl")
        plttr.plot_peaks("build/" + isotope + "_" + uStr + ".png")
    print("T: ", T)
    print("Std_t: ", Std_t)
    popt, cov = plttr.plot_U_T(selectedU, T, "build/" + isotope + ".pdf")
    params = unumpy.uarray(popt, cov)
    print("Params", params)
    print("Done")

    return selectedU, T, params


def main():
    statisch()
    firstTLim = np.array([10.0, 10.0, 1.5, 2.5, 2.5, 1.5, 1.5, 2.5, 2.5, 1.5]) * 1e-3
    secondTLim = np.array([5, 2, 2.1, 5, 3, 3, 3, 3, 3, 3]) * 1e-3
    selectedU = [1, 2, 4, 5, 6, 7, 8, 9, 10]
    U1, T1, params1 = sweep("firstPeak", firstTLim, selectedU)
    U2, T2, params2 = sweep("secondPeak", secondTLim, range(3, 11))

    df = pd.DataFrame({"U / V": U1, "T / s": T1})
    with open("build/T1.tex", "w") as tf:
        tf.write(
            df.to_latex(
                column_format="S[zero-decimal-to-integer=true,table-format=2.0]S[round-mode=figures,round-precision=3,table-format=1.2e2,scientific-notation=true]",
                escape=False,
                index=False,
                sparsify=True,
            )
        )

    df = pd.DataFrame({"U / V": U2, "T / s": T2})
    with open("build/T2.tex", "w") as tf:
        tf.write(
            df.to_latex(
                column_format="S[zero-decimal-to-integer=true,table-format=2.0]S[round-mode=figures,round-precision=3,table-format=1.2e2,scientific-notation=true]",
                escape=False,
                index=False,
                sparsify=True,
            )
        )

    print("b1/b2: ", params2[1] / params1[1])


if __name__ == "__main__":
    main()
