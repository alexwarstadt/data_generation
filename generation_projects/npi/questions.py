
from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# TODO 1: Restrict generation to frequent nouns
# TODO 2: Fix metadata (a) switch "-" and "_" (b) make sure metadata fields match other environments exactly
# TODO 3: Paradigm metadata feature, use generation_projects/npi/add_paradigm_feature.py script

# initialize output file
rel_output_path = "outputs/npi/environment=questions.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 1000
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_non_singular_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1"), ("pl", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))
any_decoys = np.concatenate((get_all("expression", "the"), get_all_conjunctive([("expression", "that"), ("category_2", "D")]),
                         get_all("expression", "this"), get_all("expression", "these"), get_all("expression", "those")))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2   ever  V1   N3
    # Ann   wonders  whether  James  ever ate  apples

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_non_singular_animate_nouns)
    N2 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
    conjugate(V1, N2)
    N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    decoy = choice(["often", "also", "obviously", "clearly", "fortunately"])

    # build sentences with conditional environment
    sentence_1 = "the %s wonder whether the %s ever %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "the %s wonder whether the %s %s %s the %s." % (N1[0], N2[0], decoy, V1[0], N3[0])
    sentence_3 = "the %s ever wonder whether the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "the %s %s wonder whether the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

    # build sentences with conditional-like environment
    sentence_5 = "the %s know that the %s ever %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "the %s know that the %s %s %s the %s." % (N1[0], N2[0], decoy, V1[0], N3[0])
    sentence_7 = "the %s ever know that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "the %s %s know that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=1_scope=0_npi-present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=1_scope=0_npi-present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=0_scope=1_npi-present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=0_scope=0_npi-present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=0_scope=0_npi-present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
        # sentence template
        # N1    wonders  whether   N2    V1  any N3
        # Ann   wonders  whether  James  ate  any apples

        N1 = choice(all_non_singular_animate_nouns)
        N2 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        conjugate(V1, N2)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
        any_decoy_N2 = choice(get_matched_by(N2, "arg_1", any_decoys))
        any_decoy_N3 = choice(get_matched_by(N3, "arg_1", any_decoys))

        # build sentences with conditional environment
        sentence_1 = "the %s wonder whether the %s %s any %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_2 = "the %s wonder whether the %s  %s %s %s." % (N1[0], N2[0], V1[0], any_decoy_N3[0], N3[0])
        sentence_3 = "any %s wonder whether the %s %s  %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_4 = "%s %s wonder whether the %s %s  %s." % (any_decoy_N3[0], N1[0], N2[0], V1[0], N3[0])

        # build sentences with conditional-like environment
        sentence_5 = "the %s know that the %s %s any %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_6 = "the %s know that the %s %s %s %s." % (N1[0], N2[0], V1[0], any_decoy_N3[0], N3[0])
        sentence_7 = "the %s any know that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_8 = "%s %s know that the %s %s the %s." % (any_decoy_N3[0], N1[0], N2[0], V1[0], N3[0])

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
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=1_scope=0_npi-present=1", 0, sentence_3))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=1_scope=0_npi-present=0", 1, sentence_4))
            # sentences 5-8 have non-conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=0_scope=1_npi-present=1", 0, sentence_5))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any licensor=0_scope=1_npi-present=0", 1, sentence_6))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=0_scope=0_npi-present=1", 0, sentence_7))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=0_scope=0_npi-present=0", 1, sentence_8))

        sentences.add(sentence_1)

        sentences = set()
        all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
        while len(sentences) < number_to_generate:
            # sentence template
            # N1    wonders  whether   N2    V1  N3 yet
            # Ann   wonders  whether  James  ate  apples yet

            N1 = choice(all_non_singular_animate_nouns)
            N2 = choice(all_animate_nouns)
            V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
            conjugate(V1, N2)
            N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
            decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])


            # build sentences with conditional environment
            sentence_1 = "the %s wonder whether the %s %s %s yet." % (N1[0], N2[0], V1[0], N3[0])
            sentence_2 = "the %s wonder whether the %s  %s %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_3 = "the %s wonder yet whether the %s %s  %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_4 = "the %s wonder %s whether the %s %s  %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

            # build sentences with conditional-like environment
            sentence_5 = "the %s know that the %s %s the %s yet." % (N1[0], N2[0], V1[0], N3[0])
            sentence_6 = "the %s know that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_7 = "the %s know yet that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_8 = "the %s know %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet_licensor=1_scope=1_npi-present=1", 1, sentence_1))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet_licensor=1_scope=1_npi-present=0", 1, sentence_2))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet_licensor=1_scope=0_npi-present=1", 0, sentence_3))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet_licensor=1_scope=0_npi-present=0", 1, sentence_4))
                # sentences 5-8 have non-conditional environment
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet_licensor=0_scope=1_npi-present=1", 0, sentence_5))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet licensor=0_scope=1_npi-present=0", 1, sentence_6))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet_licensor=0_scope=0_npi-present=1", 0, sentence_7))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=yet_licensor=0_scope=0_npi-present=0", 1, sentence_8))

            sentences.add(sentence_1)

sentences = set()
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
            # sentence template
            # N1    wonders  whether   N2    V1  N3 at all
            # Ann   wonders  whether  James  ate  apples at all

            N1 = choice(all_non_singular_animate_nouns)
            N2 = choice(all_animate_nouns)
            V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
            conjugate(V1, N2)
            N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
            decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])


            # build sentences with conditional environment
            sentence_1 = "the %s wonder whether the %s %s %s at all." % (N1[0], N2[0], V1[0], N3[0])
            sentence_2 = "the %s wonder whether the %s  %s %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_3 = "the %s wonder at all  whether the %s %s  %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_4 = "the %s wonder %s whether the %s %s  %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

            # build sentences with conditional-like environment
            sentence_5 = "the %s know that the %s %s the %s at all." % (N1[0], N2[0], V1[0], N3[0])
            sentence_6 = "the %s know that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_7 = "the %s know at all that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_8 = "the %s know  %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=1_scope=1_npi-present=1", 1, sentence_1))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=1_scope=1_npi-present=0", 1, sentence_2))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=1_scope=0_npi-present=1", 0, sentence_3))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=1_scope=0_npi-present=0", 1, sentence_4))
                # sentences 5-8 have non-conditional environment
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=0_scope=1_npi-present=1", 0, sentence_5))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=0_scope=1_npi-present=0", 1, sentence_6))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=0_scope=0_npi-present=1", 0, sentence_7))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=atall_licensor=0_scope=0_npi-present=0", 1, sentence_8))

            sentences.add(sentence_1)

sentences = set()

all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
            # sentence template
            # N1    wonders  whether   N2    V1  N3 in years
            # Ann   wonders  whether  James  ate  apples in years

            N1 = choice(all_non_singular_animate_nouns)
            N2 = choice(all_animate_nouns)
            V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
            conjugate(V1, N2)
            N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
            decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])


            # build sentences with conditional environment
            sentence_1 = "the %s wonder whether the %s %s the %s in years." % (N1[0], N2[0], V1[0], N3[0])
            sentence_2 = "the %s wonder whether the %s  %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_3 = "the %s wonder in years whether the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_4 = "the %s  wonder %s whether the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

            # build sentences with conditional-like environment
            sentence_5 = "the %s know that the %s %s  %s in years." % (N1[0], N2[0], V1[0], N3[0])
            sentence_6 = "the %s know that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_7 = "the %s know in years that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_8 = "the %s know  %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=1_scope=1_npi-present=1", 0, sentence_1))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=1_scope=1_npi-present=0", 1, sentence_2))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=1_scope=0_npi-present=1", 0, sentence_3))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=1_scope=0_npi-present=0", 1, sentence_4))
                # sentences 5-8 have non-conditional environment
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=0_scope=1_npi-present=1", 0, sentence_5))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=0_scope=1_npi-present=0", 1, sentence_6))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=0_scope=0_npi-present=1", 0, sentence_7))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=inyears_licensor=0_scope=0_npi-present=0", 1, sentence_8))

            sentences.add(sentence_1)


sentences = set()

all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
            # sentence template
            # N1    wonders  whether   N2    V1  N3 in years
            # Ann   wonders  whether  James  ate  apples in years

            N1 = choice(all_non_singular_animate_nouns)
            N2 = choice(all_animate_nouns)
            V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
            conjugate(V1, N2)
            N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
            decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])


            # build sentences with conditional environment
            sentence_1 = "the %s wonder whether the %s %s the %s either." % (N1[0], N2[0], V1[0], N3[0])
            sentence_2 = "the %s wonder whether the %s  %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_3 = "the %s wonder either whether the %s %s  the %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_4 = "the %s wonder %s whether the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

            # build sentences with conditional-like environment
            sentence_5 = "the %s know that the %s %s the  %s either." % (N1[0], N2[0], V1[0], N3[0])
            sentence_6 = "the %s know that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
            sentence_7 = "the %s know either that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
            sentence_8 = "the %s know %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=1_scope=1_npi-present=1", 0, sentence_1))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=1_scope=1_npi-present=0", 1, sentence_2))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=1_scope=0_npi-present=1", 0, sentence_3))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=1_scope=0_npi-present=0", 1, sentence_4))
                # sentences 5-8 have non-conditional environment
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=0_scope=1_npi-present=1", 0, sentence_5))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=0_scope=1_npi-present=0", 1, sentence_6))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=0_scope=0_npi-present=1", 0, sentence_7))
                output.write("%s\t%d\t\t%s\n" % (
                    "experiment=NPI_env=questions_npi=either_licensor=0_scope=0_npi-present=0", 1, sentence_8))

            sentences.add(sentence_1)


output.close()