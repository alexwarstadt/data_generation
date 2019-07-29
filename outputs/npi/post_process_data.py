# Author: Alex Warstadt
# This script fixes some formatting and metadata issues in generated datasets

import os
import re

def add_paradigm_feature(dataset_path, output_path=None, paradigm_size=8):
    """
    :param dataset_path: 
    :param output_path: 
    :param paradigm_size: number of lines per paradigm
    :return: rewrites dataset but with paradigm count added to metadata column
    """
    data = [line for line in open(dataset_path)]
    if output_path is None:
        output_path = dataset_path
    out = open(output_path, "w")
    for i, line in enumerate(data):
        vals = line.split("\t")
        vals[0] = vals[0] + "-paradigm=" + str(i // paradigm_size)
        vals[-1] = reformat_sentence(vals[-1])
        out.write("\t".join(vals))
    out.close()


def reformat_sentence(sentence):
    """
    :param sentence: 
    :return: sentence with initial letter capitalized, and no space before final punctuation
    """
    sentence = sentence.capitalize()
    sentence = re.sub(" ([\.\?])\n$", r"\1\n", sentence)
    return sentence


# project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
# npi_dir = "outputs/npi/"
# for file in os.listdir(os.path.join(project_root, npi_dir)):
#     if ".tsv" in file:
#         if "environment=sentential_negation_monoclausal.tsv" not in file:
#             paradigm_size = 4 if "simplequestions" in file else 8
#             dataset_path = os.path.join(project_root, npi_dir, file)
#             output_path = os.path.join(project_root, npi_dir, file)
#             add_paradigm_feature(dataset_path, output_path, paradigm_size)
