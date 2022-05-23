#!/usr/bin/env python3

"""Make the 3d density-of-states figure."""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
from atoMEC import unitconv
import subprocess
import figstyle

from scipy.interpolate import interp1d

figdims = figstyle.fig_initialize(latex=True, setsize=True, size="scipy3d")

plasma = cm.get_cmap("rainbow")
# temps = np.array([10000.0, 30000.0, 50000.0])
densities = np.arange(6, 0, -1, dtype=float)
densrange = np.max(densities) - np.min(densities)
densnorms = (densities - np.min(densities)) / densrange

plt.figure(figsize=figdims)
ax = plt.subplot(projection="3d")
xmax = 50
xmin = -45

zeros1 = np.zeros((len(densities) - 1))
zeros2 = np.zeros((len(densities) - 1))

for i, dens in enumerate(densities):

    filename = "../../data/raw/dos_data/dos_50000.0_" + str(dens) + ".csv"

    logfile = "../../data/raw/dos_data/He_50000.0_" + str(dens) + ".log"

    cmd = "grep 'Chemical potential' " + logfile + " | awk '{ print $4 }' | tail -n1"
    mu = float(subprocess.check_output(cmd, shell=True))

    dos_data = np.loadtxt(filename, unpack=True, skiprows=1)
    x = (dos_data[0] - mu) / unitconv.ev_to_ha
    z1 = dos_data[2]
    z2 = dos_data[2] * dos_data[1]
    z1 = z1[np.where(x < xmax)]
    z2 = z2[np.where(x < xmax)]
    x = x[np.where(x < xmax)]
    y = np.zeros_like(x) + dens
    ax.add_collection3d(
        plt.fill_between(
            x,
            0,
            z1,
            alpha=0.25,
            color=plasma(densnorms[i]),
            zorder=10 - i,
        ),
        zs=dens,
        zdir="y",
    )

    ax.add_collection3d(
        plt.fill_between(
            x,
            0,
            z2,
            alpha=0.8,
            facecolor=plasma(densnorms[i]),
            zorder=10 - i,
            hatch="....",
        ),
        zs=dens,
        zdir="y",
    )
    # ax.plot(x, y, z1, ls="-", color="k", zorder=10 - i)

    if i > 0:
        zero_locs = x[np.where(z1 == 0)]
        zeros1[i - 1] = zero_locs[1]
        zeros2[i - 1] = zero_locs[2]

func_1 = interp1d(densities[1:], zeros1, fill_value="extrapolate")
func_2 = interp1d(densities[1:], zeros2, fill_value="extrapolate")

densgrid = np.linspace(densities[-1], densities[0], 1000)
bg_1 = func_1(densgrid)[np.where(func_1(densgrid) < func_2(densgrid))]
bg_2 = func_2(densgrid)[np.where(func_1(densgrid) < func_2(densgrid))]
densgrid = densgrid[np.where(func_1(densgrid) < func_2(densgrid))]

ax.plot(bg_1, densgrid, np.zeros_like(densgrid), color="k", ls="--")
ax.plot(bg_2, densgrid, np.zeros_like(densgrid), color="k", ls="--")
ax.set_xlim(xmin, xmax)
ax.set_zlim(0, 10)
ax.set_ylim(float(densities[0]), float(densities[-1]))
ax.xaxis.set_tick_params(pad=-5)
ax.zaxis.set_tick_params(pad=-5)
ax.yaxis.set_tick_params(pad=-5)
# ax.yaxis.set_tick_params(pad=0)
# ax.zaxis.set_tick_params(pad=0)
# ax.set_xlabel("Day")
ax.set_zlabel("DOS", labelpad=-8)
ax.set_zticks([])
ax.set_yticks(densities)
ax.set_ylabel(r"$\rho_\textrm{m}\ (\textrm{g cm}^{-3})$", labelpad=-7)
ax.set_xlabel("Energy (eV)", labelpad=-7)
ax.grid(False)


# plt.tight_layout()
# plt.show()
plt.savefig("../../figs/He_dos.pdf", bbox_inches="tight")
