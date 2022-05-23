#!/usr/bin/env python3

"""Extract the mean ionization state from the .log files."""

import subprocess
import os
import numpy as np

cwd = os.getcwd() + "/"
densities = np.linspace(1, 8, 20)
temp = 5e4

Zbar = np.zeros((len(densities), 2))
Zbar[:, 0] = densities

for i, rho in enumerate(densities):

    path = cwd + "../data/raw/rho_" + str(rho)
    os.chdir(path)

    Tpath = "T_" + str(temp)
    os.chdir(Tpath)

    cmd = "grep 'Mean ionization state' He.log | tail -n1 | awk '{ print $5 }'"
    Zbar[i, 1] = float(subprocess.check_output(cmd, shell=True))

    os.chdir(cwd)

header = "Density (g cm^-3), MIS"
np.savetxt(cwd + "../data/processed/MIS_" + str(temp) + ".txt", Zbar, header=header)
