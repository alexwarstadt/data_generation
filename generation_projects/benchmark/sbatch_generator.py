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
python -m generation_projects.benchmark.%s"""

scripts = ["only_npi_licensor_present",
             "only_npy_scope",
             "principle_A_c_command",
             "principle_A_case",
             "principle_A_domain",
             "principle_A_domain2",
             "principle_A_domain3",
             "regular_plural_subj_v_agreement_1",
             "regular_plural_subj_v_agreement_2",
             "sentential_negation_npi_licensor_present"
             ]

project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
for s in scripts:
    output_file = open(os.path.join(project_root, "slurm", "%s.sbatch" % s), "w")
    output_file.write(top % s)