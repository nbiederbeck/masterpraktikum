import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-6, 6, 101)
y = x**2

plt.plot(x, y)
plt.savefig('build/plot.pdf')
