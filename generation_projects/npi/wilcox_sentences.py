# Authors: Anna Alsop (based on Alex Warstadt's vocab_table.py)
# Script for generating NPI sentences from Wilcox et al. paradigm

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import random
from utils.wilcox_data_type import data_type
import numpy as np

# read in Wilcox paradigm
paradigm_path = os.path.join("/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2]),
                             "wilcox_npi_paradigm.csv")
paradigm = np.genfromtxt(paradigm_path, delimiter=",", names=True, dtype=data_type, encoding="latin1")

# initialize output file
rel_output_path = "outputs/npi/environment=wilcox_sentences.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# generate sentences
for item in paradigm:
    # *The journalist that the critic likes has ever received any praise for his writing .
    sentence_1 = "%s %s %s %s %s %s %s %s %s %s" % (item["NonNegativeLicensor"], item["Subject"], item["RC"],
                                                      item["Aux"], item["Ever"], item["Verb"], item["Any"],
                                                      item["Noun"], item["Continuation"], item["Conclusion"])
    # No journalist that the critic likes has ever received any praise for his writing .
    sentence_2 = "%s %s %s %s %s %s %s %s %s %s" % (item["NegativeLicensor"], item["Subject"], item["RC"],
                                                      item["Aux"], item["Ever"], item["Verb"], item["Any"],
                                                      item["Noun"], item["Continuation"], item["Conclusion"])
    # *The journalist that no critic likes has ever received any praise for his writing .
    sentence_3 = "%s %s %s %s %s %s %s %s %s %s" % (item["NonNegativeLicensor"], item["Subject"], item["DistractorRC"],
                                                      item["Aux"], item["Ever"], item["Verb"], item["Any"],
                                                      item["Noun"], item["Continuation"], item["Conclusion"])
    # No journalist that no critic likes has ever received any praise for his writing .
    sentence_4 = "%s %s %s %s %s %s %s %s %s %s" % (item["NegativeLicensor"], item["Subject"], item["DistractorRC"],
                                                      item["Aux"], item["Ever"], item["Verb"], item["Any"],
                                                      item["Noun"], item["Continuation"], item["Conclusion"])
    output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=negation-npi=ever-distractor=0-licensor=0-scope=1-npi_present=1", 0, sentence_1))
    output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=negation-npi=ever-distractor=0-licensor=1-scope=1-npi_present=1", 1, sentence_2))
    output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=negation-npi=ever-distractor=1-licensor=0-scope=1-npi_present=1", 0, sentence_3))
    output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=negation-npi=ever-distractor=1-licensor=1-scope=1-npi_present=1", 1, sentence_4))

output.close()