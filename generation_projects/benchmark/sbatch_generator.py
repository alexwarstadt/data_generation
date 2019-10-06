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

scripts = ["adjunct_island",
            "anaphor_gender_agreement",
            "anaphor_number_agreement",
            "animate_subject_passive",
            "animate_subject_transitive",
            "causative",
            "complex_NP_island",
            "coordinate_structure_constraint_complex_left_branch",
            "coordinate_structure_constraint_object_extraction",
            "coordinate_structure_constraint_subject_extraction",
            "determiner_noun_agreement_1",
            "determiner_noun_agreement_2",
            "determiner_noun_agreement_irregular_1",
            "determiner_noun_agreement_irregular_2",
            "determiner_noun_agreement_with_adj_1",
            "determiner_noun_agreement_with_adj_2",
            "determiner_noun_agreement_with_adj_irregular_1",
            "determiner_noun_agreement_with_adj_irregular_2",
            "distractor_agreement_rc",
            "distractor_agreement_relational_noun",
            "drop_argument",
            "ellipsis_n_bar_1",
            "ellipsis_n_bar_2",
            "existential_there_object_raising",
            "existential_there_quantifiers_1",
            "existential_there_quantifiers_2",
            "existential_there_subject_raising",
            "expletive_it_object_raising",
            "inchoative",
            "intransitive",
            "irregular_past_participle_adjectives",
            "irregular_past_participle_verbs",
            "irregular_plural_subject_verb_agreement_1",
            "irregular_plural_subject_verb_agreement_2",
            "left_branch_island_echo_question",
            "left_branch_island_simple_question",
            "matrix_question_npi_licensor_present",
            "npi_present_1",
            "npi_present_2",
            "only_npi_licensor_present",
            "only_npi_scope",
            "passive_1",
            "passive_2",
            "principle_A_c_command",
            "principle_A_case_1",
            "principle_A_case_2",
            "principle_A_domain_1",
            "principle_A_domain_2",
            "principle_A_domain_3",
            "principle_A_reconstruction",
            "regular_plural_subject_verb_agreement_1",
            "regular_plural_subject_verb_agreement_2",
            "sentential_negation_npi_licensor_present",
            "sentential_negation_npi_scope",
            "sentential_subject",
            "superlative_quantifiers_1",
            "superlative_quantifiers_2",
            "tough_vs_raising_1",
            "tough_vs_raising_2",
            "transitive",
            "wh_island",
            "wh_questions_object_gap",
            "wh_questions_object_gap_long_distance",
            "wh_questions_subject_gap",
            "wh_questions_subject_gap_long_distance",
            "wh_vs_that_no_gap",
            "wh_vs_that_no_gap_long_distance",
            "wh_vs_that_with_gap",
            "wh_vs_that_with_gap_long_distance"
            ]

project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
for s in scripts:
    output_file = open(os.path.join(project_root, "slurm", "%s.sbatch" % s), "w")
    output_file.write(top % s)
    



