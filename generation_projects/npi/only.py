# Authors: Paloma Jeretic (based on Alex Warstadt's script for quantifiers)
# Script for generating NPI sentences with only as a licensor

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import random
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=only.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 100
sentences = set()

# gather word classes that will be accessed frequently
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_intransitive_verbs = get_all("category", "S\\NP")
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_non_progressive_intransitive_verbs = get_all("ing", "0", all_intransitive_verbs)
adverbs = ('always','sometimes','often', 'now')
sentence_final_adv = ('sometimes', 'today', 'this year', 'this week')
quantity_adv = ('happily', 'angrily', 'appropriately', 'inappropriately')





# ever
sentences = set()
while len(sentences) < number_to_generate:


    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adv = choice(adverbs)

    # select transitive or intransitive V
    x = random.random()
    if x < 1/2:
        # transitive V
        V = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
        Aux = return_aux(V, N1, allow_negated=False)
        N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns))
        D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    else:
        # intransitive V - gives empty string for N2 and D2 slots
        V = choice(get_matched_by(N1, "arg_1", all_non_progressive_intransitive_verbs))
        Aux = return_aux(V, N1, allow_negated=False)
        N2 = " "
        D2 = " "

    # sentence templates
    # D1 N1 (Aux) only adv/ever V D2 N2.
    # D1 N1 (Aux) adv/ever only V1 D2 N2.
    # D1 N1 (Aux) also adv/ever V D2 N2.
    # D1 N1 (Aux) adv/ever also V D2 N2.

    sentence_1 = "%s %s %s only ever %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_2 = "%s %s %s %s only %s %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])
    sentence_3 = "%s %s %s ever only %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_4 = "%s %s %s %s only %s %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=1-scope=0-npi_present=0", 1, sentence_4))

        # sentences 5-8 don't have only
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=ever-crucial_item=_-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    sentences.add(sentence_1)

# # ever in embedded clause
# while len(sentences) < number_to_generate:
#     # sentence template
#     #       D1    N1  Aux1  Adv    ever/also V1   that D2    N2   (Aux) V2   D3    N3
#     # Only The/a boy (has) rarely ever/also said that the/a girl (has) sung the/a song
#
#     N1 = choice(all_animate_nouns)
#     D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
#     Adv_freq = choice(all_freq_adverbs)
#     Adv_nonfreq = choice(all_nonfreq_adverbs)
#     V1 = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
#     Aux1 = return_aux(V1, N1, allow_negated=False)
#     N2 = choice(all_animate_nouns)
#     D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
#
#     # select transitive or intransitive V2
#     x = random.random()
#     if x < 1/2:
#         # transitive V2
#         V2 = choice(get_matched_by(N2, "arg_1", all_non_progressive_transitive_verbs))
#         Aux2 = return_aux(V2, N2, allow_negated=False)
#         N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
#         D3 = choice(get_matched_by(N3, "arg_1", all_common_dets))
#     else:
#         # intransitive V2 - gives empty string for N3 and D3 slots
#         V2 = choice(get_matched_by(N2, "arg_1", all_non_progressive_intransitive_verbs))
#         Aux2 = return_aux(V2, N2, allow_negated=False)
#         N3 = " "
#         D3 = " "
#
#     # check for do/does/did for both aux verbs, make the aux directly adjacent to verb.
#     if Aux1[0] in ["do", "does", "did"]:
#         Aux1_final = ""
#         V1_final = Aux1[0] + " " + V1[0]
#     else:
#         Aux1_final = Aux1[0]
#         V1_final = V1[0]
#
#     if Aux2[0] in ["do", "does", "did"]:
#         Aux2_final = ""
#         V2_final = Aux2[0] + " " + V2[0]
#     else:
#         Aux2_final = Aux2[0]
#         V2_final = V2[0]
#
#     # build sentences with frequent adverb
#     sentence_1 = "%s %s %s %s ever %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#     sentence_2 = "%s %s %s %s also %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0],  V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#     sentence_3 = "%s %s %s %s %s that %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0],  V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#     sentence_4 = "%s %s %s %s %s that %s %s %s also %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0],  V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#
#     # build sentences with nonfrequent adverb
#     sentence_5 = "%s %s %s %s ever %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#     sentence_6 = "%s %s %s %s also %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#     sentence_7 = "%s %s %s %s %s that %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#     sentence_8 = "%s %s %s %s %s that %s %s %s also %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
#
#     # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
#     # but the code outputs a determiner with an empty string. might want to change this)
#     sentence_1 = remove_extra_whitespace(sentence_1)
#     sentence_2 = remove_extra_whitespace(sentence_2)
#     sentence_3 = remove_extra_whitespace(sentence_3)
#     sentence_4 = remove_extra_whitespace(sentence_4)
#     sentence_5 = remove_extra_whitespace(sentence_5)
#     sentence_6 = remove_extra_whitespace(sentence_6)
#     sentence_7 = remove_extra_whitespace(sentence_7)
#     sentence_8 = remove_extra_whitespace(sentence_8)
#
#     # write sentences to output
#     if sentence_1 not in sentences:
#         # sentences 1-4 have frequent adverb
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=0-scope=1-npi_present=1" % Adv_freq[0], 0, sentence_1))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=0-scope=1-npi_present=0" % Adv_freq[0], 1, sentence_2))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=0-scope=0-npi_present=1" % Adv_freq[0], 0, sentence_3))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=0-scope=0-npi_present=0" % Adv_freq[0], 1, sentence_4))
#
#         # sentences 5-8 have nonfrequent adverb
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=1-scope=1-npi_present=1" % Adv_nonfreq[0], 1, sentence_5))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=1-scope=1-npi_present=0" % Adv_nonfreq[0], 1, sentence_6))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=1-scope=0-npi_present=1" % Adv_nonfreq[0], 0, sentence_7))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=only-crucial_item=%s-licensor=1-scope=0-npi_present=0" % Adv_nonfreq[0], 1, sentence_8))
#
#     # keep track of which sentences have already been generated
#     sentences.add(sentence_1)

#any
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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=1-scope=0-npi_present=0", 1, sentence_4))

        # sentences 5-8 don't have only
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=any-crucial_item=_-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    sentences.add(sentence_1)




# at all
sentences = set()
while len(sentences) < number_to_generate:



    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    q_adv = choice(quantity_adv)
    fin_adv = choice(sentence_final_adv)

    # select transitive or intransitive V
    x = random.random()
    if x < 1/2:
        # transitive V
        V = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
        Aux = return_aux(V, N1, allow_negated=False)
        N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns))
        D3 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    else:
        # intransitive V - gives empty string for N2 and D2 slots
        V = choice(get_matched_by(N1, "arg_1", all_non_progressive_intransitive_verbs))
        Aux = return_aux(V, N1, allow_negated=False)
        N2 = " "
        D2 = " "

    # sentence templates
    # Only D1 N1 (Aux) V D2 N2 at all/q fin_adv
    # D1 N1 (Aux) V D2 N2 at all/q only fin_adv
    # D1 N1 (Aux) also V D2 N2 at all/q fin_adv
    # D1 N1 (Aux) V D2 N2 at all/q also fin_adv

    sentence_1 = "only %s %s %s %s %s %s at all %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], fin_adv)
    sentence_2 = "only %s %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], q_adv, fin_adv)
    sentence_3 = "%s %s %s %s %s %s at all only %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], fin_adv)
    sentence_4 = "%s %s %s %s %s %s %s only %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], q_adv, fin_adv)

    sentence_5 = "%s %s %s also %s %s %s at all %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], fin_adv)
    sentence_6 = "%s %s %s also %s %s %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], q_adv, fin_adv)
    sentence_7 = "%s %s %s %s %s %s at all also %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], fin_adv)
    sentence_8 = "%s %s %s %s %s %s %s also %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0], q_adv, fin_adv)

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=1-scope=0-npi_present=0", 1, sentence_4))

        # sentences 5-8 don't have only
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    sentences.add(sentence_1)





output.close()