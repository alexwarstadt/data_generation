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
            "irregular_form_absolute_token_position",
            "irregular_form_control",
            "irregular_form_length",
            "irregular_form_lexical_content_the",
            "irregular_form_relative_token_position",
            "irregular_form_titlecase",
            "length_control",
            "lexical_content_the_control",
            "main_verb_absolute_token_position",
            "main_verb_control",
            "main_verb_length",
            "main_verb_lexical_content_the",
            "main_verb_relative_token_position",
            "main_verb_title_case",
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
            "main_verb_absolute_token_position_1",
            "main_verb_absolute_token_position_2",
            "main_verb_absolute_token_position_3",
            "main_verb_absolute_token_position_4",
            "main_verb_absolute_token_position_5",
            "main_verb_control_1",
            "main_verb_control_2",
            "main_verb_control_3",
            "main_verb_control_4",
            "main_verb_control_5",
            "main_verb_length_1",
            "main_verb_length_2",
            "main_verb_length_3",
            "main_verb_length_4",
            "main_verb_length_5",
            "main_verb_lexical_content_the_1",
            "main_verb_lexical_content_the_2",
            "main_verb_lexical_content_the_3",
            "main_verb_lexical_content_the_4",
            "main_verb_lexical_content_the_5",
            "main_verb_relative_token_position_1",
            "main_verb_relative_token_position_2",
            "main_verb_relative_token_position_3",
            "main_verb_relative_token_position_4",
            "main_verb_relative_token_position_5",
            "main_verb_title_case_1",
            "main_verb_title_case_2",
            "main_verb_title_case_3",
            "main_verb_title_case_4",
            "main_verb_title_case_5",

           ]

project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
for s in scripts:
    output_file = open(os.path.join(project_root, "slurm", "inductive_biases", "%s.sbatch" % s), "w")
    output_file.write(top % s)





