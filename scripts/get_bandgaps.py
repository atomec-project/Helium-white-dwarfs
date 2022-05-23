#!/usr/bin/env python3

"""Extract the band-gap from the dos.csv files."""

import os
import numpy as np

cwd = os.getcwd() + "/"
densities = np.linspace(1, 8, 20)
bgs = np.zeros((len(densities), 2))
bgs[:, 0] = densities
temp = 5e4

for i, rho in enumerate(densities):

    path = cwd + "../data/raw/rho_" + str(rho)
    os.chdir(path)

    Tpath = "T_" + str(temp)
    os.chdir(Tpath)

    dos = np.loadtxt("dos.csv", skiprows=1, unpack=True)
    x = dos[0]
    z = dos[2]

    try:
        zero_locs = x[np.where(z == 0)]
        bgs[i, 1] = zero_locs[2] - zero_locs[1]
    except IndexError:
        break

    os.chdir(cwd)

header = "Density (g cm^-3), BG (Ha)"
np.savetxt(cwd + "../data/processed/bandgap_" + str(temp) + ".txt", bgs, header=header)
