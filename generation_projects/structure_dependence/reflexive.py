# Author: Alex Warstadt
# Script for generating structure dependent reflexive paradigm for QP1

from utils.vocab_table import *
from utils.constituent_building import *
from utils.conjugate import *
from random import choice
from utils.string_utils import remove_extra_whitespace


# initialize output file
rel_output_path = "outputs/structure_dependence/reflexive.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of sentences to generate
number_to_generate = 100
sentences = set()

# gather noun classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_inanimate_nouns = get_all_conjunctive([("category", "N"), ("animate", "0"), ("frequent", "1")])
all_documents = get_all_conjunctive([("category", "N"), ("document", "1")])
all_frequent_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_singular_neuter_animate_nouns = get_all_conjunctive([("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
all_singular_inanimate_nouns = get_all_conjunctive([("category", "N"), ("sg", "1"), ("animate", "0")])

# gather functional classes that will be accessed frequently
all_frequent_quantifiers = get_all("frequent", "1", get_all("category", "(S/(S\\NP))/N"))
all_reflexives = get_all("category_2", "refl")

# gather potentially reflexive predicates
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1", get_matched_by(choice(all_animate_nouns), "arg_2", all_transitive_verbs))
all_doc_doc_verbs = get_matched_by(choice(all_documents), "arg_1", get_matched_by(choice(all_documents), "arg_2", all_transitive_verbs))
all_refl_preds = np.union1d(all_anim_anim_verbs, all_doc_doc_verbs)
# all_predicates




# sample sentences until desired number
while len(sentences) < number_to_generate:
    # DP1       Rel V1   DP2     V2  Refl1/Refl2
    # The women who like the boy see themselves/himself

    # D1  N1    Rel V2  Refl1/Refl2        V1   D2  N2
    # The women who saw themselves/himself like the boy

    # Get two reflexives that don't collide
    Refl1 = choice(all_reflexives)
    # Refl2 =
    DP1 = choice(get_matches_of(Refl1, "arg_1", all_frequent_nouns))
    DP2 = DP1
    Refl2 = Refl1
    if Refl1["expression"] is "themselves":
        # "themselves" could accidentally be anteceded by neuter singular animate nouns (the doctor), so avoid
        while DP2 in all_singular_neuter_animate_nouns:
            DP2 = choice(all_frequent_nouns)
        Refl2 = get_matched_by(DP2, "arg_1", all_reflexives)
    else:
        Refl2 = Refl1
        while Refl2 == Refl1:
            Refl2 = choice(all_reflexives)
            DP2 = DP2
        DP2 = DP2





    V1 = choice(all_refl_preds)
    DP1 = choice(get_matches_of(V1, "arg_1", all_frequent_nouns))
    N_to_DP_mutate(DP1)
    Refl1 = get_reflexive(DP1)      # get_reflexive excludes singular "themselves"
    V2 = choice(get_matched_by(DP1, "arg_1", all_refl_preds))


    DP2 = DP1
    Refl2 = Refl1


    while Refl1 in get_matched_by(DP2, "arg_1", all_reflexives) or Refl2 in get_matched_by(DP1, "arg_1", all_reflexives):
        DP2 = choice(get_matches_of(V1, "arg_2", all_frequent_nouns))
        Refl2 = get_reflexive(DP2)
    N_to_DP_mutate(DP2)

    Refl2 = get_reflexive(DP2)       # get_reflexive excludes singular "themselves"

    Rel = choice(get_matched_by(DP1, "arg_1", get_all("category_2", "rel")))
    conjugate(V1, DP1)
    conjugate(V2, DP1)

    sentence_1 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], Refl1[0], V2[0], DP2[0])
    sentence_2 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], Refl2[0], V2[0], DP2[0])
    sentence_3 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], DP2[0], V2[0], Refl1[0])
    sentence_4 = "%s %s %s %s %s %s." % (DP1[0], Rel[0], V1[0], DP2[0], V2[0], Refl2[0])

    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)

    if sentence_1 not in sentences:
        output.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=0-matrix_antecedent=1-precede=1", 1, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=0-matrix_antecedent=1-precede=0", 0, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=1-matrix_antecedent=1-precede=1", 1, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("exp=reflexive-matrix_reflexive=1-matrix_antecedent=0-precede=1", 0, sentence_4))
    sentences.add(sentence_1)




