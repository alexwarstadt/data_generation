# Authors: Alex Warstadt
# Script for generating NPI sentences with quantifiers as licensors

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import random
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=questions.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_intransitive_verbs = get_all("category", "S\\NP")
all_nouns = get_all("category", "N")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))
all_embedding_verbs = get_all_conjunctive([("category_2","V_embedding"),("finite","1")])
all_wh_verbs = get_all_conjunctive([("category_2","V_wh"),("finite","1")])

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1      V1      whether    D2  N2      ever    V2   N3
    # The   teacher wonders whether    the child   ever    ate  apples

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    V1_wh = choice(get_matched_by(N1, "arg_1", all_wh_verbs))
    V1_decl = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
    N2 = choice(all_animate_nouns)
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))

    # select transitive or intransitive V1
    x = random.random()
    if x < 1/2:
        # transitive V1
        V2 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    else:
        # intransitive V1 - gives empty string for N3 slot
        V2 = choice(get_matched_by(N2, "arg_1", all_intransitive_verbs))
        N3 = " "

    # build sentences with conditional environment
    sentence_1 = "%s %s %s whether %s %s ever %s %s." % (D1[0], N1[0], V1_wh[0], D2[0], N2[0], V2[0], N3[0])
    sentence_2 = "%s %s %s whether %s %s never %s %s." % (D1[0], N1[0], V1_wh[0], D2[0], N2[0], V2[0], N3[0])
    sentence_3 = "%s %s %s ever whether %s %s %s %s." % (D1[0], N1[0], V1_wh[0], D2[0], N2[0], V2[0], N3[0])
    sentence_4 = "%s %s %s never whether %s %s %s %s." % (D1[0], N1[0], V1_wh[0], D2[0], N2[0], V2[0], N3[0])

    # build sentences with conditional-like environment
    sentence_5 = "%s %s %s that %s %s ever %s %s." % (D1[0], N1[0], V1_decl[0], D2[0], N2[0], V2[0], N3[0])
    sentence_6 = "%s %s %s that %s %s never %s %s." % (D1[0], N1[0], V1_decl[0], D2[0], N2[0], V2[0], N3[0])
    sentence_7 = "%s %s %s ever that %s %s %s %s." % (D1[0], N1[0], V1_decl[0], D2[0], N2[0], V2[0], N3[0])
    sentence_8 = "%s %s %s never that %s %s %s %s." % (D1[0], N1[0], V1_decl[0], D2[0], N2[0], V2[0], N3[0])

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
        # sentences 1-4 have conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=1-scope=1-npi_present=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=1-scope=1-npi_present=0", 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=1-scope=0-npi_present=1", 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=1-scope=0-npi_present=0", 0, sentence_4))
        # sentences 5-8 have non-conditional environment
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=0-scope=1-npi_present=1", 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=0-scope=1-npi_present=0", 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=0-scope=0-npi_present=1", 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=questions-npi=ever-licensor=0-scope=0-npi_present=0", 0, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)
# the end :)

output.close()