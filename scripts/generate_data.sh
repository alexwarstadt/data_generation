#!/bin/bash
export PROJECT_ROOT=/Users/alexwarstadt/Workspace/data_generation/
python sbatch_generator.py
cd ../slurm/struc_dep_language
#for x in *; do sbatch $x; done
for x in *; do . $x; done
