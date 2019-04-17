
from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
# from random import choice
import numpy as np
from utils.randomize import choice
import os
from outputs.npi.post_process_data import add_paradigm_feature

# initialize output file
rel_output_path = "outputs/npi/environment=questions.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_non_singular_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1"), ("pl", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
any_decoys = np.concatenate((get_all("expression", "the"), get_all_conjunctive([("expression", "that"), ("category_2", "D")]),
                         get_all("expression", "this"), get_all("expression", "these"), get_all("expression", "those")))

# sample sentences until desired number
while len(sentences) < number_to_generate:

    # ever sentences

    # sentence template
    # The N1    wonder  whether N2    ever V1   N3
    # The girls wonder  whether James ever ate  apples

    # build all lexical items
    #TODO: throw in modifiers
    try:
        N1 = choice(all_non_singular_animate_nouns)
        N2 = choice(all_animate_nouns, [N1])
        V1 = choice(get_matched_by(N2, "arg_1", all_non_progressive_transitive_verbs))
        V1 = conjugate(V1, N2, allow_negated=False)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1, N2])
        decoy = choice(["often", "also", "obviously", "clearly", "fortunately"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "The %s wonder whether the %s ever %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "The %s wonder whether the %s %s %s the %s." % (N1[0], N2[0], decoy, V1[0], N3[0])
    sentence_3 = "The %s ever wonder whether the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "The %s %s wonder whether the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

    # build sentences with non-question environment
    sentence_5 = "The %s say that the %s ever %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "The %s say that the %s %s %s the %s." % (N1[0], N2[0], decoy, V1[0], N3[0])
    sentence_7 = "The %s ever say that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "The %s %s say that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
        # sentences 1-4 have question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-crucial_item=whether-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of ever

# repeat for any

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  any N3
    # Ann   wonders  whether  James  ate any apples
    try:
        N1 = choice(all_non_singular_animate_nouns)
        N2 = choice(all_animate_nouns, [N1])
        V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N2, allow_negated=False)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1, N2])
        any_decoy_N1 = choice(get_matched_by(N1, "arg_1", any_decoys))
        any_decoy_N1_capital = any_decoy_N1[0].capitalize()
        any_decoy_N3 = choice(get_matched_by(N3, "arg_1", any_decoys))
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "The %s wonder whether the %s %s any %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "The %s wonder whether the %s %s %s %s." % (N1[0], N2[0], V1[0], any_decoy_N3[0], N3[0])
    sentence_3 = "Any %s wonder whether the %s %s %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "%s %s wonder whether the %s %s %s." % (any_decoy_N1_capital, N1[0], N2[0], V1[0], N3[0])

    # build sentences with question-like environment
    sentence_5 = "The %s say that the %s %s any %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "The %s say that the %s %s %s %s." % (N1[0], N2[0], V1[0], any_decoy_N3[0], N3[0])
    sentence_7 = "Any %s say that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "%s %s say that the %s %s the %s." % (any_decoy_N1_capital, N1[0], N2[0], V1[0], N3[0])

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
        # sentences 1-4 have question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=any-crucial_item=whether-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of any

# repeat for yet

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  N3 yet
    # Ann   wonders  whether  James  ate  apples yet
    try:
        N1 = choice(all_non_singular_animate_nouns)
        N2 = choice(all_animate_nouns, [N1])
        V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N2, allow_negated=False)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1, N2])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "The %s have wondered whether the %s %s %s yet." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "The %s have wondered whether the %s  %s %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_3 = "The %s have wondered yet whether the %s %s %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "The %s have wondered %s whether the %s %s %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

    # build sentences with non-question environment
    sentence_5 = "The %s have said that the %s %s the %s yet." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "The %s have said that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_7 = "The %s have said yet that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "The %s have said %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
        # sentences 1-4 have question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=yet-crucial_item=whether-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of yet

# repeat for at all

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  N3 at all
    # Ann   wonders  whether  James  ate  apples at all
    try:
        N1 = choice(all_non_singular_animate_nouns)
        N2 = choice(all_animate_nouns, [N1])
        V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N2, allow_negated=False)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1, N2])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "The %s have wondered whether the %s %s %s at all." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "The %s have wondered whether the %s %s %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_3 = "The %s have wondered at all whether the %s %s %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "The %s have wondered %s whether the %s %s %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

    # build sentences with non-question environment
    sentence_5 = "The %s have said that the %s %s the %s at all." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "The %s have said that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_7 = "The %s have said at all that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "The %s have said %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
        # sentences 1-4 have question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-question environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=atall-crucial_item=whether-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of at all

# repeat for in years

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1  N3 in years
    # Ann   wonders  whether  James  ate  apples in years
    try:
        N1 = choice(all_non_singular_animate_nouns)
        N2 = choice(all_animate_nouns, [N1])
        V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N2, allow_negated=False)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1, N2])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "The %s have wondered whether the %s %s the %s in years." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "The %s have wondered whether the %s  %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_3 = "The %s have wondered in years whether the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "The %s have wondered %s whether the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

    # build sentences with non-question environment
    sentence_5 = "The %s have said that the %s %s  %s in years." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "The %s have said that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_7 = "The %s have said in years that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "The %s have said %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=inyears-crucial_item=whether-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of in years

# repeat for either

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # N1    wonders  whether   N2    V1   N3     either
    # Ann   wonders  whether  James  ate  apples either
    try:
        N1 = choice(all_non_singular_animate_nouns)
        N2 = choice(all_animate_nouns, [N1])
        V1 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N2, allow_negated=False)
        N3 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1, N2])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N2[0], V1[0])
        continue

    # build sentences with question environment
    sentence_1 = "The %s have wondered whether the %s %s the %s either." % (N1[0], N2[0], V1[0], N3[0])
    sentence_2 = "The %s have wondered whether the %s  %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_3 = "The %s have wondered either whether the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_4 = "The %s have wondered %s whether the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

    # build sentences with non-question environment
    sentence_5 = "The %s have said that the %s %s the %s either." % (N1[0], N2[0], V1[0], N3[0])
    sentence_6 = "The %s have said that the %s %s the %s %s." % (N1[0], N2[0], V1[0], N3[0], decoy)
    sentence_7 = "The %s have said either that the %s %s the %s." % (N1[0], N2[0], V1[0], N3[0])
    sentence_8 = "The %s have said %s that the %s %s the %s." % (N1[0], decoy, N2[0], V1[0], N3[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=1-scope=1-npi_present=1", 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=1-scope=0-npi_present=0", 1, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=either-crucial_item=whether-licensor=0-scope=0-npi_present=0", 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of either

output.close()

# add paradigm parameter to metadata
dataset_path = os.path.join(project_root, rel_output_path)
output_path = os.path.join(project_root, rel_output_path)
add_paradigm_feature(dataset_path, output_path)