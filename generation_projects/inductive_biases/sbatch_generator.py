import os

top = """#!/bin/bash

# Generic job script for all experiments.

#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH -t167:59:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

# Log what we're running and where.
#echo $SLURM_JOBID - `hostname` - $SPINN_FLAGS >> ~/spinn_machine_assignments.txt

# Make sure we have access to HPC-managed libraries.



# Run.


cd ~/data_generation
python -m generation_projects.inductive_biases.%s
"""

scripts = [
            "absolute_token_position_control",
            "antonym_absolute_token_position",
            "antonym_control",
            "antonym_length",
            "antonym_lexical_content_the",
            "antonym_relative_token_position",
            "antonym_title_case",
            "control_raising_absolute_token_position",
            "control_raising_control",
            "control_raising_length",
            "control_raising_lexical_content_the",
            "control_raising_relative_token_position",
            "control_raising_title_case",
            "irregular_form_control",
            "length_control",
            "lexical_content_the_control",
            "relative_position_control",
            "same_clause1_a_control",
            "same_clause1_b_control",
            "same_clause1_control",
            "same_clause2_a_control",
            "same_clause2_b_control",
            "same_clause2_control",
            "same_clause3_a_control",
            "same_clause3_b_control",
            "same_clause3_control",
            "same_clause4_a_control",
            "same_clause4_b_control",
            "same_clause4_control",
            "syntactic_category_absolute_position",
            "syntactic_category_control",
            "syntactic_category_length",
            "syntactic_category_lexical_content_the",
            "syntactic_category_relative_position",
            "syntactic_category_title_case",
            "title_case_control",
           ]

project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
for s in scripts:
    output_file = open(os.path.join(project_root, "slurm", "inductive_biases", "%s.sbatch" % s), "w")
    output_file.write(top % s)





