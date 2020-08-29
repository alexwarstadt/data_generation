# Author: Alex Warstadt
# Script for generating Chomsky's "structure dependent" sentences for QP1
# Loosens some restrictions from polar_q so that complementizer + finite verb is not such a reliable cue

from utils.conjugate import *
from utils.constituent_building import verb_args_from_verb
from utils.constituent_building import N_to_DP_mutate
from utils.randomize import choice
import numpy as np
from utils.string_utils import string_beautify
import pattern
from pattern.en import PAST, SG, PL


# initialize output file
rel_output_path = "outputs/structure_dependence_qp/matrix_tense/10k/"
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

all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
# all_singular_nouns = get_all("sg", "0", all_nouns)
all_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP")])
# all_safe_verbs = all_transitive_verbs
all_pres_verbs = get_all("pres", "1", all_transitive_verbs)
all_past_pres_verbs = get_all("finite", "1", all_transitive_verbs)
all_aux = get_all("category", "(S\\NP)/(S[bare]\\NP)") #TODO: don't worry about frontable aux
animate_noun = choice(get_all("animate", "1"))
inanimate_noun = choice(get_all("animate", "0"))
all_consistent_transitive_verbs = np.union1d(
    get_matched_by(animate_noun, "arg_1", get_matched_by(animate_noun, "arg_2", all_pres_verbs)),
    get_matched_by(inanimate_noun, "arg_1", get_matched_by(inanimate_noun, "arg_2", all_pres_verbs))
)

pass

# all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1", get_matched_by(choice(all_animate_nouns), "arg_2", all_transitive_verbs))
# TODO: think about predicates that don't care about animacy (is adjacent to)

# sample sentences until desired number


def past(verb, sg):
    number = SG if sg == 1 else PL
    words = verb[0].split(" ")
    words[0] = pattern.en.conjugate(words[0], tense=PAST, number=number)
    return " ".join(words)

test2_output.write("metadata\tjudgment\t\tsentence")
for writer in [train_output, dev_output, test_output]:
    counter = 0
    while counter < number_to_generate:
        # The man who went/goes to France hugs/hugged the woman.
        # N1      Rel V1/V2      N2       V3          N3

        # The man is   hugging the woman who might goes/went to France .
        # N1      Aux3 V3      N3        Rel Aux1  V1   V2      N3

        try:
            V3 = choice(all_past_pres_verbs)
            N1 = N_to_DP_mutate(choice(get_matches_of(V3, "arg_1", all_nouns)))
            N3 = N_to_DP_mutate(choice(get_matches_of(V3, "arg_2", get_all_conjunctive([("animate", N1["animate"]), ("sg", N1["sg"])], all_nouns)), [N1]))
            V1 = choice(get_matched_by(N1, "arg_1", all_pres_verbs), [V3])
            V2 = get_all_conjunctive([("expression", past(V1, N1["sg"])), ("past", "1")])[0]
            N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_nouns), [N1, N3]))
            Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))
        except IndexError:
            continue

        sentence_1 = "%s %s %s %s %s %s." % (N1[0], Rel[0], V2[0], N2[0], V3[0], N3[0])
        sentence_2 = "%s %s %s %s %s %s." % (N1[0], Rel[0], V1[0], N2[0], V3[0], N3[0])
        sentence_3 = "%s %s %s %s %s %s." % (N1[0], V3[0], N3[0], Rel[0], V2[0], N2[0])
        sentence_4 = "%s %s %s %s %s %s." % (N1[0], V3[0], N3[0], Rel[0], V1[0], N2[0])

        sentence_1 = string_beautify(sentence_1)
        sentence_2 = string_beautify(sentence_2)
        sentence_3 = string_beautify(sentence_3)
        sentence_4 = string_beautify(sentence_4)

        if sentence_1 not in sentences:
            if writer == test_output:
                #TODO!!
                writer.write("%s\t%d\t\t%s\n" % ("exp=matrix_tense-src=1-emb_past=1-first_past=1-matrix_v=%s-emb_v=%s" % (V3[0], V2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=matrix_tense-src=1-emb_past=0-first_past=0-matrix_v=%s-emb_v=%s" % (V3[0], V1[0]), 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("exp=matrix_tense-src=0-emb_past=1-first_past=0-matrix_v=%s-emb_v=%s" % (V2[0], V3[0]), 1, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("exp=matrix_tense-src=0-emb_past=0-first_past=0-matrix_v=%s-emb_v=%s" % (V1[0], V3[0]), 0, sentence_4))

                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
            else:
                writer.write("%s\t%d\t\t%s\n" % ("exp=matrix_tense-src=1-emb_past=1-first_past=1-matrix_v=%s-emb_v=%s" % (V3[0], V2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=matrix_tense-src=1-emb_past=0-first_past=0-matrix_v=%s-emb_v=%s" % (V3[0], V1[0]), 0, sentence_2))
                counter += 2
        sentences.add(sentence_1)


train_output.close()
test_output.close()
test2_output.close()
dev_output.close()


