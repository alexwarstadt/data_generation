import os

top = """#!/bin/bash

# Generic job script for all experiments.

#SBATCH --cpus-per-task=7
#SBATCH --mem=16GB
#SBATCH -t24:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

#PRINCE PRINCE_GPU_COMPUTE_MODE=default

# Log what we're running and where.
#echo $SLURM_JOBID - `hostname` - $SPINN_FLAGS >> ~/spinn_machine_assignments.txt

# Make sure we have access to HPC-managed libraries.



# Run.


cd ~/data_generation
python -m generation_projects.IMPPRES.%s"""

scripts = ["all_n",
           "both",
           "change_of_state",
           "cleft_existence",
           "cleft_uniqueness",
           "only",
           "possessed_definites_existence",
           "possessed_definites_uniqueness",
           "question_presupposition",
           "scalar_implicatures"
           ]

project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
for s in scripts:
    output_file = open(os.path.join(project_root, "slurm/IMPPRES", "%s.sbatch" % s), "w")
    output_file.write(top % s)