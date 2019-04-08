
from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=conditionals.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))
any_decoys = np.concatenate((get_all("expression", "the"), get_all_conjunctive([("expression", "that"), ("category_2", "D")]),
                         get_all("expression", "this"), get_all("expression", "these"), get_all("expression", "those")))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # if     N1  ever  V1        N2     N1   should   V2   N3
    # if    you  ever  bought    apples  you  should   eat  them

    # build all lexical items
    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V2, N1, allow_negated=False)
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    decoy = choice(["often", "also", "obviously", "clearly", "fortunately"])

    # build sentences with conditional environment
    sentence_1 = "if the %s ever %s the %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_2 = "if the %s %s %s the %s, the %s  %s the %s ." % (N1[0], decoy, V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_3 = "ever if the %s %s the %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_4 = "%s if the %s %s the %s, the %s  %s the %s ." % (decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

    # build sentences with conditional-like environment
    sentence_5 = "while the %s ever %s the %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_6 = "while the %s %s %s the %s, the %s  %s the %s ." % (N1[0], decoy, V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_7 = "ever while the %s %s the %s, the %s %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_8 = "%s while the %s %s the %s, the %s %s the %s ." % (decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=1_scope=0_npi-present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=1_scope=0_npi-present=0", 0, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=ever_licensor=0_scope=0_npi-present=0", 0, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)
# the end :)

sentences = set()
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
    # sentence template
    # if  the   N1     V1     any  N2      the N  V2 the N3.
    # if  the   boy   bought  any  apples  the boy should eat them.

    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V2, N1, allow_negated=False)
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    any_decoy_N2 = choice(get_matched_by(N2, "arg_1", any_decoys))
    any_decoy_N3 = choice(get_matched_by(N3, "arg_1", any_decoys))


    # build sentences with conditional environment
    sentence_1 = "if the %s %s any %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_2 = "if the %s  %s %s %s, the %s  %s the %s ." % (N1[0], V1[0], any_decoy_N2[0], N2[0], N1[0], V2[0], N3[0])
    sentence_3 = "any if the %s %s  %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_4 = "%s if  the %s %s  %s, the %s  %s the %s ." % (any_decoy_N2[0], N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

    # build sentences with conditional-like environment
    sentence_5 = "while the %s  %s any %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_6 = "while the %s  %s %s %s, the %s  %s the %s ." % (N1[0], V1[0], any_decoy_N2[0], N2[0], N1[0], V2[0], N3[0])
    sentence_7 = "any while the %s %s  %s, the %s %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_8 = "%s while the %s %s  %s, the %s %s the %s ." % (any_decoy_N2[0], N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])


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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=1_scope=0_npi-present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=1_scope=0_npi-present=0", 0, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=any_licensor=0_scope=0_npi-present=0", 0, sentence_8))

    sentences.add(sentence_1)


sentences = set()
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
    # sentence template
    # if  the   N1     V1     the  N2  yet, the N V2 the N3.
    # if  the   boy   bought  the  apples yet, the boy should eat them.

    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V2, N1, allow_negated=False)
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])


    # build sentences with conditional environment
    sentence_1 = "if the %s %s the %s yet, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_2 = "if the %s  %s the %s %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
    sentence_3 = "yet if the %s %s  the %s , the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_4 = "%s if  the %s %s the %s, the %s  %s the %s ." % (decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

    # build sentences with conditional-like environment
    sentence_5 = "while the %s  %s the %s yet, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_6 = "while the %s  %s the %s %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
    sentence_7 = "yet while the %s %s the %s, the %s %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
    sentence_8 = "%s while the %s %s the %s, the %s %s the %s ." % (decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])


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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=1_scope=0_npi-present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=1_scope=0_npi-present=0", 0, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=conditional_npi=yet_licensor=0_scope=0_npi-present=0", 0, sentence_8))

    sentences.add(sentence_1)

    sentences = set()
    all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
    while len(sentences) < number_to_generate:
        # sentence template
        # if  the   N1     V1     the  N2  at all, the N V2 the N3.
        # if  the   boy   bought  the  apples at all, the boy should eat them.

        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
        V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        conjugate(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

        # build sentences with conditional environment
        sentence_1 = "if the %s %s the %s at all, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
        sentence_2 = "if the %s  %s the %s %s, the %s  %s the %s ." % (N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
        sentence_3 = "at all if the %s %s  the %s , the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
        sentence_4 = "%s if  the %s %s the %s, the %s  %s the %s ." % (decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

        # build sentences with conditional-like environment
        sentence_5 = "while the %s  %s the %s at all, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
        sentence_6 = "while the %s  %s the %s %s, the %s  %s the %s ." % (
        N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
        sentence_7 = "at all while the %s %s the %s, the %s %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
        sentence_8 = "%s while the %s %s the %s, the %s %s the %s ." % (decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

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
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=1_scope=1_npi-present=0", 1, sentence_2))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=1_scope=0_npi-present=1", 0, sentence_3))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=1_scope=0_npi-present=0", 0, sentence_4))
            # sentences 5-8 have non-conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=0_scope=1_npi-present=1", 0, sentence_5))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=0_scope=1_npi-present=0", 1, sentence_6))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=0_scope=0_npi-present=1", 0, sentence_7))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=conditional_npi=atall_licensor=0_scope=0_npi-present=0", 0, sentence_8))

        sentences.add(sentence_1)

        sentences = set()
        all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
        while len(sentences) < number_to_generate:
            # sentence template
            # if  the   N1     V1     the  N2  at all, the N V2 the N3.
            # if  the   boy   bought  the  apples in years, the boy should eat them.

            N1 = choice(all_animate_nouns)
            V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            conjugate(V1, N1, allow_negated=False)
            N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
            V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            conjugate(V2, N1, allow_negated=False)
            N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
            decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

            # build sentences with conditional environment
            sentence_1 = "if the %s %s the %s in years, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_2 = "if the %s  %s the %s %s, the %s  %s the %s ." % (
            N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
            sentence_3 = "in years if the %s %s  the %s , the %s  %s the %s ." % (
            N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_4 = "%s if  the %s %s the %s, the %s  %s the %s ." % (
            decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

            # build sentences with conditional-like environment
            sentence_5 = "while the %s  %s the %s in years, the %s  %s the %s ." % (
            N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_6 = "while the %s  %s the %s %s, the %s  %s the %s ." % (
                N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
            sentence_7 = "in years while the %s %s the %s, the %s %s the %s ." % (
            N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_8 = "%s while the %s %s the %s, the %s %s the %s ." % (
            decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

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
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=1_npi-present=1", 1, sentence_1))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=1_npi-present=0", 1, sentence_2))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=0_npi-present=1", 0, sentence_3))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=0_npi-present=0", 0, sentence_4))
                # sentences 5-8 have non-conditional environment
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=1_npi-present=1", 0, sentence_5))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=1_npi-present=0", 1, sentence_6))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=0_npi-present=1", 0, sentence_7))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=0_npi-present=0", 0, sentence_8))

            sentences.add(sentence_1)

        sentences = set()
        all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
        while len(sentences) < number_to_generate:
            # sentence template
            # if  the   N1     V1     the  N2  at all, the N V2 the N3.
            # if  the   boy   bought  the  apples in years, the boy should eat them.

            N1 = choice(all_animate_nouns)
            V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            conjugate(V1, N1, allow_negated=False)
            N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
            V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
            conjugate(V2, N1, allow_negated=False)
            N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
            decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

            # build sentences with conditional environment
            sentence_1 = "if the %s %s the %s either, the %s  %s the %s ." % (N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_2 = "if the %s  %s the %s %s, the %s  %s the %s ." % (
            N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
            sentence_3 = "either if the %s %s  the %s , the %s  %s the %s ." % (
            N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_4 = "%s if  the %s %s the %s, the %s  %s the %s ." % (
            decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

            # build sentences with conditional-like environment
            sentence_5 = "while the %s  %s the %s either, the %s  %s the %s ." % (
            N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_6 = "while the %s  %s the %s %s, the %s  %s the %s ." % (
                N1[0], V1[0], N2[0], decoy, N1[0], V2[0], N3[0])
            sentence_7 = "either while the %s %s the %s, the %s %s the %s ." % (
            N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])
            sentence_8 = "%s while the %s %s the %s, the %s %s the %s ." % (
            decoy, N1[0], V1[0], N2[0], N1[0], V2[0], N3[0])

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
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=1_npi-present=1", 1, sentence_1))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=1_npi-present=0", 1, sentence_2))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=0_npi-present=1", 0, sentence_3))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=1_scope=0_npi-present=0", 0, sentence_4))
                # sentences 5-8 have non-conditional environment
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=1_npi-present=1", 0, sentence_5))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=1_npi-present=0", 1, sentence_6))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=0_npi-present=1", 0, sentence_7))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=conditional_npi=inyears_licensor=0_scope=0_npi-present=0", 0, sentence_8))

            sentences.add(sentence_1)


output.close()