#!/bin/bash

# make ALL the input files

files=("full_densities" "integer_densities")
filetypes=("pressure" "SCF")

for file in "${files[@]}"; do
    for filetype in "${filetypes[@]}"; do
	python make_files.py $file $filetype
    done
done
