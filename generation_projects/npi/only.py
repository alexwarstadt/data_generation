# Authors: Paloma Jeretic (based on Alex Warstadt's script for quantifiers)
# Script for generating NPI sentences with only as a licensor

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=only.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 20
sentences = set()

# gather word classes that will be accessed frequently
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
adverbs = ('always','sometimes','often', 'now')
sentence_final_adv = ('sometimes', 'now', 'today', 'this year', 'this week')
quantity_adv = ('a lot', 'little')



# TODO : fix "been"


# repeat for "ever"

# PITFALL:
# ever doesn't occur with progressive
# Every boy who has ever eaten a potato is tall.
# *? Every boy who is ever eating a potato is tall.

# PITFALL #2:
# ever occurs after auxiliary "do"
# The boy rarely ever did say that the girl wears jeans.
# * The boy rarely did ever say that the girl wears jeans.

sentences = set()
while len(sentences) < number_to_generate:

    # sentence templates
    # Only D1 N1 (Aux) n/ever V D2 N2.
    # DP1 (Aux) n/ever V1 only DP2.
    # DP1 (Aux) also n/ever V1 DP2.
    # DP1 (Aux) n/ever also V1 DP2.

    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    V = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    Aux = return_aux(V, N1, allow_negated=False)
    N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    Adv = choice(adverbs)

    # sentence templates
    # Only D1 N1 (Aux) adv/ever V D2 N2.
    # D1 N1 (Aux) adv/ever V1 only D2 N2.
    # D1 N1 (Aux) also adv/ever V D2 N2.
    # D1 N1 (Aux) adv/ever also V D2 N2.

    sentence_1 = "only %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_2 = "only %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])
    sentence_3 = "%s %s %s ever %s only %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_4 = "%s %s %s %s %s only %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])

    sentence_5 = "%s %s %s also ever %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_6 = "%s %s %s also %s %s %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])
    sentence_7 = "%s %s %s ever also %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_8 = "%s %s %s %s also %s %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])

    # remove doubled up spaces (this is because of empty determiner AND EMPTY AUXILIARY).
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)


    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have only
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=1_scope=0_npi-present=1", 0, sentence_3))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=1_scope=0_npi-present=0", 1, sentence_4))

        # sentences 5-8 don't have only
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=ever_licensor=0_scope=0_npi-present=0", 1, sentence_8))

    sentences.add(sentence_1)




sentences = set()
while len(sentences) < number_to_generate:

    # sentence templates
    # Only D1 N1 (Aux) V any/some N2.
    # Any/Some N1 (Aux) only V D2 N2.
    # D1 N1 (Aux) also V any/some N2.
    # Any/Some N1 (Aux) also V D2 N2.

    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    V = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    Aux = return_aux(V, N1, allow_negated=False)
    N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))

    # sentence templates
    # Only D1 N1 (Aux) V any/some N2.
    # Any/Some N1 (Aux) only V D2 N2.
    # D1 N1 (Aux) also V any/some N2.
    # Any/Some N1 (Aux) also V D2 N2.

    sentence_1 = "only %s %s %s %s any %s ." % (D1[0], N1[0], Aux[0], V[0], N2[0])
    sentence_2 = "only %s %s %s %s some %s ." % (D1[0], N1[0], Aux[0], V[0], N2[0])
    sentence_3 = "any %s %s only %s %s %s ." % (N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_4 = "some %s %s only %s %s %s ." % (N1[0], Aux[0], V[0], D2[0], N2[0])

    sentence_5 = "%s %s %s also %s any %s ." % (D1[0], N1[0], Aux[0], V[0], N2[0])
    sentence_6 = "%s %s %s also %s some %s ." % (D1[0], N1[0], Aux[0], V[0], N2[0])
    sentence_7 = "any %s %s also %s %s %s ." % (N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_8 = "some %s %s also %s %s %s ." % (N1[0], Aux[0], V[0], D2[0], N2[0])

    # remove doubled up spaces (this is because of empty determiner AND EMPTY AUXILIARY).
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)


    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have only
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=1_scope=0_npi-present=1", 0, sentence_3))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=1_scope=0_npi-present=0", 1, sentence_4))

        # sentences 5-8 don't have only
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t%s\n" % ("experiment=NPI_env=only_npi=any_licensor=0_scope=0_npi-present=0", 1, sentence_8))

    sentences.add(sentence_1)




output.close()