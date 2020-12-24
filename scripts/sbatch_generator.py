import os
import argparse

top = """#!/bin/bash
# Generic job script for all experiments.
#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH -t167:59:00
#SBATCH --mail-type=END
#SBATCH --mail-user=alexwarstadt@gmail.com

cd ~/data_generation
python -m generation_projects.structure_dependence.{script} --number_to_generate {number} --output_path {output} --one_template {template} --{ambiguous}
"""

scripts = [
    ("reflexive", "sample_2_RCs", "ambiguous"),
    ("reflexive", "sample_nested_rc", "ambiguous"),
    ("reflexive", "sample_CP_verb_RC", "ambiguous"),
    ("reflexive", "sample_CP_noun", "ambiguous"),
    ("reflexive", "sample_CP_noun_RC", "ambiguous"),
    ("reflexive", "sample_nested_RC_2_RCs", "ambiguous"),
    ("reflexive", "sample_1_RC", "ambiguous"),
    ("reflexive", "sample_nested_CP_verb", "ambiguous"),
    ("reflexive", "sample_CP_under_RC", "ambiguous"),
    ("reflexive", "sample_nested_rc", "unambiguous"),
    ("reflexive", "sample_CP_verb_RC", "unambiguous"),
    ("reflexive", "sample_CP_noun_RC", "unambiguous"),
    ("reflexive", "sample_1_RC", "unambiguous"),
    ("reflexive", "sample_CP_under_RC", "unambiguous"),

    ("subject_aux_inversion", "sample_2_RCs", "unambiguous"),
    ("subject_aux_inversion", "sample_nested_rc", "ambiguous"),
    ("subject_aux_inversion", "sample_nested_rc", "unambiguous"),
    ("subject_aux_inversion", "sample_CP_verb_RC", "ambiguous"),
    ("subject_aux_inversion", "sample_CP_verb_RC", "unambiguous"),
    ("subject_aux_inversion", "sample_CP_noun", "unambiguous"),
    ("subject_aux_inversion", "sample_CP_noun_RC", "unambiguous"),
    ("subject_aux_inversion", "sample_nested_RC_2_RCs", "unambiguous"),
    ("subject_aux_inversion", "sample_1_RC", "ambiguous"),
    ("subject_aux_inversion", "sample_1_RC", "unambiguous"),
    ("subject_aux_inversion", "sample_nested_CP_verb", "ambiguous"),
    ("subject_aux_inversion", "sample_CP_under_RC", "ambiguous"),
    ("subject_aux_inversion", "sample_CP_under_RC", "unambiguous"),

    ("main_verb", "sample_2_RCs", "unambiguous"),
    ("main_verb", "sample_nested_rc", "ambiguous"),
    ("main_verb", "sample_nested_rc", "unambiguous"),
    ("main_verb", "sample_CP_verb_RC", "ambiguous"),
    ("main_verb", "sample_CP_verb_RC", "unambiguous"),
    ("main_verb", "sample_CP_noun", "unambiguous"),
    ("main_verb", "sample_CP_noun_RC", "unambiguous"),
    ("main_verb", "sample_nested_RC_2_RCs", "unambiguous"),
    ("main_verb", "sample_1_RC", "ambiguous"),
    ("main_verb", "sample_1_RC", "unambiguous"),
    ("main_verb", "sample_nested_CP_verb", "ambiguous"),
    ("main_verb", "sample_CP_under_RC", "ambiguous"),
    ("main_verb", "sample_CP_under_RC", "unambiguous"),
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create sbatch scripts for generating datasets.")
    parser.add_argument("--phenomenon", "-p", type=str, default=None, help="What major phenomenon/experiment is the data from")
    parser.add_argument("--template", "-t", type=str, default=None, help="What specific template is the data from")
    parser.add_argument("--number", "-n", type=int, default=5000, help="How many pairs to generate for each template")
    project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
    args = parser.parse_args()
    if args.phenomenon is not None:
        scripts = [s for s in scripts if s[0] == args.phenomenon]
    if args.template is not None:
        scripts = [s for s in scripts if s[1] == args.template]
    for s in scripts:
        output_dir = os.path.join(project_root, "slurm", "struc_dep_language")
        os.makedirs(output_dir, exist_ok=True)
        output_file = open(os.path.join(output_dir, f"{s[0]}_{s[1]}_{s[2]}.sbatch"), "w")
        output_file.write(top.format(script=s[0],
                                     number=args.number,
                                     output=f"outputs/structure/",
                                     template=s[1],
                                     ambiguous=s[2]))
