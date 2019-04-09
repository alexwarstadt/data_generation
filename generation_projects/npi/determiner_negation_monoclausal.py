# Authors: Alicia Parrish via Alex Warstadt's script :)
# Script for generating NPI sentences with explicit negation as licensors

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from utils.randomize import choice
import random
import numpy as np

# initialize output file
# project_root = "G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation"
# output = open(os.path.join(project_root, rel_output_path), "w")
rel_output_path = "outputs/npi/environment=determiner_negation_monoclausal.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_def_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "these"), np.append(get_all("expression", "those"), np.append(get_all("expression", "this"), get_all("expression", "that")))))
npi_any = np.append(get_all("expression", "any"), get_all("expression", "any"))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_neg_det = np.append(get_all("expression", "none of the"), get_all("expression", "no"))
all_neg_aux = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "1")])
all_nonneg_aux = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "0")])
all_intransitive_verbs = get_all("category", "S\\NP")
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_embedding_verbs = get_all("category_2", "V_embedding")
all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_institution_nouns = np.append(get_all_conjunctive([("institution","1"), ("pl","1")]),get_all_conjunctive([("institution","1"), ("mass","1")]))
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))
all_non_singular_nouns_freq = np.append(get_all_conjunctive([("category", "N"), ("frequent", "1"), ("pl","1")]),get_all_conjunctive([("category", "N"), ("frequent", "1"), ("mass","1")]))
all_non_singular_animate_nouns = np.append(get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1"), ("pl","1")]),get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1"), ("mass","1")]))
sentence_final_npi = ["yet", "at all", "in years", "either"]
sentence_final_nonnpi = ["regularly", "on weekends", "on occasion", "for a while", "as well"]
replace_ever = ["often", "also", "really", "certainly", "clearly"]
all_past_or_perfect_transitive_verbs = np.union1d(get_all("past", "1", all_transitive_verbs), get_all("en", "1", all_transitive_verbs))
all_past_or_perfect_intransitive_verbs = np.union1d(get_all("past", "1", all_intransitive_verbs), get_all("en", "1", all_intransitive_verbs))
all_past_or_perfect_embedding_verbs = np.union1d(get_all("past", "1", all_embedding_verbs), get_all("en", "1", all_embedding_verbs))

# -------------------------
# "ever" as NPI

sentences = set()

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # Neg_word  N1          aux  ever/often  V1      no/some  N2
    # No        teachers    will ever        fail    some     students .

    try:
        # build all lexical items
        #TODO: throw in modifiers
        N1 = choice(all_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
        Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
        V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        Aux1 = require_aux(V1, N1, allow_negated=False)
        #N2 = choice(all_animate_nouns)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns_freq))
        D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
        Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))
        repl_ever = choice(replace_ever)
    except IndexError:
        #print(N1[0], N2[0], V1[0])
        continue
    except TypeError:
        print("found type error again")
        continue

    if Aux1[0] in ["do", "does", "did"]:
        Aux1_final = ""
        V1_final = Aux1[0] + " " + V1[0]
    else:
        Aux1_final = Aux1[0]
        V1_final = V1[0]

    # build sentences with licensor present
    sentence_1 = "%s %s %s ever %s %s %s ." % (Neg_word1[0], N1[0], Aux1_final, V1_final, D2[0], N2[0])
    sentence_2 = "%s %s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1_final, repl_ever, V1_final, D2[0], N2[0])
    sentence_3 = "%s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Neg_word1[0], N2[0])
    sentence_4 = "%s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, repl_ever, V1_final, Neg_word1[0], N2[0])

    # build sentences with no licensor present
    sentence_5 = "some %s %s ever %s %s %s ." % (N1[0], Aux1_final, V1_final, D2[0], N2[0])
    sentence_6 = "some %s %s %s %s %s %s ." % (N1[0], Aux1_final, repl_ever, V1_final, D2[0], N2[0])
    sentence_7 = "%s %s %s ever %s some %s ." % (D1[0], N1[0], Aux1_final, V1_final, N2[0])
    sentence_8 = "%s %s %s %s %s some %s ." % (D1[0], N1[0], Aux1_final, repl_ever, V1_final, N2[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
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
        # sentences 1-4 have negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=%s-licensor=1-scope=1-npi_present=1" % Neg_word1[0], 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=%s-licensor=1-scope=1-npi_present=0" % Neg_word1[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=%s-licensor=1-scope=0-npi_present=1" % Neg_word1[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=%s-licensor=1-scope=0-npi_present=0" % Neg_word1[0], 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=some-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=some-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=some-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=ever-crucial_item=some-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# -------------------------
# sentence final npi

for Final_npi in sentence_final_npi:

    sentences = set()

    # sample sentences until desired number
    while len(sentences) < number_to_generate:
        # sentence template
        # Neg_word  N1          aux  V1      no/some  N2        at all
        # No        teachers    will fail    some     students  at all.

        try:
            # build all lexical items
            #TODO: throw in modifiers
            N1 = choice(all_animate_nouns)
            D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
            Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
            V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            Aux1 = return_aux(V1, N1, allow_negated=False)
            N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns_freq))
            D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
            Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))
            Final_nonnpi = choice(sentence_final_nonnpi)
            N3 = choice(all_institution_nouns)
            Neg_word3 = choice(get_matched_by(N3, "arg_1", all_neg_det))

            if Final_npi == 'in years':
                V1 = choice(get_matched_by(N1, "arg_1", all_past_or_perfect_embedding_verbs))
                Aux1 = return_aux(V1, N1, allow_negated=False)

        except IndexError:
            #print(N1[0], N2[0], V1[0])
            continue
        except TypeError:
            print("found type error again")
            continue

        # build sentences with licensor present
        sentence_1 = "%s %s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_npi)
        sentence_2 = "%s %s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_nonnpi)
        sentence_3 = "%s %s %s %s %s %s %s at %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_npi, Neg_word1[0], N3[0])
        sentence_4 = "%s %s %s %s %s %s %s at %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_nonnpi, Neg_word1[0], N3[0])

        # build sentences with no licensor present
        sentence_5 = "some %s %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_npi)
        sentence_6 = "some %s %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_nonnpi)
        sentence_7 = "%s %s %s %s %s %s %s at some %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_npi, N3[0])
        sentence_8 = "%s %s %s %s %s %s %s at some %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Final_nonnpi, N3[0])

        # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
        # but the code outputs a determiner with an empty string. might want to change this)
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
            # sentences 1-4 have negation present
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=1-npi_present=1" % (Final_npi, Neg_word1[0]), 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=1-npi_present=0" % (Final_npi, Neg_word1[0]), 1, sentence_2))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=0-npi_present=1" % (Final_npi, Neg_word3[0]), 0, sentence_3))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=0-npi_present=0" % (Final_npi, Neg_word3[0]), 1, sentence_4))

            # sentences 5-8 have no negation present
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=1-npi_present=1" % Final_npi , 0, sentence_5))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=1-npi_present=0" % Final_npi , 1, sentence_6))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=0-npi_present=1" % Final_npi , 0, sentence_7))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=0-npi_present=0" % Final_npi , 1, sentence_8))

        # keep track of which sentences have already been generated
        sentences.add(sentence_1)

# -------------------------
# 'any' as NPI

sentences = set()

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # No/Some N1          aux         V1       npi_any    N2
    # No      teachers    will        fail     any        students

    try:
        # build all lexical items
        #TODO: throw in modifiers
        N1 = choice(all_non_singular_animate_nouns)
        D1 = choice(get_matched_by(N1, "arg_1", all_def_dets))
        Neg_word1 = choice(get_matched_by(N1, "arg_1", all_neg_det))
        Any = choice(npi_any)
        V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = choice(all_non_singular_nouns_freq)
        D2 = choice(get_matched_by(N2, "arg_1", all_def_dets))
        Neg_word2 = choice(get_matched_by(N2, "arg_1", all_neg_det))
    except IndexError:
        #print(N1[0], N2[0], V1[0])
        continue

    # build sentences with licensor present
    sentence_1 = "%s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], Any[0], N2[0])
    sentence_2 = "%s %s %s %s %s %s ." % (Neg_word1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_3 = "%s %s %s %s %s %s ." % (Any[0], N1[0], Aux1[0], V1[0], Neg_word1[0],  N2[0])
    sentence_4 = "%s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], Neg_word1[0], N2[0])

    # build sentences with no licensor present
    sentence_5 = "some %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], Any[0], N2[0])
    sentence_6 = "some %s %s %s %s %s ." % (N1[0], Aux1[0], V1[0], D2[0], N2[0])
    sentence_7 = "%s %s %s %s some %s ." % (Any[0], N1[0], Aux1[0], V1[0], N2[0])
    sentence_8 = "%s %s %s %s some %s ." % (D1[0], N1[0], Aux1[0], V1[0], N2[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
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
        # sentences 1-4 have negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=1-npi_present=1" % (Any[0], Neg_word1[0]), 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=1-npi_present=0" % (Any[0], Neg_word1[0]), 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=0-npi_present=1" % (Any[0], Neg_word2[0]), 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=%s-licensor=1-scope=0-npi_present=0" % (Any[0], Neg_word2[0]), 1, sentence_4))

        # sentences 5-8 have no negation present
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=1-npi_present=1" % Any[0] , 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=1-npi_present=0" % Any[0] , 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=0-npi_present=1" % Any[0] , 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=determiner_negation_monoclausal-npi=%s-crucial_item=some-licensor=0-scope=0-npi_present=0" % Any[0] , 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)


output.close()