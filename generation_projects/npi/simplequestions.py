from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np


# initialize output file
rel_output_path = "outputs/npi/environment=simplequestions.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 1000
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_nonfinite_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0")])
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
    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False) #numpy set diff, get rid of empty strings
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))

    # build sentences with conditional environment
    sentence_1 = "%s the %s ever %s the %s?" % (Aux1[0], N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s often %s the %s?" % (Aux1[0], N1[0], V1[0], N2[0])

    # build sentences with conditional-like environment
    sentence_5 = "the %s ever %s %s the %s." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "the %s often %s %s the %s." % (N1[0], Aux1[0], V1[0], N2[0])

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=simplequestions_npi=ever_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=simplequestions_npi=ever_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=simplequestions_npi=ever_licensor=0_scope=1_npi-present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=simplequestions_npi=ever_licensor=0_scope=1_npi-present=0", 1, sentence_6))


    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
        # sentence template
        # N1    wonders  whether   N2    V1  any N3
        # Ann   wonders  whether  James  ate  any apples

        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
        any_decoy_N1 = choice(get_matched_by(N1, "arg_1", any_decoys))

        # build sentences with conditional environment
        sentence_1 = "%s any %s %s the %s?" % (Aux1[0], N1[0], V1[0],  N2[0])
        sentence_2 = "%s %s %s  %s the %s?" % (Aux1[0], any_decoy_N1[0], N1[0], V1[0], N2[0])

        # build sentences with conditional-like environment
        sentence_5 = "any %s %s %s the %s." % (N1[0], Aux1[0], V1[0], N2[0])
        sentence_6 = "%s %s %s %s the %s." % (any_decoy_N1[0], N1[0], Aux1[0], V1[0], N2[0])

        # remove doubled up spaces
        sentence_1 = remove_extra_whitespace(sentence_1)
        sentence_2 = remove_extra_whitespace(sentence_2)
        sentence_5 = remove_extra_whitespace(sentence_5)
        sentence_6 = remove_extra_whitespace(sentence_6)

        # write sentences to output
        if sentence_1 not in sentences:
            # sentences 1-4 have conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
              # sentences 5-8 have non-conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=0_scope=1_npi-present=1", 1, sentence_5))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=0_scope=1_npi-present=0", 1, sentence_6))

        # keep track of which sentences have already been generated
        sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
        # sentence template
        # N1    wonders  whether   N2    V1  any N3
        # Ann   wonders  whether  James  ate  any apples

        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))

        # build sentences with conditional environment
        sentence_1 = "%s any %s %s the %s?" % (Aux1[0], N1[0], V1[0], N2[0])
        sentence_2 = "%s the %s  %s the %s?" % (Aux1[0], N1[0], V1[0], N2[0])

        # build sentences with conditional-like environment
        sentence_5 = "any %s %s %s the %s." % (N1[0], Aux1[0], V1[0], N2[0])
        sentence_6 = "the %s %s %s the %s." % (N1[0], Aux1[0], V1[0], N2[0])

        # remove doubled up spaces
        sentence_1 = remove_extra_whitespace(sentence_1)
        sentence_2 = remove_extra_whitespace(sentence_2)
        sentence_5 = remove_extra_whitespace(sentence_5)
        sentence_6 = remove_extra_whitespace(sentence_6)

        # write sentences to output
        if sentence_1 not in sentences:
            # sentences 1-4 have conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
              # sentences 5-8 have non-conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=0_scope=1_npi-present=1", 1, sentence_5))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=any_licensor=0_scope=1_npi-present=0", 1, sentence_6))

        # keep track of which sentences have already been generated
        sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
        # sentence template
        # N1    wonders  whether   N2    V1  any N3
        # Ann   wonders  whether  James  ate  any apples

        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

        # build sentences with conditional environment
        sentence_1 = "%s the %s %s the %s yet?" % (Aux1[0], N1[0], V1[0], N2[0])
        sentence_2 = "%s the %s  %s the %s %s?" % (Aux1[0], N1[0], V1[0], N2[0], decoy)

        # build sentences with conditional-like environment
        sentence_5 = "any %s %s %s the %s yet." % (N1[0], Aux1[0], V1[0], N2[0])
        sentence_6 = "the %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

        # remove doubled up spaces
        sentence_1 = remove_extra_whitespace(sentence_1)
        sentence_2 = remove_extra_whitespace(sentence_2)
        sentence_5 = remove_extra_whitespace(sentence_5)
        sentence_6 = remove_extra_whitespace(sentence_6)

        # write sentences to output
        if sentence_1 not in sentences:
            # sentences 1-4 have conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=1_scope=1_npi-present=0", 1, sentence_2))
              # sentences 5-8 have non-conditional environment
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=0_scope=1_npi-present=1", 1, sentence_5))
            output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=0_scope=1_npi-present=0", 1, sentence_6))

        # keep track of which sentences have already been generated
        sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  any N3
    # Ann   wonders  whether  James  ate  any apples

    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

    # build sentences with conditional environment
    sentence_1 = "%s the %s %s the %s at all?" % (Aux1[0], N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s  %s the %s %s?" % (Aux1[0], N1[0], V1[0], N2[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "any %s %s %s the %s at all." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "the %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=atall_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=atall_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=atall_licensor=0_scope=1_npi-present=1", 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=atall_licensor=0_scope=1_npi-present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  any N3
    # Ann   wonders  whether  James  ate  any apples

    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

    # build sentences with conditional environment
    sentence_1 = "%s the %s %s the %s in years?" % (Aux1[0], N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s  %s the %s %s?" % (Aux1[0], N1[0], V1[0], N2[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "any %s %s %s the %s in years." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "the %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=inyears_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=inyears_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=inyears_licensor=0_scope=1_npi-present=1", 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=inyears_licensor=0_scope=1_npi-present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  any N3
    # Ann   wonders  whether  James  ate  any apples

    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

    # build sentences with conditional environment
    sentence_1 = "%s the %s %s the %s yet?" % (Aux1[0], N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s  %s the %s %s?" % (Aux1[0], N1[0], V1[0], N2[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "any %s %s %s the %s yet." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "the %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=0_scope=1_npi-present=1", 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=yet_licensor=0_scope=1_npi-present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  any N3
    # Ann   wonders  whether  James  ate  any apples

    N1 = choice(all_animate_nouns)
    V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])

    # build sentences with conditional environment
    sentence_1 = "%s the %s %s the %s either?" % (Aux1[0], N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s  %s the %s %s?" % (Aux1[0], N1[0], V1[0], N2[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "any %s %s %s the %s either." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "the %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=either_licensor=1_scope=1_npi-present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=either_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=either_licensor=0_scope=1_npi-present=1", 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI_env=simplequestions_npi=either_licensor=0_scope=1_npi-present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

output.close()
