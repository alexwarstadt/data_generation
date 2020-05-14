import os

top = """#!/bin/bash

# Generic job script for all experiments.

#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH -t200:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

# Log what we're running and where.
#echo $SLURM_JOBID - `hostname` - $SPINN_FLAGS >> ~/spinn_machine_assignments.txt

# Make sure we have access to HPC-managed libraries.



# Run.


cd ~/data_generation
python -m generation_projects.inductive_biases.%s"""

scripts = [
            "absolute_token_position_control",
            "antonym_absolute_token_position",
            "antonym_control",
            "antonym_length",
            "antonym_lexical_content_the",
            "antonym_relative_position",
            "antonym_title_case",
            "c_command_same_control",
            "control_raising_absolute_token_position",
            "control_raising_control",
            "control_raising_length",
            "control_raising_lexical_content_the",
            "control_raising_relative_token_position",
            "control_raising_title_case",
            "length_control",
            "lexical_content_the_control",
            "old_person_length",
            "person_absolute_token_position",
            "person_control",
            "person_length",
            "person_lexical_content_apparition",
            "person_lexical_content_doctor",
            "person_lexical_content_repeated",
            "person_lexical_content_the",
            "person_relative_position",
            "relative_position_control",
            "same_verb_form",
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




