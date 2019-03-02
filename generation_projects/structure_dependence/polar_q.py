# Author: Alex Warstadt
# Script for generating Chomsky's "structure dependent" sentences for QP1

from utils.vocab_table import *
from utils.conjugate import *
from random import choice
from utils.string_utils import remove_extra_whitespace


# initialize output file
output = open("../../outputs/structure_dependence/polar_q.tsv", "w")

# set total number of sentences to generate
number_to_generate = 1000
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1")])
all_common_quantifiers = get_all("common", "1", get_all("category", "(S/(S\\NP))/N"))
all_transitive_verbs = get_all("arg_1", "animate=1", get_all("category", "(S\\NP)/NP"))
all_frontable_aux = get_all("frontable", "1")

all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1", get_matched_by(choice(all_animate_nouns), "arg_2", all_transitive_verbs))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # Aux1/2 D1  N1  who Aux1  V1    D2  N2  Aux2 V2      D3  N3
    # is/has the man who (has) met   the boy (is) kissing the patient?
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_quantifiers))
    N2 = choice(all_animate_nouns)
    D2 = choice(get_matched_by(N2, "arg_1", all_common_quantifiers))
    N3 = choice(all_animate_nouns)
    D3 = choice(get_matched_by(N3, "arg_1", all_common_quantifiers))
    Aux1 = choice(get_matched_by(N1, "arg_2", all_frontable_aux))   #TODO: worry about participles that are homophones with past
    V1 = choice(get_matches_of(Aux1, "arg_1", all_anim_anim_verbs))
    Aux2 = choice(get_matched_by(N1, "arg_2", all_frontable_aux))   #TODO: worry about participles that are homophones with past
    V2 = choice(get_matches_of(Aux2, "arg_1", all_anim_anim_verbs))

    sentence_1 = "%s %s %s who %s %s %s %s %s %s %s ?" % (Aux2[0], D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s %s who %s %s %s %s %s %s %s ?" % (Aux1[0], D1[0], N1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)

    if sentence_1 not in sentences:
        output.write("%s\t%d\t\t%s\n" % ("exp=polar_src=1_highest=1_last=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("exp=polar_src=1_highest=0_last=0", 0, sentence_2))
    sentences.add(sentence_1)
    # print(sentence_1)



    # Aux1/2 D1  N1  who Aux1  V1    D2  N2    Aux2 V2      D3  N3
    # is/has the man who (has) eaten the apple (is) opening the jar?

output.close()