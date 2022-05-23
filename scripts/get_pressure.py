#!/usr/bin/env python3

"""Extract the pressure from the .pkl pressure files."""

import subprocess
import os
import numpy as np
import pickle as pkl

cwd = os.getcwd() + "/"
densities = np.linspace(1, 8, 20)
temps = np.linspace(1e4, 5e4, 20)

P = np.zeros((len(densities), len(temps)))

for i, rho in enumerate(densities):
    for j, temp in enumerate(temps):

        path = cwd + "../data/raw/rho_" + str(rho)
        os.chdir(path)

        Tpath = "T_" + str(temp)
        os.chdir(Tpath)

        with open("Pressure.pkl", "rb") as f:
            Pressure = pkl.load(f)

        P[i, j] = Pressure["P_st"] + Pressure["P_ion"]

    os.chdir(cwd)

np.save(cwd + "../data/processed/Pressure", P)
