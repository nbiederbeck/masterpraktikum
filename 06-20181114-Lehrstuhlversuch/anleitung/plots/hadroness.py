import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['lines.linewidth'] = 2

rnd = np.random.rand(int(3e3))

def exp_dist(a, zahl):
    return - 1 / a * np.log(zahl)

def inv_exp(a, zahl):
    return 1 - exp_dist(a, zahl)

gamma = exp_dist(15, rnd[:1000])
hadron = np.append(exp_dist(20, rnd[:200]), 
        inv_exp(5, rnd[1001::]))

def cov_matrix(cut, signal, untergrund):
    tp = len(signal[signal<=cut])
    fp = len(untergrund[untergrund<=cut])
    tn = len(untergrund[untergrund>cut])
    fn = len(signal[signal>cut])
    return tp, fp, tn, fn

def sensitivity(cut, signal, untergrund):
    tp, _, _, fn = cov_matrix(cut, signal, untergrund)
    return tp / (tp + fn)

def precission(cut, signal, untergrund):
    tp, fp, _, _= cov_matrix(cut, signal, untergrund)
    return tp / (tp + fp)

def accuracy(cut, signal, untergrund):
    tp, fp, tn, fn= cov_matrix(cut, signal, untergrund)
    return (tp + tn) / (tp + fp + tn + fn)

param = {'cut':[], 'sen':[], 'pre': [], 'acc': []}

for cut in np.linspace(0.01,1,50):
    param['cut'].append(cut)
    param['sen'].append(sensitivity(cut, gamma, hadron))
    param['pre'].append(precission(cut, gamma, hadron))
    param['acc'].append(accuracy(cut, gamma, hadron))

fig = plt.figure(figsize=(4.5,3.5))
ax = fig.add_subplot(211)
ax.hist(
        [hadron, gamma], 
        bins=np.linspace(0,1,20), 
        stacked=True,
        histtype='step',
        label=['hadron', 'gamma'],
        linewidth=2,
        )

ax.axvline(x=0.10, c='r', alpha=0.7)
ax.axvline(x=0.10, c='r', alpha=0.05, linewidth=30)
ax.axvline(x=0.10, c='r', alpha=0.10, linewidth=15)

ax.set_ylabel('\# Events')
ax.legend(loc='best')
ax.tick_params(labelleft=False, labelbottom=False)

ax = fig.add_subplot(212)
ax.plot(param['cut'], param['sen'], label='sensitivity')
ax.plot(param['cut'], param['pre'], label='precision')
ax.plot(param['cut'], param['acc'], label='accuracy')

ax.axvline(x=0.10, c='r', alpha=0.7)
ax.axvline(x=0.10, c='r', alpha=0.05, linewidth=30)
ax.axvline(x=0.10, c='r', alpha=0.10, linewidth=15)

ax.set_xlabel('hadroness')
ax.legend(loc='best')

plt.tight_layout()
plt.savefig('../build/hadroness.pdf')
