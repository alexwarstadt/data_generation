
from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=questions.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2   ever  V1   N3
    # Ann   wonders  whether  James  ever ate  apples

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    N2 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
    conjugate(V1, N1)
    N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))

    # build sentences with conditional environment
    sentence_1 = "the %s wonder whether the %s ever %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "the %s wonder whether the %s often %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_3 = "the %s ever wonder whether the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "the %s often wonder whether the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])

    # build sentences with conditional-like environment
    sentence_5 = "the %s know that the %s ever %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "the %s know that the %s often %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_7 = "the %s ever know that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "the %s often know that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=questions_npi=ever_licensor=1_scope=0_npi-present=0", 0, sentence_4))
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

        N1 = choice(all_animate_nouns)
        N2 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        conjugate(V1, N1)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))

        # build sentences with conditional environment
        sentence_1 = "the %s wonder whether the %s %s any %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_2 = "the %s wonder whether the %s  %s the %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_3 = "the %s any wonder whether the %s %s  %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_4 = "the %s the wonder whether the %s %s  %s." % (N1[0], N2[0], V1[0], N3[0])

        # build sentences with conditional-like environment
        sentence_5 = "the %s know that the %s %s any %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_6 = "the %s know that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_7 = "the %s any know that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
        sentence_8 = "the %s the know that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])

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
            "experiment=NPI_env=questions_npi=any_licensor=1_scope=0_npi-present=0", 0, sentence_4))
            # sentences 5-8 have non-conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=0_scope=1_npi-present=1", 0, sentence_5))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any licensor=0_scope=1_npi-present=0", 1, sentence_6))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=0_scope=0_npi-present=1", 0, sentence_7))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=questions_npi=any_licensor=0_scope=0_npi-present=0", 0, sentence_8))

        sentences.add(sentence_1)

output.close()