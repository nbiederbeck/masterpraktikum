import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

df = pd.read_csv('data/TEK0007.CSV')
data = pd.DataFrame(df.loc[18:].values[:,3:5],
        columns=['time', 'voltage'])

lowerTLim = -1e-5
upperTLim =  2.5e-3
mask = (data.time > lowerTLim) & (data.time < upperTLim)
data = data[mask].reset_index()

uMean = np.mean(data['voltage'])
peaks, _ = signal.find_peaks(
        data['voltage'], 
        height=uMean, 
        distance=sum(mask)/20)

tPeaks = data['time'][peaks]
uPeaks = data['voltage'][peaks]

print('Peaks: ', tPeaks)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(data['time'], data['voltage'])
ax.scatter(tPeaks, uPeaks)
ax.set_xlim(lowerTLim, upperTLim)
ax.set_xlabel('Zeit / t')
ax.set_ylabel('Spannung / U')
fig.savefig('text.png')
