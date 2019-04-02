# Author: Alex Warstadt
# Script for generating Chomsky's "structure dependent" sentences for QP1

from utils.conjugate import *
from utils.constituent_building import verb_args_from_verb
from utils.constituent_building import N_to_DP_mutate
from random import choice
import numpy as np
from utils.string_utils import string_beautify


# initialize output file
rel_output_path = "outputs/structure_dependence/polar_q/"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
train_output = open(os.path.join(project_root, rel_output_path, "train.tsv"), "w")
test_output = open(os.path.join(project_root, rel_output_path, "test_full.tsv"), "w")
test2_output = open(os.path.join(project_root, rel_output_path, "test.tsv"), "w")
dev_output = open(os.path.join(project_root, rel_output_path, "dev.tsv"), "w")

# set total number of sentences to generate
number_to_generate = 1000
sentences = set()
test_counter = 0    # Jiant requires test data to be in numbered, two-column format

# gather word classes that will be accessed frequently

# all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])     # all subjects should agree in animacy/number
# all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])     # objects don't need to should be animate


all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_singular_nouns = get_all("sg", "0", all_nouns)
# all_frequent_quantifiers = get_all("frequent", "1", get_all("category", "(S/(S\\NP))/N"))


all_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0")])
all_homophonous_participles = get_all("homophonous", "1", all_transitive_verbs)
all_safe_verbs = np.setdiff1d(all_transitive_verbs, all_homophonous_participles)       # verbs that (a) require an aux and (b) don't have homophonous past/participle
all_non_bare_verbs = get_all("bare", "0", all_safe_verbs)

all_frontable_aux = get_all("frontable", "1") #TODO: don't worry about frontable aux



animate_noun = choice(get_all("animate", "1"))
inanimate_noun = choice(get_all("animate", "0"))
all_consistent_transitive_verbs = np.union1d(
    get_matched_by(animate_noun, "arg_1", get_matched_by(animate_noun, "arg_2", all_safe_verbs)),
    get_matched_by(inanimate_noun, "arg_1", get_matched_by(inanimate_noun, "arg_2", all_safe_verbs))
)





# all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1", get_matched_by(choice(all_animate_nouns), "arg_2", all_transitive_verbs))
# TODO: think about predicates that don't care about animacy (is adjacent to)

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # Aux1/2 D1  N1  who Aux1  V1    D2  N2  Aux2 V2      D3  N3
    # is/has the man who (has) met   the boy (is) kissing the patient ?

    # Aux1/2 D1  N1  Aux2 V2      D3  N3      who Aux2  V2    D2  N2
    # is/has the man (is) kissing the patient who (has) met   the boy ?

    # The arguments of V2 must match in animacy/number
    V2 = choice(all_consistent_transitive_verbs)
    if V2["bare"] == "1":
        # if the verb is bare, it will be homophonous with the present plural, so avoid
        N1 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_1", all_singular_nouns)))
    else:
        N1 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_1", all_nouns)))

    N3 = N_to_DP_mutate(choice(get_matched_by(V2, "arg_2", get_all_conjunctive([("animate", N1["animate"]), ("sg", N1["sg"])], all_nouns))))

    if N3["sg"] == "0":
        # if N3 is plural, then V1 must not be bare
        try:
            V1 = choice(get_matched_by(N3, "arg_1", all_non_bare_verbs))
        except IndexError:
            print(V2[0], N1[0], N3[0])
            continue
    else:
        V1 = choice(get_matched_by(N3, "arg_1", all_safe_verbs))

    N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_nouns)))
    Aux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_frontable_aux)))
    Aux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_frontable_aux)))
    Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))

    sentence_1 = "%s %s %s %s %s %s %s %s?" % (Aux2[0], N1[0], Rel[0], Aux1[0], V1[0], N2[0], V2[0], N3[0])
    sentence_2 = "%s %s %s %s %s %s %s %s?" % (Aux1[0], N1[0], Rel[0], V1[0], N2[0], Aux2[0], V2[0], N3[0])
    sentence_3 = "%s %s %s %s %s %s %s %s?" % (Aux2[0], N1[0], V2[0], N3[0], Rel[0], Aux1[0], V1[0], N2[0])
    sentence_4 = "%s %s %s %s %s %s %s %s?" % (Aux1[0], N1[0], Aux2[0], V2[0], N3[0], Rel[0], V1[0], N2[0])

    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)

    in_domain_writer = np.random.choice([train_output, dev_output, test_output], 1, p=[0.5, 0.25, 0.25])[0]
    out_of_domain_writer = np.random.choice([dev_output, test_output], 1)[0] \
        if in_domain_writer == train_output \
        else in_domain_writer
    paradigm_in_domain = 1 if in_domain_writer == train_output else 0


    if sentence_1 not in sentences:
        in_domain_writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=1-last=1-aux1=%s-aux2=%s-paradigm_in_domain=%d" % (Aux1[0], Aux2[0], paradigm_in_domain), 1, sentence_1))
        in_domain_writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=0-last=0-aux1=%s-aux2=%s-paradigm_in_domain=%d" % (Aux1[0], Aux2[0], paradigm_in_domain), 0, sentence_2))
        out_of_domain_writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=1-last=0-aux1=%s-aux2=%s-paradigm_in_domain=%d" % (Aux1[0], Aux2[0], paradigm_in_domain), 1, sentence_3))
        out_of_domain_writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=0-last=1-aux1=%s-aux2=%s-paradigm_in_domain=%d" % (Aux1[0], Aux2[0], paradigm_in_domain), 0, sentence_4))

    if in_domain_writer == test_output:
        test2_output.write("%d\t%s\n" % (test_counter, sentence_1))
        test_counter += 1
        test2_output.write("%d\t%s\n" % (test_counter, sentence_2))
        test_counter += 1

    if out_of_domain_writer == test_output:
        test2_output.write("%d\t%s\n" % (test_counter, sentence_3))
        test_counter += 1
        test2_output.write("%d\t%s\n" % (test_counter, sentence_4))
        test_counter += 1

    sentences.add(sentence_1)

train_output.close()
test_output.close()
test2_output.close()
dev_output.close()


