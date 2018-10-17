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
                'sweep': {
                    'radius': 16.39e-2, 'N': 11, 'R': 1.0
                    },
                "horizontal" : {
                    'radius': 15.79e-2, 'N': 154, 'R': 0.5
                    },
                "vertical" : {
                    'radius': 11.735e-2, 'N': 20, 'R': 0.5
                    }
                }

    def calc_b_helmoltz(self, spule, U):
        return constants.mu_0 * 8 * (U/self.spulen[spule]['R']) *   \
            self.spulen[spule]['N'] / ( np.sqrt(125) *          \
            self.spulen[spule]['radius'] )

    def calc_b_gesamt(self, U_sweep, U_horiz):
        B_Sweep = self.calc_b_helmoltz("sweep", U_sweep)
        B_Horiz = self.calc_b_helmoltz("horizontal", U_horiz)
        return B_Sweep + B_Horiz

class static_experiment:
    def __init__(self):
        self.nu, self.p1_s, self.p1_h, self.p2_s, \
                self.p2_h = np.genfromtxt(
                        'data/task_c.txt', unpack=True)
        self.spu = spulen()

    def calc_earth_b_static(self):
        s = self.spu.calc_b_helmoltz('sweep', 0.32)
        v = self.spu.calc_b_helmoltz('vertical', 0.12)
        print('Magnetfeld der Erde')
        print('Verticale komponente : ', v, 'T')
        print('Horizontale komponente : ', s, 'T')
        return s, v

    def frequenz_B_fit(self):
        B1 = self.spu.calc_b_gesamt(self.p1_s, self.p1_h)
        B2 = self.spu.calc_b_gesamt(self.p2_s, self.p2_h)

        def f(x, m, b):
            return m * x + b

        params = []
        std = []
        for B, nu in zip([B1,B2], [self.nu, self.nu]):
            popt, pcov = curve_fit(f, nu, B)
            cov = np.sqrt(np.diag(pcov))
            std.append(cov)
            params.append(popt)
        return nu, [B1, B2], params, std



class larmor_sweep:
    def __init__(self, csvPath, spulenU, upperTLim=2.5e-3, lowerTLim=-1e-5):
        df = pd.read_csv(csvPath)
        data = pd.DataFrame(
                df.loc[18:].values[:,3:5],
                columns=['time', 'voltage'])
        # self.timescale = float(df.loc[10].values[1])
        # data.time = data.time.values / self.timescale
        self.mask = (data.time > lowerTLim) & \
                (data.time < upperTLim)
        self.data = data[self.mask].reset_index()
        self.lowerTLim = lowerTLim
        self.upperTLim = upperTLim
        self.spulenU = spulenU

    def find_peaks(self, distance=None):
        if distance==None:
            distance=sum(self.mask)/20
        self.uMean = np.mean(self.data['voltage'])
        peaks, _ = signal.find_peaks(
                self.data['voltage'], 
                height=self.uMean, 
                distance=sum(self.mask)/10)
        self.tPeaks = self.data['time'][peaks]
        self.uPeaks = self.data['voltage'][peaks]
        self.tDist = self.tPeaks.values[1:] - self.tPeaks.values[:-1]
        return self.tPeaks, self.uPeaks


    def save_info(self, path, find_peaks_dict={}):
        self.find_peaks(*find_peaks_dict)
        df = {
                "lowerTLim": self.lowerTLim, 
                "upperTLim": self.upperTLim,
                "uMean": self.uMean,
                "tPeaks": self.tPeaks,
                "uPeaks": self.uPeaks,
                "tDist": ufloat(np.mean(self.tDist), np.std(self.tDist)),
                "time": self.data.time.values,
                "voltage": self.data.voltage,
                "spulenU": self.spulenU,
                }
        pickle.dump(df, open(path+ str(int(self.spulenU))+ ".pkl",'wb'))

class plotter:
    def __init__(self):
        self.df = None
        pass

    def load_data(self, path):
        self.df = pickle.load(open(path, 'rb'))

    def plot_nu_b(self, nu, b, params, figPath='build/test.pdf'):
        def f(x, m, b):
            return m * x + b

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x_sample = np.linspace(0,max(nu), 3)
        label = [r'Rb$^{78}$', r'Rb$^{80}$']
        for x in range(2):
            ax.plot(nu, b[x], 'x')
            ax.plot(x_sample, f(x_sample, *params[x]), label=label[x])
        ax.set_xlim(xmin=0)
        # ax.set_ylim(0.05*min(b.flatten()), 1.05*max(b.flatten()))
        ax.set_xlabel(r'$\nu$ / kHz')
        ax.set_ylabel('B / T')
        ax.legend(loc='best')
        fig.savefig(figPath)
        plt.close()

    def plot_exp(self, figPath):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.df["time"], self.df["voltage"])
        ax.axhline(self.df["uMean"], linestyle='--', color='r')
        ax.scatter(self.df["tPeaks"], 
                self.df["uPeaks"], 
                label='detected peak')
        ax.set_xlim(self.df["lowerTLim"], 
                self.df["upperTLim"])
        ax.set_xlabel('Zeit / s')
        ax.set_ylabel('Spannung / U')
        ax.set_title('T = ' + str(self.df["tDist"]*1e3) + ' ms')
        plt.legend(loc='best')
        fig.savefig(figPath)
        plt.close()

def statisch():
    stc = static_experiment()
    stc.calc_earth_b_static()
    nu, B, params, stds = stc.frequenz_B_fit()
    
    plttr = plotter()
    plttr.plot_nu_b(nu, B, params)

def sweep():
    plttr = plotter()
    csvPath = 'data/firstPeak/'
    TLim = np.array([10.,10.,1.5,2.5,2.5,1.5,1.5,2.5,
        2.5,1.5])*1e-3
    for U in range(1, 11):
        uStr = str(int(U))

        print('Processing U=: ', U)
        lam = larmor_sweep(csvPath + uStr + 'V.CSV', U,
                upperTLim=TLim[U-1])
        lam.save_info(csvPath)

        print('Plotting U=: ', U)
        plttr.load_data(csvPath + uStr +'.pkl')
        plttr.plot_exp('build/peaks_' + uStr + '.png')
    print('Done')

def main():
    statisch()
    #sweep()

if __name__ == '__main__':
    main()
