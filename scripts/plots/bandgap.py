#!/usr/bin/env python3

"""Make the band-gap and ionization figure."""

import matplotlib.pyplot as plt
import numpy as np
from atoMEC import unitconv
import figstyle
from scipy.stats import linregress

figdims = figstyle.fig_initialize(
    latex=True, setsize=True, size="reprint", fraction=0.8
)
# General figure set-up
fig, ax = plt.subplots(1, 1, figsize=(figdims))

bg_data = np.loadtxt(
    "../../data/processed/bandgap_50000.0.txt", unpack=True, skiprows=1
)

density = bg_data[0]
bg = 1 / unitconv.ev_to_ha * bg_data[1]
bg = bg[np.where(bg > 0)]
density = density[np.where(bg > 0)]

# grad, intcpt, R2, p, err, intcpt_err = linregress(density, bg)

linreg = linregress(density, bg)
grad = linreg.slope
intcpt = linreg.intercept
R2 = linreg.rvalue
print("R2 = ", R2 ** 2)

bg_close = -intcpt / grad
print("band-gap closure", bg_close)


def bestfit(x, m, c):

    return m * x + c


x = np.linspace(0.5, 6, 100)
Y_x = bestfit(x, grad, intcpt)

ax.plot(x, Y_x, ls="--", color="k")
ax.set_ylim(0, 18)


dens, Zbar = np.loadtxt(
    "../../data/processed/MIS_50000.0.txt",
    unpack=True,
    skiprows=1,
)

# convert to % ionization
Zbar *= 100 / 2

ax2 = ax.twinx()
ax2.set_ylim(0, 80)
ax2.set_ylabel(r"Ionization (\%)", labelpad=5, color="b")
ax.set_ylabel(r"Band-gap (eV)", color="r")
ax2.scatter(dens, Zbar, s=4, color="b", marker="s")
ax.scatter(density, bg, s=6, color="r", zorder=10)
ax.set_xlim(0.8, 7)
ax.set_xlabel(r"$\rho_\textrm{m}\ (\textrm{g cm}^{-3})$")

# plt.tight_layout()
# plt.show()

plt.savefig("../../figs/He_bg_Z.pdf", bbox_inches="tight")
