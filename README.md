# Helium-white-dwarfs
This contains the scripts to reproduce the results in the final section of our SciPy Proceedings 2022 paper.

To make the input files, run `make_files.sh` from the `scripts/` folder. 
The raw data (input files and their direct output files) is not stored in this repository due to the size and number of files.
If you want to run the input scripts, it is recommended to do so on an HPC platform, as each script takes roughly "a few" minutes to run on 4 CPU cores  (and there are > 800 files in total).
N.B. if you want to generate the pressure data, you have to be on the "pressure" branch of [this fork of atoMEC](https://github.com/timcallow/atoMEC).

The processed data used to make the figures in the paper is found under `data/processed/`. An exception is the DOS data which is found under `data/raw/`.
The plotting scripts used to generate the figures from this data can be found in `scripts/plots`.
