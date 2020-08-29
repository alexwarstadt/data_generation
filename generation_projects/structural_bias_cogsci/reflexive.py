# Author: Alex Warstadt
# Script for generating structure dependent reflexive paradigm for QP1

from utils.vocab_table import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


# initialize output file
rel_output_path = "data/reflexive"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
train_output = open(os.path.join(project_root, rel_output_path, "train.tsv"), "w")
test_output = open(os.path.join(project_root, rel_output_path, "test_full.tsv"), "w")
test2_output = open(os.path.join(project_root, rel_output_path, "test.tsv"), "w")
dev_output = open(os.path.join(project_root, rel_output_path, "dev.tsv"), "w")

# set total number of sentences to generate
number_to_generate = 10000
sentences = set()
counter = 0    # Jiant requires test data to be in numbered, two-column format


# gather noun classes that will be accessed frequently
all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_documents = get_all_conjunctive([("category", "N"), ("document", "1")])
all_singular_neuter_animate_nouns = get_all_conjunctive([("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
all_safe_nouns = np.setdiff1d(all_nouns, all_singular_neuter_animate_nouns)



# gather functional classes that will be accessed frequently
all_frequent_quantifiers = get_all("frequent", "1", get_all("category", "(S/(S\\NP))/N"))
all_reflexives = get_all("category_2", "refl")

# gather potentially reflexive predicates
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1", get_matched_by(choice(all_animate_nouns), "arg_2", all_transitive_verbs))
all_doc_doc_verbs = get_matched_by(choice(all_documents), "arg_1", get_matched_by(choice(all_documents), "arg_2", all_transitive_verbs))
all_refl_preds = np.union1d(all_anim_anim_verbs, all_doc_doc_verbs)




# sample sentences until desired number
for writer in [train_output, dev_output, test_output]:
    counter = 0
    while counter < number_to_generate:
        # DP1       Rel V1   DP2     V2  Refl1/Refl2
        # The women who like the boy see themselves/himself

        # D1  N1    Rel V2  Refl1/Refl2        V1   D2  N2
        # The women who saw themselves/himself like the boy

        V1 = choice(all_refl_preds)

        DP1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_safe_nouns)))
        Refl1 = choice(get_matched_by(DP1, "arg_1", all_reflexives))

        V2 = choice(get_matched_by(DP1, "arg_1", all_refl_preds), [V1])
        DP2 = DP1
        while is_match_disj(DP2, Refl1["arg_1"]):
            DP2 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_2", all_safe_nouns)))
        Refl2 = choice(get_matched_by(DP2, "arg_1", all_reflexives))

        V1 = conjugate(V1, DP1)
        V2 = conjugate(V2, DP1)

        Rel = choice(get_matched_by(DP1, "arg_1", get_all("category_2", "rel")))

        sentence_1 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], Refl1[0], V2[0], DP2[0])
        sentence_2 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], Refl2[0], V2[0], DP2[0])
        sentence_3 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], DP2[0], V2[0], Refl1[0])
        sentence_4 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], DP2[0], V2[0], Refl2[0])

        sentence_1 = string_beautify(sentence_1)
        sentence_2 = string_beautify(sentence_2)
        sentence_3 = string_beautify(sentence_3)
        sentence_4 = string_beautify(sentence_4)

        if sentence_1 not in sentences:
            if writer == test_output:
                writer.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=0-matrix_antecedent=1-refl1=%s-refl2=%s-precede=1" % (Refl1[0], Refl2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=0-matrix_antecedent=1-refl1=%s-refl2=%s-precede=0" % (Refl1[0], Refl2[0]), 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=1-matrix_antecedent=1-refl1=%s-refl2=%s-precede=1" % (Refl1[0], Refl2[0]), 1, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=1-matrix_antecedent=0-refl1=%s-refl2=%s-precede=1" % (Refl1[0], Refl2[0]), 0, sentence_4))
                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
            else:
                writer.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=0-matrix_antecedent=1-refl1=%s-refl2=%s-precede=1" % (Refl1[0], Refl2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=0-matrix_antecedent=1-refl1=%s-refl2=%s-precede=0" % (Refl1[0], Refl2[0]), 0, sentence_2))
                counter += 2

            # keep track of which sentences have already been generated
            sentences.add(sentence_1)

train_output.close()
test_output.close()
test2_output.close()
dev_output.close()



