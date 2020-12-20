import os

top = """#!/bin/bash
# Generic job script for all experiments.
#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH -t167:59:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

cd ~/data_generation
python -m generation_projects.structure_dependence.{script} --number_to_generate {number} --output_path {output} --one_template {template} --ambiguous {ambiguous}
"""

scripts = [
    ("reflexive", "sample_2_RCs", "True"),
    ("reflexive", "sample_nested_rc", "True"),
    ("reflexive", "sample_CP_verb_RC", "True"),
    ("reflexive", "sample_CP_noun", "True"),
    ("reflexive", "sample_CP_noun_RC", "True"),
    ("reflexive", "sample_nested_RC_2_RCs", "True"),
    ("reflexive", "sample_1_RC", "True"),
    ("reflexive", "sample_nested_CP_verb", "True"),
    ("reflexive", "sample_CP_under_RC", "True"),
    ("reflexive", "sample_nested_rc", "False"),
    ("reflexive", "sample_CP_verb_RC", "False"),
    ("reflexive", "sample_CP_noun_RC", "False"),
    ("reflexive", "sample_1_RC", "False"),
    ("reflexive", "sample_CP_under_RC", "False"),

    ("subject_aux_inversion", "sample_2_RCs", "False"),
    ("subject_aux_inversion", "sample_nested_rc", "True"),
    ("subject_aux_inversion", "sample_nested_rc", "False"),
    ("subject_aux_inversion", "sample_CP_verb_RC", "True"),
    ("subject_aux_inversion", "sample_CP_verb_RC", "False"),
    ("subject_aux_inversion", "sample_CP_noun", "False"),
    ("subject_aux_inversion", "sample_CP_noun_RC", "False"),
    ("subject_aux_inversion", "sample_nested_RC_2_RCs", "False"),
    ("subject_aux_inversion", "sample_1_RC", "True"),
    ("subject_aux_inversion", "sample_1_RC", "False"),
    ("subject_aux_inversion", "sample_nested_CP_verb", "True"),
    ("subject_aux_inversion", "sample_CP_under_RC", "True"),
    ("subject_aux_inversion", "sample_CP_under_RC", "False"),

    ("main_verb", "sample_2_RCs", "False"),
    ("main_verb", "sample_nested_rc", "True"),
    ("main_verb", "sample_nested_rc", "False"),
    ("main_verb", "sample_CP_verb_RC", "True"),
    ("main_verb", "sample_CP_verb_RC", "False"),
    ("main_verb", "sample_CP_noun", "False"),
    ("main_verb", "sample_CP_noun_RC", "False"),
    ("main_verb", "sample_nested_RC_2_RCs", "False"),
    ("main_verb", "sample_1_RC", "True"),
    ("main_verb", "sample_1_RC", "False"),
    ("main_verb", "sample_nested_CP_verb", "True"),
    ("main_verb", "sample_CP_under_RC", "True"),
    ("main_verb", "sample_CP_under_RC", "False"),
]


project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
for s in scripts:
    output_dir = os.path.join(project_root, "slurm", "struc_dep_language")
    os.makedirs(output_dir, exist_ok=True)
    output_file = open(os.path.join(output_dir, f"{s[0]}_{s[1]}_{s[2]}.sbatch"), "w")
    ambiguous = "ambiguous" if bool(s[2]) else "unambiguous"
    output_file.write(top.format(script=s[0],
                                 number=5000,
                                 output=f"outputs/structure_dependence_language/",
                                 template=s[1],
                                 ambiguous=s[2]))
