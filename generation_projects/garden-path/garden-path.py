# Authors: Alicia Parrish via Alex Warstadt's script :)
# Script for generating NPI sentences with explicit negation as licensors

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/garden-path/environment=garden-path.tsv"
#project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
project_root = "G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation"
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_neg_aux = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "1")])
all_nonneg_aux = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "0")])
all_connectors = ["as", "while", "when"]
all_intransitive_verbs = get_all("category", "S\\NP")
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # Connector D1  N1   V_mix   D2  N2   V_intrans
    # While     the lady dressed the baby cried.

    # build all lexical items
    #TODO: throw in modifiers
    Conx = choice(all_connectors)
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    V_mix = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    V_trans = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    V_intrans = choice(get_matched_by(N1, "arg_1", all_intransitive_verbs))
    conjugate(V_mix, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    V_final = choice(get_matched_by(N2, "arg_1", all_intransitive_verbs))
    conjugate(V_intrans, N2, allow_negated=True)

    # build classic garden paths
    sentence_1 = "%s %s %s %s %s %s %s ." % (Conx, D1[0], N1[0], V_mix[0], D2[0], N2[0], V_final[0])
    sentence_2 = "%s %s %s %s %s %s %s ." % (Conx, D1[0], N1[0], V_intrans[0], D2[0], N2[0], V_final[0])
    sentence_3 = "%s %s %s %s %s %s %s ." % (Conx, D1[0], N1[0], V_trans[0], D2[0], N2[0], V_final[0])

    # flip the order of clauses
    sentence_4 = "%s %s %s %s %s %s %s ." % (D2[0], N2[0], V_final[0], Conx, D1[0], N1[0], V_mix[0])
    sentence_5 = "%s %s %s %s %s %s %s ." % (D2[0], N2[0], V_final[0], Conx, D1[0], N1[0], V_intrans[0])
    sentence_6 = "%s %s %s %s %s %s %s ." % (D2[0], N2[0], V_final[0], Conx, D1[0], N1[0], V_trans[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    print(sentence_1)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have negation present
        output.write("%s\t%s\n" % ("experiment=garden-path_verb=mix_while-clause=1_garden=True", sentence_1))
        output.write("%s\t%s\n" % ("experiment=garden-path_verb=intrans_while-clause=1_garden=True", sentence_2))
        output.write("%s\t%s\n" % ("experiment=garden-path_verb=trans_while-clause=1_garden=False", sentence_3))
        output.write("%s\t%s\n" % ("experiment=garden-path_verb=mix_while-clause=2_garden=False", sentence_4))
        output.write("%s\t%s\n" % ("experiment=garden-path_verb=intrans_while-clause=2_garden=False", sentence_5))
        output.write("%s\t%s\n" % ("experiment=garden-path_verb=trans_while-clause=2_garden=False", sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

output.close()