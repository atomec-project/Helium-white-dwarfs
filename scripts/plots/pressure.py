#!/usr/bin/env python3

"""Make the pressure surface plot."""

import matplotlib.pyplot as plt
import numpy as np
from atoMEC import unitconv
import figstyle

figdims = figstyle.fig_initialize(latex=True, setsize=True, size="scipy3d")

rhos = np.linspace(1, 8, 20)
temps = np.linspace(1e4, 5e4, 20)

X, Y = np.meshgrid(temps, rhos)
Z = np.load("../../data/processed/Pressure.npy")
Z = np.log10(Z * unitconv.ha_to_gpa)

fig = plt.figure(figsize=figdims)
ax = plt.axes(projection="3d")
ax.grid(False)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="rainbow", edgecolor="none")
ax.view_init(18, -154)

ax.set_xlabel(r"$T$ (kK)", labelpad=-2)
ax.set_ylabel(r"$\rho_\textrm{m}\ (\textrm{g cm}^{-3})$", labelpad=-2)
ax.set_zlabel(r"$\log P\ (\textrm{GPa})$", labelpad=-1)
xticks = [1e4, 2e4, 3e4, 4e4, 5e4]
xlabs = [10, "", 30, "", 50]
ax.set_xticks(xticks)
ax.set_xticklabels(xlabs)
ax.xaxis.set_tick_params(pad=-2)
ax.zaxis.set_tick_params(pad=0)
ax.yaxis.set_tick_params(pad=-2)


# plt.show()
plt.savefig("../../figs/He_pressure.pdf", bbox_inches="tight")
