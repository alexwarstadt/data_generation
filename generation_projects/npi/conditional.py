
from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
# from random import choice
import numpy as np
from utils.randomize import choice
import os
from outputs.npi.post_process_data import add_paradigm_feature

# initialize output file
rel_output_path = "outputs/npi/environment=conditionals.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 1000
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_present_transitive_verbs = get_all("pres", "1", all_transitive_verbs)
all_bare_transitive_verbs = get_all("bare", "1", all_transitive_verbs)
all_en_transitive_verbs = get_all("en", "1", all_transitive_verbs)
all_nonfuture_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"),("past", "1")])
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
any_decoys = np.concatenate((get_all("expression", "the"), get_all_conjunctive([("expression", "that"), ("category_2", "D")]),
                         get_all("expression", "this"), get_all("expression", "these"), get_all("expression", "those")))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # if    N1  ever  V1   N2      N1       will   V2    N3
    # if    you  ever buy  apples, waiters  will   eat   cake

    # build all lexical items
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_present_transitive_verbs))
        # Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(all_animate_nouns, [N1, N2])
        V2 = choice(get_matched_by(N3, "arg_1", all_bare_transitive_verbs))
        # Aux2 = return_aux(V2, N3, allow_negated=False)
        N4 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2, N3])
        decoy = choice(["often", "also", "obviously", "clearly", "fortunately"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "If the %s ever %s the %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_2 = "If the %s %s %s the %s, the %s will %s the %s." % (N1[0], decoy, V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_3 = "If the %s %s the %s, the %s will ever %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_4 = "If the %s %s the %s, the %s will %s %s the %s." % (N1[0], V1[0], N2[0], N3[0], decoy, V2[0], N4[0])

    # build sentences with conditional-like environment
    sentence_5 = "While the %s ever %s the %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_6 = "While the %s %s %s the %s, the %s will %s the %s." % (N1[0], decoy, V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_7 = "While the %s %s the %s, the %s will ever %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_8 = "While the %s %s the %s, the %s will %s %s the %s." % (N1[0], V1[0], N2[0], N3[0], decoy, V2[0], N4[0])

    # remove doubled up spaces
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
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=if-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=if-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=if-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=if-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=while-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=while-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=while-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=ever-crucial_item=while-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)
# the end :)

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # if  the   N1     V1     any  N2      the N  V2 the N3.
    # if  the   boy   bought  any  apples  the boy should eat them.
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_present_transitive_verbs))
        # V1 = conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(all_animate_nouns, [N1, N2])
        V2 = choice(get_matched_by(N3, "arg_1", all_bare_transitive_verbs), [V1])
        # V2 = conjugate(V2, N3, allow_negated=False)
        N4 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2, N3])
        any_decoy_N2 = choice(get_matched_by(N2, "arg_1", any_decoys))
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "If the %s %s any %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_2 = "If the %s %s %s %s, the %s will %s the %s." % (N1[0], V1[0], any_decoy_N2[0], N2[0], N3[0], V2[0], N4[0])
    sentence_3 = "If the %s %s the %s, the %s will %s any %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_4 = "If the %s %s the %s, the %s will %s %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], any_decoy_N2[0], N4[0])

    # build sentences with conditional-like environment
    sentence_5 = "While the %s %s any %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_6 = "While the %s %s %s %s, the %s will %s the %s." % (N1[0], V1[0], any_decoy_N2[0], N2[0], N3[0], V2[0], N4[0])
    sentence_7 = "While the %s %s the %s, the %s will %s any %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_8 = "While the %s %s the %s, the %s will %s %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], any_decoy_N2[0], N4[0])


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
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=if-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=if-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=if-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=if-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=while-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=while-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=while-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=any-crucial_item=while-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)



sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # if  the   N1     V1     the  N2  yet, the N V2 the N3.
    # if  the   boy   bought  the  apples yet, the boy should eat them.
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_present_transitive_verbs))
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(all_animate_nouns, [N1, N2])
        V2 = choice(get_matched_by(N3, "arg_1", all_bare_transitive_verbs), [V1])
        N4 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2, N3])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "If the %s %s the %s yet, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_2 = "If the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_3 = "If the %s %s the %s, the %s will %s the %s yet." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_4 = "If the %s %s the %s, the %s will %s the %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "While the %s %s the %s yet, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_6 = "While the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_7 = "While the %s %s the %s, the %s will %s the %s yet." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_8 = "While the %s %s the %s, the %s will %s the %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)


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
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=if-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=if-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=if-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=if-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=while-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=while-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=while-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=yet-crucial_item=while-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
        # sentence template
        # if  the   N1     V1     the  N2  at all, the N V2 the N3.
        # if  the   boy   bought  the  apples at all, the boy should eat them.
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_present_transitive_verbs))
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(all_animate_nouns, [N1, N2])
        V2 = choice(get_matched_by(N3, "arg_1", all_bare_transitive_verbs), [V1])
        N4 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2, N3])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "If the %s %s the %s at all, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_2 = "If the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_3 = "If the %s %s the %s, the %s will %s the %s at all." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_4 = "If the %s %s the %s, the %s will %s the %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "While the %s %s the %s at all, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_6 = "While the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_7 = "While the %s %s the %s, the %s will %s the %s at all." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_8 = "While the %s %s the %s, the %s will %s the %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)

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
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=if-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=if-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=if-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=if-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=while-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=while-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=while-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=atall-crucial_item=while-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # if  the   N1    Aux V1_en   the  N2  at all, the N V2 the N3.
    # if  the   boy   has bought  the  apples in years, the boy should eat them.
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_en_transitive_verbs))
        V1 = conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(all_animate_nouns, [N1, N2])
        V2 = choice(get_matched_by(N3, "arg_1", all_bare_transitive_verbs))
        N4 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2, N3])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0], V2[0], "in-years")
        continue
    except TypeError:
        print("Type error")
        continue

    # build sentences with conditional environment
    sentence_1 = "If the %s %s the %s in years, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_2 = "If the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_3 = "If the %s %s the %s, the %s will %s the %s in years." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_4 = "If the %s %s the %s, the %s will %s the %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "While the %s %s the %s in years, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_6 = "While the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_7 = "While the %s %s the %s, the %s will %s the %s in years." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_8 = "While the %s %s the %s, the %s will %s the %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)

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
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=if-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=if-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=if-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=if-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=while-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=while-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=while-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=inyears-crucial_item=while-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # if  the   N1     V1     the  N2  at all, the N3 V2 the N4.
    # if  the   boy   bought  the  apples in years, the girl should eat them.
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_present_transitive_verbs))
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(all_animate_nouns, [N1, N2])
        V2 = choice(get_matched_by(N3, "arg_1", all_bare_transitive_verbs), [V1])
        N4 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2, N3])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "If the %s %s the %s either, the %s will %s the %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_2 = "If the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_3 = "If the %s %s the %s, the %s will %s the %s either." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_4 = "If the %s %s the %s, the %s will %s the %s %s." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "While the %s %s the %s either, the %s will %s the %s ." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_6 = "While the %s %s the %s %s, the %s will %s the %s." % (N1[0], V1[0], N2[0], decoy, N3[0], V2[0], N4[0])
    sentence_7 = "While the %s %s the %s, the %s will %s the %s either ." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0])
    sentence_8 = "While the %s %s the %s, the %s will %s the %s %s ." % (N1[0], V1[0], N2[0], N3[0], V2[0], N4[0], decoy)

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
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=if-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=if-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=if-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=if-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=while-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=while-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=while-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=conditional-npi=either-crucial_item=while-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)


output.close()

# add paradigm parameter to metadata
dataset_path = os.path.join(project_root, rel_output_path)
output_path = os.path.join(project_root, rel_output_path)
add_paradigm_feature(dataset_path, output_path)