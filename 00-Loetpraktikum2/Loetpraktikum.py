# coding: utf-8
import pandas as pd
from matplotlib import pyplot as plt

spannungsteiler = pd.read_csv(
    'data/spannungsteiler.csv', sep='\s+', header=[0, 1])

for header in spannungsteiler.columns.levels[0]:
    fig, ax = plt.subplots()
    spannungsteiler[header].plot.scatter(
        x='I/mA', y='U/V', label=header, ax=ax, figsize=(5.78, 3.57))
    fig.tight_layout(pad=0)
    fig.savefig('plots/spannungsteiler_{}.pdf'.format(header))

diode = pd.read_csv('data/diode.csv', sep='\s+', header=[0, 1, 2])

for header_0 in diode.columns.levels[0]:
    for header_1 in diode.columns.levels[1]:
        fig, ax = plt.subplots()
        for comb in [
                ('I/mA', 'U/mV'), ('I/uA', 'U/mV'), ('I/mA', 'U/V'), ('I/uA', 'U/V')]:
            try:
                diode[header_0][header_1].plot.scatter(
                    y=comb[0], x=comb[1],
                    label='{}, {}'.format(header_0, header_1),
                    ax=ax, figsize=(5.78, 3.57))
                fig.tight_layout(pad=0)
                fig.savefig('plots/diode_{}_{}.pdf'.format(header_0, header_1))
            except Exception:
                pass
