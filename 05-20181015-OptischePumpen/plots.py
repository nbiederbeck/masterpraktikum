import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, constants
from scipy.spatial.distance import cdist
from glob import glob 
import pickle
from uncertainties import ufloat


class spulen:
    def __init__(self):
        self.spulen = {
                'sweep': {
                    'radius': 16.39*10-2, 'N': 11, 'R': 1.0
                    },
                "horizontal" : {
                    'radius': 15.79*10-2, 'N': 154, 'R': 0.5
                    },
                "vertical" : {
                    'radius': 11.735*10-2, 'N': 20, 'R': 0.5
                    }
                }

    def calc_b_helmoltz(self, spule, U):
        return constants.mu_0 * 8 * (U/self.spulen[spule]['R']) *   \
            self.spulen[spule]['N'] / ( np.sqrt(125) *          \
            self.spulen[spule]['radius'] )

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
    spu = spulen()
    s = spu.calc_b_helmoltz('sweep', 0.32)
    v = spu.calc_b_helmoltz('vertical', 0.12)
    print('B-Feld: ', s, v)
    pass

def sweep():
    csvPath = 'data/firstPeak/'
    plttr = plotter()
    TLim = np.array([10.,10.,1.5,2.5,2.5,1.5,1.5,2.5,2.5,1.5])*1e-3
    for U in range(1, 11):
        uStr = str(int(U))

        print('Processing U=: ', U)
        lam = larmor_sweep(csvPath + uStr + 'V.CSV', U, upperTLim=TLim[U-1])
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
