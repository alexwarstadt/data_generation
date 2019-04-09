# Authors: Paloma Jeretic (based on Alex Warstadt's script for quantifiers)
# Script for generating NPI sentences with only as a licensor

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from utils.randomize import choice
import random
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=only.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 50
sentences = set()

# gather word classes that will be accessed frequently
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_intransitive_verbs = get_all("category", "S\\NP")
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
all_non_singular_animate_nouns = np.intersect1d(all_animate_nouns, all_non_singular_nouns)
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_non_progressive_intransitive_verbs = get_all("ing", "0", all_intransitive_verbs)

#adverbs = ('always','sometimes','often', 'now')

all_institutions = get_all_conjunctive([("category","N"),("institution","1"),("sg","1")])
all_plural_non_institutions = get_all_conjunctive([("category","N"),("institution","0"),("pl","1")])

#quantity_adv = ('happily', 'angrily', 'appropriately', 'inappropriately')

replace_ever = ["often", "really", "certainly", "clearly", "also"]

any_decoys = np.concatenate((get_all("expression", "the"), get_all_conjunctive([("expression", "that"), ("category_2", "D")]),
                         get_all("expression", "this"), get_all("expression", "these"), get_all("expression", "those")))

replace_adv = ["regularly", "on weekends", "on occasion", "for a while", "as well"]



####################################### ever
sentences = set()
while len(sentences) < number_to_generate:

    try:
        N1 = choice(all_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
        Adv = choice(replace_ever)

        # select transitive or intransitive V
        x = random.random()
     #   if x < 1/2:
            # transitive V
        V = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
        Aux = return_aux(V, N1, allow_negated=False)
        N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns),[N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
        #else:
            # intransitive V - gives empty string for N2 and D2 slots
            #V = choice(get_matched_by(N1, "arg_1", all_non_progressive_intransitive_verbs))
            #Aux = return_aux(V, N1, allow_negated=False)
            #N2 = " "
            #D2 = " "

        # sentence templates
        # Only D1 N1 (Aux) adv/ever V D2 N2.
        # D1 N1 (Aux) adv/ever V1 only D2 N2.
        # D1 N1 (Aux) also adv/ever V D2 N2.
        # D1 N1 (Aux) adv/ever also V D2 N2.
    except IndexError:
        continue


    sentence_1 = "only %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_2 = "only %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])
    sentence_3 = "%s %s %s ever %s only %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_4 = "%s %s %s %s %s only %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])

    sentence_5 = "even %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_6 = "even %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])
    sentence_7 = "%s %s %s ever %s even %s %s ." % (D1[0], N1[0], Aux[0], V[0], D2[0], N2[0])
    sentence_8 = "%s %s %s %s %s even %s %s ." % (D1[0], N1[0], Aux[0], Adv, V[0], D2[0], N2[0])


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


####################################### any

sentences = set()
while len(sentences) < number_to_generate:

    # sentence templates
    # Only D1 N1 (Aux) V any/some N2.
    # Any/Some N1 (Aux) only V D2 N2.
    # D1 N1 (Aux) also V any/some N2.
    # Any/Some N1 (Aux) also V D2 N2.
    try:
        N1 = choice(all_non_singular_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
        V = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        V = conjugate(V, N1, allow_negated=False)
        N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns),[N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
        any_decoy_N2 = choice(get_matched_by(N2, "arg_1", any_decoys))
        any_decoy_N1 = choice(get_matched_by(N1, "arg_1", any_decoys))
    except IndexError:
        continue

    # sentence templates
    # Only D1 N1 (Aux) V any/some N2.
    # Any/Some N1 (Aux) only V D2 N2.
    # D1 N1 (Aux) also V any/some N2.
    # Any/Some N1 (Aux) also V D2 N2.

    sentence_1 = "only %s %s %s any %s ." % (D1[0], N1[0], V[0], N2[0])
    sentence_2 = "only %s %s %s %s %s ." % (D1[0], N1[0], V[0], any_decoy_N2[0], N2[0])
    sentence_3 = "any %s only %s %s %s ." % (N1[0], V[0], D2[0], N2[0])
    sentence_4 = "%s %s only %s %s %s ." % (any_decoy_N1[0], N1[0],  V[0], D2[0], N2[0])

    sentence_5 = "even %s %s %s any %s ." % (D1[0], N1[0], V[0], N2[0])
    sentence_6 = "even %s %s %s %s %s ." % (D1[0], N1[0], V[0], any_decoy_N2[0], N2[0])
    sentence_7 = "any %s even %s %s %s ." % (N1[0], V[0], D2[0], N2[0])
    sentence_8 = "%s %s even %s %s %s ." % (any_decoy_N1[0], N1[0],  V[0], D2[0], N2[0])

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




###################################### at all

sentences = set()
while len(sentences) < number_to_generate:


    try:
        N1 = choice(all_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
        q_adv = choice(replace_adv)
        fin_adv = choice(all_institutions)

        # select transitive or intransitive V
        x = random.random()
        if x < 1/2:
            # transitive V
            V = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns),[N1])
            D3 = choice(get_matched_by(N2, "arg_1", all_common_dets))
        else:
            # intransitive V - gives empty string for N2 and D2 slots
            V = choice(get_matched_by(N1, "arg_1", all_intransitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            N2 = " "
            D2 = " "
    except IndexError:
        continue

    # sentence templates
    # Only D1 N1 (Aux) V D2 N2 at all/q at the [institution]
    # D1 N1 (Aux) V D2 N2 at all/q only at the [institution]
    # D1 N1 (Aux) also V D2 N2 at all/q at the [institution]
    # D1 N1 (Aux) V D2 N2 at all/q also at the [institution]

    sentence_1 = "only %s %s %s %s %s at all at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_2 = "only %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_3 = "%s %s %s %s %s at all only at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_4 = "%s %s %s %s %s only at the %s ." % (D1[0], N1[0], D2[0], N2[0], q_adv, fin_adv[0])

    sentence_5 = "even %s %s %s %s %s at all at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_6 = "even %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_7 = "%s %s %s %s %s at all even at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_8 = "%s %s %s %s %s even at the %s ." % (D1[0], N1[0], D2[0], N2[0], q_adv, fin_adv[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=1-scope=0-npi_present=0", 1, sentence_4))

        # sentences 5-8 don't have only
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=atall-crucial_item=_-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    sentences.add(sentence_1)


###################################### yet

sentences = set()
while len(sentences) < number_to_generate:


    try:
        N1 = choice(all_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
        q_adv = choice(replace_adv)
        fin_adv = choice(all_institutions)

        # select transitive or intransitive V
        x = random.random()
        if x < 1/2:
            # transitive V
            V = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns),[N1])
            D3 = choice(get_matched_by(N2, "arg_1", all_common_dets))
        else:
            # intransitive V - gives empty string for N2 and D2 slots
            V = choice(get_matched_by(N1, "arg_1", all_intransitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            N2 = " "
            D2 = " "

    except IndexError:
        continue

    # sentence templates
    # Only D1 N1 (Aux) V D2 N2 yet/q at the [institution]
    # D1 N1 (Aux) V D2 N2 yet/q only at the [institution]
    # D1 N1 (Aux) also V D2 N2 yet/q at the [institution]
    # D1 N1 (Aux) V D2 N2 yet/q also at the [institution]

    sentence_1 = "only %s %s %s %s %s yet at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_2 = "only %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_3 = "%s %s %s %s %s yet only at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_4 = "%s %s %s %s %s %s only at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])

    sentence_5 = "even %s %s %s %s %s yet at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_6 = "even %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_7 = "%s %s %s %s %s yet even at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_8 = "%s %s %s %s %s %s even at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])

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



###################################### in years
all_past_or_perfect_transitive_verbs = np.union1d(get_all("past", "1", all_transitive_verbs), get_all("en", "1", all_transitive_verbs))
all_past_or_perfect_intransitive_verbs = np.union1d(get_all("past", "1", all_intransitive_verbs), get_all("en", "1", all_intransitive_verbs))


sentences = set()
while len(sentences) < number_to_generate:


    try:
        N1 = choice(all_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
        q_adv = choice(replace_adv)
        fin_adv = choice(all_institutions)

        # select transitive or intransitive V
        x = random.random()
        if x < 1/2:
            # transitive V
            V = choice(get_matched_by(N1, "arg_1", all_past_or_perfect_transitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            #Aux = return_aux(V, N1, allow_negated=False)
            N2 = choice(get_matches_of(V, "arg_2", all_non_singular_nouns),[N1])
            D3 = choice(get_matched_by(N2, "arg_1", all_common_dets))
        else:
            # intransitive V - gives empty string for N2 and D2 slots
            V = choice(get_matched_by(N1, "arg_1", all_past_or_perfect_intransitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            #Aux = return_aux(V, N1, allow_negated=False)
            N2 = " "
            D2 = " "
    except IndexError:
        continue

    # sentence templates
    # Only D1 N1 (Aux) V D2 N2 in years/q at the [institution]
    # D1 N1 (Aux) V D2 N2 in years/q only at the [institution]
    # D1 N1 (Aux) also V D2 N2 in years/q at the [institution]
    # D1 N1 (Aux) V D2 N2 in years/q also at the [institution]

    sentence_1 = "only %s %s %s %s %s in years at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_2 = "only %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_3 = "%s %s %s %s %s in years only at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_4 = "%s %s %s %s %s %s only at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])

    sentence_5 = "even %s %s %s %s %s in years at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_6 = "even %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_7 = "%s %s %s %s %s in years even at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_8 = "%s %s %s %s %s %s even at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=1-scope=0-npi_present=0", 1, sentence_4))

        # sentences 5-8 don't have only
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=inyears-crucial_item=_-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    sentences.add(sentence_1)



###################################### either



sentences = set()
while len(sentences) < number_to_generate:


    try:
        N1 = choice(all_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
        q_adv = choice(replace_adv)
        fin_adv = choice(all_institutions)

        # select transitive or intransitive V
        x = random.random()
        if x < 1/2:
            # transitive V
            V = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            N2 = choice(get_matches_of(V, "arg_2", all_plural_non_institutions),[N1])
            D3 = choice(get_matched_by(N2, "arg_1", all_common_dets))
        else:
            # intransitive V - gives empty string for N2 and D2 slots
            V = choice(get_matched_by(N1, "arg_1", all_intransitive_verbs))
            V = conjugate(V, N1, allow_negated=False)
            N2 = " "
            D2 = " "
    except IndexError:
        continue
    # sentence templates
    # Only D1 N1 (Aux) V D2 N2 either/q at the [institution]
    # D1 N1 (Aux) V D2 N2 either/q only at the [institution]
    # D1 N1 (Aux) also V D2 N2 either/q at the [institution]
    # D1 N1 (Aux) V D2 N2 either/q also at the [institution]

    sentence_1 = "only %s %s %s %s %s either at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_2 = "only %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_3 = "%s %s %s %s %s either only at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_4 = "%s %s %s %s %s %s only at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])

    sentence_5 = "even %s %s %s %s %s either at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_6 = "even %s %s %s %s %s %s at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])
    sentence_7 = "%s %s %s %s %s either even at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], fin_adv[0])
    sentence_8 = "%s %s %s %s %s %s even at the %s ." % (D1[0], N1[0], V[0], D2[0], N2[0], q_adv, fin_adv[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=only-npi=yet-crucial_item=_-licensor=1-scope=1-npi_present=1", 0, sentence_1))
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