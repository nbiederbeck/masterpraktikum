import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['lines.linewidth'] = 2

rnd = np.random.rand(int(1e4))
exp_rnd= -1/20*np.log(rnd)
lin_rnd = 2*(1-np.sqrt(rnd))

fig = plt.figure(figsize=(3.,2.))
ax = fig.add_subplot(111)

ax.axvline(x=0.1,  alpha=0.7, c='r',
        linestyle='-', label='theta2-cut', zorder=1)
ax.axvline(x=0.10, c='r', alpha=0.05, linewidth=20)
ax.axvline(x=0.10, c='r', alpha=0.10, linewidth=10)

ax.hist([lin_rnd, exp_rnd], bins=np.linspace(0,1,15),
        stacked=True, histtype='step',
        label=['Off-Region', 'On-Region'],
        linewidth=2, zorder=10)

ax.set_xlabel('theta2')
ax.set_ylabel('\# Events')
plt.legend(loc='best')
ax.tick_params(
        labelleft=False,
        labelbottom=False
        )

plt.tight_layout()
plt.savefig('../build/theta2.pdf')
plt.close()
