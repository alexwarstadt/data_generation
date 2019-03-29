# Author: Alex Warstadt
# Script for generating Chomsky's "structure dependent" sentences for QP1
# Loosens some restrictions from polar_q so that complementizer + finite verb is not such a reliable cue

from utils.conjugate import *
from utils.constituent_building import verb_args_from_verb
from utils.constituent_building import N_to_DP_mutate
from utils.randomize import choice
import numpy as np
from utils.string_utils import string_beautify


# initialize output file
rel_output_path = "outputs/alexs_qp_structure_dependence/polar_q/10k"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
train_output = open(os.path.join(project_root, rel_output_path, "train.tsv"), "w")
test_output = open(os.path.join(project_root, rel_output_path, "test_full.tsv"), "w")
test2_output = open(os.path.join(project_root, rel_output_path, "test.tsv"), "w")
dev_output = open(os.path.join(project_root, rel_output_path, "dev.tsv"), "w")

# set total number of sentences to generate
number_to_generate = 10000
sentences = set()
counter = 0    # Jiant requires test data to be in numbered, two-column format

# gather word classes that will be accessed frequently

# all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])     # all subjects should agree in animacy/number
# all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])     # objects don't need to should be animate


all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_singular_nouns = get_all("sg", "0", all_nouns)
# all_frequent_quantifiers = get_all("frequent", "1", get_all("category", "(S/(S\\NP))/N"))


all_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0")])
# all_homophonous_participles = get_all("homophonous", "1", all_transitive_verbs)
# all_safe_verbs = np.setdiff1d(all_transitive_verbs, all_homophonous_participles)       # verbs that (a) require an aux and (b) don't have homophonous past/participle
all_safe_verbs = all_transitive_verbs
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

for writer in [train_output, dev_output, test_output]:
    counter = 0
    while counter < number_to_generate:
        # Aux1/2 D1  N1  who Aux1  V1    D2  N2  Aux2 V2      D3  N3
        # is/has the man who (has) met   the boy (is) kissing the patient ?

        # Aux1/2 D1  N1  Aux2 V2      D3  N3      who Aux2  V2    D2  N2
        # is/has the man (is) kissing the patient who (has) met   the boy ?

        # The arguments of V2 must match in animacy/number
        V2 = choice(all_consistent_transitive_verbs)
        # if V2["bare"] == "1":
            # if the verb is bare, it will be homophonous with the present plural, so avoid
        #     N1 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_1", all_singular_nouns)))
        # else:
        N1 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_1", all_nouns)))

        N3 = N_to_DP_mutate(choice(get_matched_by(V2, "arg_2", get_all_conjunctive([("animate", N1["animate"]), ("sg", N1["sg"])], all_nouns)), [N1]))

        try:
            if N3["sg"] == "0":
                # if N3 is plural, then V1 must not be bare
                    V1 = choice(get_matched_by(N3, "arg_1", all_non_bare_verbs))
            else:
                V1 = choice(get_matched_by(N3, "arg_1", all_safe_verbs), [V2])

        except IndexError:
            print(V2[0], N1[0], N3[0])
            continue

        N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_nouns), [N1, N3]))
        Aux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_frontable_aux)))
        Aux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_frontable_aux)), [Aux1])
        Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))

        sentence_1 = "%s %s %s %s %s %s %s %s?" % (Aux2[0], N1[0], Rel[0], Aux1[0], V1[0], N2[0], V2[0], N3[0])
        sentence_2 = "%s %s %s %s %s %s %s %s?" % (Aux1[0], N1[0], Rel[0], V1[0], N2[0], Aux2[0], V2[0], N3[0])
        sentence_3 = "%s %s %s %s %s %s %s %s?" % (Aux2[0], N1[0], V2[0], N3[0], Rel[0], Aux1[0], V1[0], N2[0])
        sentence_4 = "%s %s %s %s %s %s %s %s?" % (Aux1[0], N1[0], Aux2[0], V2[0], N3[0], Rel[0], V1[0], N2[0])

        sentence_1 = string_beautify(sentence_1)
        sentence_2 = string_beautify(sentence_2)
        sentence_3 = string_beautify(sentence_3)
        sentence_4 = string_beautify(sentence_4)

        if sentence_1 not in sentences:
            if writer == test_output:
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=1-last=1-aux1=%s-aux2=%s" % (Aux1[0], Aux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=0-last=0-aux1=%s-aux2=%s" % (Aux1[0], Aux2[0]), 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=1-last=0-aux1=%s-aux2=%s" % (Aux1[0], Aux2[0]), 1, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=0-last=1-aux1=%s-aux2=%s" % (Aux1[0], Aux2[0]), 0, sentence_4))
                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
            else:
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=1-last=1-aux1=%s-aux2=%s" % (Aux1[0], Aux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=0-last=0-aux1=%s-aux2=%s" % (Aux1[0], Aux2[0]), 0, sentence_2))
                counter += 2
        sentences.add(sentence_1)


train_output.close()
test_output.close()
test2_output.close()
dev_output.close()



"""
Think more about the paradigm

1.  1   Has the teacher [who is] praising the essay criticized the student?
2.  0   Is the teacher [who praising] the essay has criticized the student?
3.  1   Has the teacher criticized the student [who is] praising the essay?
4.  0   Is the teacher has criticized the student [who praising] the essay? 


1.  1   Has the teacher who is praising the essay has criticized the student?
2.  0   Is the teacher who is praising the essay has criticized the student?
3.  1   Has the teacher has criticized the student who is praising the essay?
4.  0   Is the teacher has criticized the student who is praising the essay? 


Question: Does the model use the bigram of complementizer + finite verb to identify grammatical sentences?
- Response 1: If this were so we would expect to see incorrect classification on ungrammatical sentences with the same bigram
- Response 2: If we eliminate this as a reliable cue...
    1.  1   Has the teacher [who praising the essay criticized the student?
    2.  0   Is the teacher [who praising] the essay has criticized the student?
    3.  1   Has the teacher criticized the student [who is] praising the essay?
    4.  0   Is the teacher has criticized the student [who praising] the essay? 



"""



