import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from glob import glob 

class larmor_sweep:
    def __init__(self, csvPath, spulenU, upperTLim=2.5e-3, lowerTLim=-1.5e-5):
        df = pd.read_csv(csvPath)
        data = pd.DataFrame(
                df.loc[18:].values[:,3:5],
                columns=['time', 'voltage'])
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
                distance=sum(self.mask)/20)
        self.tPeaks = self.data['time'][peaks]
        self.uPeaks = self.data['voltage'][peaks]
        return self.tPeaks, self.uPeaks

    def save_info(self, path, find_peaks_dict={}):
        self.find_peaks(*find_peaks_dict)
        df = pd.DataFrame({
            "lowerTLim": self.lowerTLim, 
            "upperTLim": self.upperTLim,
            "uMean": self.uMean,
            "tPeaks": self.tPeaks,
            "uPeaks": self.uPeaks,
            "time": self.data.time,
            "voltage": self.data.voltage,
            "spulenU": self.spulenU,
            })
        df.to_pickle(path+ str(int(self.spulenU))+ ".pkl")

class plotter:
    def __init__(self):
        self.df = None
        pass

    def load_data(self, path):
        self.df = pd.read_pickle(path)

    def plot_exp(self, figPath):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(1000*self.df.time, self.df.voltage)
        ax.scatter(1000*self.df.tPeaks, 
                self.df.uPeaks, 
                label='detected peak')
        ax.set_xlim(1000*self.df.lowerTLim[0], 
                1000*self.df.upperTLim[0])
        ax.set_xlabel('Zeit / ms')
        ax.set_ylabel('Spannung / U')
        plt.legend(loc='best')
        fig.savefig(figPath)
        plt.close()

def main():
    # csvPath = 'data/firstPeak/'
    # for U in np.linspace(1,10,10):
    #     print('Processing U=: ', U)
    #     lam = larmor_sweep(csvPath+str(int(U))+'V.CSV', U)
    #     lam.save_info('data/')
    # print('Done')

    plttr = plotter()
    plttr.load_data('data/7.pkl')
    plttr.plot_exp('test.pdf')

if __name__ == '__main__':
    main()
