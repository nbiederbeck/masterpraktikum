import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class larmor_sweep:
    def __init__(self, csvPath, upperTLim=2.5e-3, lowerTLim=-1.5e-5):
        df = pd.read_csv(csvPath)
        data = pd.DataFrame(
                df.loc[18:].values[:,3:5],
                columns=['time', 'voltage'])
        self.mask = (data.time > lowerTLim) & \
                (data.time < upperTLim)
        self.data = data[self.mask].reset_index()
        self.lowerTLim = lowerTLim
        self.upperTLim = upperTLim

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
            "voltage": self.data.voltage
            })
        df.to_pickle(path)

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
    # lam = larmor_sweep('data/TEK0007.CSV')
    # lam.save_info('test')

    plttr = plotter()
    plttr.load_data('test')
    plttr.plot_exp('test.pdf')

if __name__ == '__main__':
    main()
