#!/usr/bin/env python3

"""Make the input files for the temperature / density spectrum."""

import os
import fileinput
import time
import sys
import numpy as np

cwd = os.getcwd() + "/"

files = sys.argv[1]
if files == "integer_densities":
    densities = np.arange(1, 11, 1)
    temps = np.array([5e4])
elif files == "full_densities":
    densities = np.linspace(1, 8, 20)
    temps = np.linspace(1e4, 5e4, 20)

filetype = sys.argv[2]
if filetype == "pressure":
    extension = "_pressure"
elif filetype == "SCF":
    extension = ""

for rho in densities:
    for temp in temps:

        path = cwd + "../data/raw/rho_" + str(rho)

        if os.path.exists(path):
            os.chdir(path)
        else:
            os.makedirs(path)
            os.chdir(path)

        Tpath = "T_" + str(temp)

        if not os.path.exists(Tpath):
            os.makedirs(Tpath)
        os.chdir(Tpath)

        # copy the template
        os.popen("cp ../../../He" + extension + "_template.py He" + extension + ".py")
        new_cwd = os.getcwd() + "/"

        time.sleep(0.1)

        for line in fileinput.input(new_cwd + "He" + extension + ".py", inplace=True):
            line = line.replace("density = 1", "density = " + str(rho))
            line = line.replace("temperature = 1", "temperature = " + str(temp))
            sys.stdout.write(line)

    os.chdir(cwd)
