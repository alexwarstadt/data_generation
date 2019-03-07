# Author: Alex Warstadt
# Script for generating structure dependent reflexive paradigm for QP1

from utils.vocab_table import *
from utils.conjugate import *
from random import choice
from utils.string_utils import remove_extra_whitespace


# initialize output file
output = open("../../outputs/structure_dependence/reflexive.tsv", "w")

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
    # D1  N1    who Aux1     V1   D2  N2  Aux2   V2  Refl1/Refl2
    # The women who (should) like the boy (will) see herself/himself
    # The woman who saw himself/herself likes the boy

    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_quantifiers))
    N2 = choice(all_animate_nouns)
    D2 = choice(get_matched_by(N2, "arg_1", all_common_quantifiers))
    N3 = choice(all_animate_nouns)
    D3 = choice(get_matched_by(N3, "arg_1", all_common_quantifiers))
    Aux1 = choice(get_matched_by(N1, "arg_1", all_frontable_aux))   #TODO: worry about participles that are homophones with past
    V1 = choice(get_matches_of(Aux1, "arg_2", all_anim_anim_verbs))
    Aux2 = choice(get_matched_by(N1, "arg_1", all_frontable_aux))   #TODO: worry about participles that are homophones with past
    V2 = choice(get_matches_of(Aux2, "arg_2", all_anim_anim_verbs))

    sentence_1 = "%s %s %s who %s %s %s %s %s %s %s ?" % (Aux2[0], D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s %s who %s %s %s %s %s %s %s ?" % (Aux1[0], D1[0], N1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s %s %s %s %s who %s %s %s %s ?" % (Aux1[0], D1[0], N1[0], V1[0], D3[0], N3[0], Aux2[0], V2[0], D2[0], N2[0])
    sentence_4 = "%s %s %s %s %s %s %s who %s %s %s ?" % (Aux2[0], D1[0], N1[0], Aux1[0], V1[0], D3[0], N3[0], V2[0], D2[0], N2[0])
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)

    if sentence_1 not in sentences:
        output.write("%s\t%d\t\t%s\n" % ("exp=polar_src=1_highest=1_last=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("exp=polar_src=1_highest=0_last=0", 0, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("exp=polar_src=0_highest=1_last=0", 1, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("exp=polar_src=0_highest=0_last=1", 0, sentence_4))
    sentences.add(sentence_1)




