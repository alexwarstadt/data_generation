from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
# from random import choice
import numpy as np
from utils.randomize import choice

# TODO 3: Paradigm metadata feature, use generation_projects/npi/add_paradigm_feature.py script

# initialize output file
rel_output_path = "outputs/npi/environment=simplequestions.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_nonfinite_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0")])
all_past_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0"), ("en", "1")])
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
any_decoys = np.concatenate((get_all("expression", "the"), get_all_conjunctive([("expression", "that"), ("category_2", "D")]),
                         get_all("expression", "this"), get_all("expression", "these"), get_all("expression", "those")))

# begin ever

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # Aux1 the N1   ever V1  the N2?
    # Did  the girl ever eat the apples?

    # build all lexical items
    #TODO: throw in modifiers
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False) #numpy set diff, get rid of empty strings
        Aux1_capital = Aux1[0].capitalize()
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        decoy = choice(["often", "also", "obviously", "clearly", "fortunately"])
    except IndexError:
        print(N1[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "%s the %s ever %s the %s?" % (Aux1_capital, N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s %s %s the %s?" % (Aux1_capital, N1[0], decoy, V1[0], N2[0])

    # build sentences with non-question environment
    sentence_5 = "The %s %s ever %s the %s." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "The %s %s %s %s the %s." % (N1[0], Aux1[0], decoy, V1[0], N2[0])

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=ever-crucial_item=?-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=ever-crucial_item=?-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        # sentences 5-8 have non-question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=ever-crucial_item=?-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=ever-crucial_item=?-licensor=0-scope=1-npi_present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of ever

# repeat for any

sentences = set()
while len(sentences) < number_to_generate:
        # sentence template
        # Aux1 the N1   V1  any N2?
        # Did  the girl eat any apples?
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        Aux1_capital = Aux1[0].capitalize()
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        any_decoy_N2 = choice(get_matched_by(N2, "arg_1", any_decoys))
    except IndexError:
        print(N1[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "%s the %s %s any %s?" % (Aux1_capital, N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s %s %s %s?" % (Aux1_capital, N1[0], V1[0], any_decoy_N2[0], N2[0])

    # build sentences with question-like environment
    sentence_5 = "The %s %s %s any %s." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "The %s %s %s %s %s." % (N1[0], Aux1[0], V1[0], any_decoy_N2[0], N2[0])

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=any-crucial_item=?-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=any-crucial_item=?-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        # sentences 5-8 have non-question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=any-crucial_item=?-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=simplequestions-npi=any-crucial_item=?-licensor=0-scope=1-npi_present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of any

# repeat for at all

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # Aux1 the N1   V1  the N2     at all?
    # Did  the girl eat the apples at all?
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        Aux1_capital = Aux1[0].capitalize()
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "%s the %s %s the %s at all?" % (Aux1_capital, N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s %s the %s %s?" % (Aux1_capital, N1[0], V1[0], N2[0], decoy)

    # build sentences with non-question environment
    sentence_5 = "The %s %s %s the %s at all." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "The %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=atall-crucial_item=?-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=atall-crucial_item=?-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=atall-crucial_item=?-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=atall-crucial_item=?-licensor=0-scope=1-npi_present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of at all

# repeat for in years

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # Aux1 the N1   V1_en the N2     in years?
    # Had  the girl eaten the apples in years?
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_past_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        Aux1_capital = Aux1[0].capitalize()
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "%s the %s %s the %s in years?" % (Aux1_capital, N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s %s the %s %s?" % (Aux1_capital, N1[0], V1[0], N2[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "The %s %s %s the %s in years." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "The %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=inyears-crucial_item=?-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=inyears-crucial_item=?-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=inyears-crucial_item=?-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=inyears-crucial_item=?-licensor=0-scope=1-npi_present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of in years

# repeat for yet

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # Aux1 the N1   V1  the N2     yet?
    # Did  the girl eat the apples yet?
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        Aux1_capital = Aux1[0].capitalize()
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "%s the %s %s the %s yet?" % (Aux1_capital, N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s %s the %s %s?" % (Aux1_capital, N1[0], V1[0], N2[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "The %s %s %s the %s yet." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "The %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=yet-crucial_item=?-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=yet-crucial_item=?-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=yet-crucial_item=?-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=yet-crucial_item=?-licensor=0-scope=1-npi_present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of yet

# repeat for either

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # Aux1 the N1   V1  the N2     either?
    # Did  the girl eat the apples either?
    try:
        N1 = choice(all_animate_nouns)
        V1 = choice(get_matched_by(N1, "arg_1", all_nonfinite_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        Aux1_capital = Aux1[0].capitalize()
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], V1[0])
        continue

    # build sentences with conditional environment
    sentence_1 = "%s the %s %s the %s either?" % (Aux1_capital, N1[0], V1[0], N2[0])
    sentence_2 = "%s the %s %s the %s %s?" % (Aux1_capital, N1[0], V1[0], N2[0], decoy)

    # build sentences with conditional-like environment
    sentence_5 = "The %s %s %s the %s either." % (N1[0], Aux1[0], V1[0], N2[0])
    sentence_6 = "The %s %s %s the %s %s." % (N1[0], Aux1[0], V1[0], N2[0], decoy)

    # remove doubled up spaces
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=either-crucial_item=?-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=either-crucial_item=?-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=either-crucial_item=?-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (
            "experiment=NPI-env=simplequestions-npi=either-crucial_item=?-licensor=0-scope=1-npi_present=0", 1, sentence_6))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

output.close()