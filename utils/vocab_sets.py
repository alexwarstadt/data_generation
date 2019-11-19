from utils.vocab_table import *
from utils.randomize import *
from functools import reduce
import numpy as np

#

# NOUNS
all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_singular_nouns = get_all("sg", "1", all_nouns)
all_singular_count_nouns = get_all("mass", "0", all_singular_nouns)
all_animate_nouns = get_all("animate", "1", all_nouns)
all_inanimate_nouns = get_all("animate", "0", all_nouns)
all_documents = get_all_conjunctive([("category", "N"), ("document", "1")])
all_gendered_nouns = np.union1d(get_all("gender", "m"), get_all("gender", "f"))
all_singular_neuter_animate_nouns = get_all_conjunctive(
    [("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
all_plural_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1"), ("pl", "1")])
all_plural_animate_nouns = np.intersect1d(all_animate_nouns, all_plural_nouns)
all_common_nouns = get_all_conjunctive([("category", "N"), ("properNoun", "0")])
all_relational_nouns = get_all("category", "N/NP")
all_nominals = get_all_conjunctive([("noun", "1"), ("frequent", "1")])
all_relational_poss_nouns = get_all("category", "N\\NP[poss]")
all_proper_names = get_all("properNoun", "1")

# VERBS
all_verbs = get_all("verb", "1")
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_intransitive_verbs = get_all("category", "S\\NP")
all_non_recursive_verbs = np.union1d(all_transitive_verbs, all_intransitive_verbs)
all_finite_verbs = get_all("finite", "1", all_verbs)
all_non_finite_verbs = get_all("finite", "0", all_verbs)
all_ing_verbs = get_all("ing", "1", all_verbs)
all_en_verbs = get_all("en", "1", all_verbs)
all_bare_verbs = get_all("bare", "1", all_verbs)
all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1",
                                          get_matched_by(choice(all_animate_nouns), "arg_2",
                                                         all_transitive_verbs))
all_doc_doc_verbs = get_matched_by(choice(all_documents), "arg_1",
                                        get_matched_by(choice(all_documents), "arg_2", all_transitive_verbs))
all_refl_nonverbal_predicates = np.extract([x["arg_1"] == x["arg_2"] for x in get_all("category_2", "Pred")],
                                                get_all("category_2", "Pred"))
all_refl_preds = reduce(np.union1d, (all_anim_anim_verbs, all_doc_doc_verbs))
all_non_plural_transitive_verbs = np.extract(
    ["sg=0" not in x["arg_1"] and "pl=1" not in x["arg_1"] for x in all_transitive_verbs],
    all_transitive_verbs)
all_strictly_plural_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "0")], all_verbs)
all_strictly_singular_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "1")], all_verbs)
all_strictly_plural_transitive_verbs = np.intersect1d(all_strictly_plural_verbs, all_transitive_verbs)
all_strictly_singular_transitive_verbs = np.intersect1d(all_strictly_singular_verbs, all_transitive_verbs)
all_possibly_plural_verbs = np.setdiff1d(all_verbs, all_strictly_singular_verbs)
all_possibly_singular_verbs = np.setdiff1d(all_verbs, all_strictly_plural_verbs)
all_non_finite_transitive_verbs = np.intersect1d(all_non_finite_verbs, all_transitive_verbs)
all_non_finite_intransitive_verbs = get_all("finite", "0", all_intransitive_verbs)
all_modals_auxs = get_all("category", "(S\\NP)/(S[bare]\\NP)")
all_modals = get_all("category_2", "modal")
all_auxs = get_all("category_2", "aux")
all_negated_modals_auxs = get_all("negated", "1", all_modals_auxs)
all_non_negated_modals_auxs = get_all("negated", "0", all_modals_auxs)
all_negated_modals = get_all("negated", "1", all_modals)
all_non_negated_modals = get_all("negated", "0", all_modals)
all_negated_auxs = get_all("negated", "1", all_auxs)
all_non_negated_auxs = get_all("negated", "0", all_auxs)

all_copulas = get_all("category_2", "copula")
all_finite_copulas = np.setdiff1d(all_copulas, get_all("bare", "1"))
all_rogatives = get_all("category", "(S\\NP)/Q")


all_agreeing_aux = np.setdiff1d(all_auxs, get_all("arg_1", "sg=1;sg=0"))
all_non_negative_agreeing_aux = get_all("negated", "0", all_agreeing_aux)
all_negative_agreeing_aux = get_all("negated", "1", all_agreeing_aux)
all_auxiliaries_no_null = np.setdiff1d(all_auxs, get_all("expression", ""))
all_non_negative_copulas = get_all("negated", "0", all_finite_copulas)
all_negative_copulas = get_all("negated", "1", all_finite_copulas)

# OTHER
all_quantifiers = get_all("category", "(S/(S\\NP))/N")
all_frequent_quantifiers = get_all("frequent", "1", all_quantifiers)
all_quantifiers = get_all("category", "(S/(S\\NP))/N")
all_common_dets = np.append(get_all("expression", "the"),
                            np.append(get_all("expression", "a"), get_all("expression", "an")))
all_relativizers = get_all("category_2", "rel")
all_reflexives = get_all("category_2", "refl")
all_ACCpronouns = get_all("category_2", "proACC")
all_NOMpronouns = get_all("category_2", "proNOM")
all_embedding_verbs = get_all("category_2", "V_embedding")
all_wh_words = get_all("category", "NP_wh")
all_demonstratives = np.append(get_all("expression", "this"),
                            np.append(get_all_conjunctive([("category_2", "D"),("expression", "that")]),
                                    np.append(get_all("expression", "these"), get_all("expression", "those"))))
all_adjectives = np.append(get_all("category_2", "adjective"), get_all("category_2", "Adj"))
all_frequent = get_all("frequent", "1")