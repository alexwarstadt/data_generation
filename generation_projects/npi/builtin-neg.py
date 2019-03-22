# Authors: Anna Alsop
# Script for generating NPI sentences with predicates with built-in negation as licensors

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=builtin-neg.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# generate sentences for "ever"

# set total number of paradigms to generate
number_to_generate = 100
sentences = set()

# gather word classes that will be accessed frequently
# PITFALL:
# ever doesn't occur with progressive
# Every boy who has ever eaten a potato is tall.
# *? Every boy who is ever eating a potato is tall.

# PITFALL #2:
# ever occurs after auxiliary "do"
# The boy rarely ever did say that the girl wears jeans.
# * The boy rarely did ever say that the girl wears jeans.

all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1")])
all_nonfreq_adverbs = get_all_conjunctive([("frequent", "0"), ("category_2", "Adv")])
all_freq_adverbs = get_all_conjunctive([("frequent", "1"), ("category_2", "Adv")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_embedding_verbs = get_all_conjunctive([("category_2","V_embedding"),("finite","1")])
all_nouns = get_all("category", "N")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))