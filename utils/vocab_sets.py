from utils.vocab_table import *
from utils.randomize import *
from functools import reduce

# NOUNS
all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_singular_nouns = get_all("sg", "1", all_nouns)
all_singular_count_nouns = get_all("mass", "0", all_singular_nouns)
all_animate_nouns = get_all("animate", "1", all_nouns)
all_documents = get_all_conjunctive([("category", "N"), ("document", "1")])
all_gendered_nouns = np.union1d(get_all("gender", "m"), get_all("gender", "f"))
all_singular_neuter_animate_nouns = get_all_conjunctive(
    [("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
all_plural_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1"), ("pl", "1")])
all_plural_animate_nouns = np.intersect1d(all_animate_nouns, all_plural_nouns)
all_common_nouns = get_all_conjunctive([("category", "N"), ("properNoun", "0")])
all_relational_nouns = get_all("category", "N/NP")
all_nominals = get_all("noun", "1")
all_relational_poss_nouns = get_all("category", "N\\NP[poss]")
all_proper_names = get_all("properNoun", "1")

# VERBS
all_verbs = get_all("verb", "1")
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_intransitive_verbs = get_all("category", "S\\NP")
all_non_finite_verbs = get_all("finite", "0", all_verbs)
all_ing_verbs = get_all("ing", "1", all_verbs)
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
all_plural_transitive_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "0")], all_transitive_verbs)
all_singular_transitive_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "1")], all_transitive_verbs)
all_non_finite_transitive_verbs = np.intersect1d(all_non_finite_verbs, all_transitive_verbs)
all_non_finite_intransitive_verbs = get_all("finite", "0", all_intransitive_verbs)

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
