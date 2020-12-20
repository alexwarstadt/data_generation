from utils.vocab_table import *
from utils.randomize import *
from functools import reduce
import numpy as np

VOCAB_SETS = {}

# =================================================
#                    NOUNS
# =================================================

def get_all_nouns():
    if "all_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_nouns"] = get_all_conjunctive([("category", "N"), ("frequent", "1")])
    return VOCAB_SETS["all_nouns"]

def get_all_singular_nouns():
    if "all_singular_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_singular_nouns"] = get_all("sg", "1", get_all_nouns())
    return VOCAB_SETS["all_singular_nouns"]

def get_all_singular_count_nouns():
    if "all_singular_count_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_singular_count_nouns"] = get_all("mass", "0", get_all_singular_nouns())
    return VOCAB_SETS["all_singular_count_nouns"]

def get_all_animate_nouns():
    if "all_animate_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_animate_nouns"] = get_all("animate", "1", get_all_nouns())
    return VOCAB_SETS["all_animate_nouns"]

def get_all_inanimate_nouns():
    if "all_inanimate_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_inanimate_nouns"] = get_all("animate", "0", get_all_nouns())
    return VOCAB_SETS["all_inanimate_nouns"]

def get_all_documents():
    if "all_documents" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_documents"] = get_all_conjunctive([("category", "N"), ("document", "1")])
    return VOCAB_SETS["all_documents"]

def get_all_gendered_nouns():
    if "all_gendered_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_gendered_nouns"] = np.union1d(get_all("gender", "m"), get_all("gender", "f"))
    return VOCAB_SETS["all_gendered_nouns"]

def get_all_singular_neuter_animate_nouns():
    if "all_singular_neuter_animate_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_singular_neuter_animate_nouns"] = get_all_conjunctive([("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
    return VOCAB_SETS["all_singular_neuter_animate_nouns"]

def get_all_plural_nouns():
    if "all_plural_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_plural_nouns"] = get_all_conjunctive([("category", "N"), ("frequent", "1"), ("pl", "1")])
    return VOCAB_SETS["all_plural_nouns"]

def get_all_plural_animate_nouns():
    if "all_plural_animate_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_plural_animate_nouns"] = np.intersect1d(get_all_animate_nouns(), get_all_plural_nouns())
    return VOCAB_SETS["all_plural_animate_nouns"]

def get_all_common_nouns():
    if "all_common_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_common_nouns"] = get_all_conjunctive([("category", "N"), ("properNoun", "0")])
    return VOCAB_SETS["all_common_nouns"]

def get_all_relational_nouns():
    if "all_relational_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_relational_nouns"] = get_all("category", "N/NP")
    return VOCAB_SETS["all_relational_nouns"]

def get_all_nominals():
    if "all_nominals" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_nominals"] = get_all_conjunctive([("noun", "1"), ("frequent", "1")])
    return VOCAB_SETS["all_nominals"]

def get_all_relational_poss_nouns():
    if "all_relational_poss_nouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_relational_poss_nouns"] = get_all("category", "N\\NP[poss]")
    return VOCAB_SETS["all_relational_poss_nouns"]

def get_all_proper_names():
    if "all_proper_names" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_proper_names"] = get_all("properNoun", "1")
    return VOCAB_SETS["all_proper_names"]

# =================================================
#                    VERBS
# =================================================

def get_all_verbs():
    if "all_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_verbs"] = get_all("verb", "1")
    return VOCAB_SETS["all_verbs"]

def get_all_transitive_verbs():
    if "all_transitive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_transitive_verbs"] = get_all("category", "(S\\NP)/NP")
    return VOCAB_SETS["all_transitive_verbs"]

def get_all_intransitive_verbs():
    if "all_intransitive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_intransitive_verbs"] = get_all("category", "S\\NP")
    return VOCAB_SETS["all_intransitive_verbs"]

def get_all_non_recursive_verbs():
    if "all_non_recursive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_recursive_verbs"] = np.union1d(get_all_transitive_verbs(), get_all_intransitive_verbs())
    return VOCAB_SETS["all_non_recursive_verbs"]

def get_all_CP_verbs():
    if "all_CP_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_CP_verbs"] = get_all("category", "(S\\NP)/S")
    return VOCAB_SETS["all_CP_verbs"]

def get_all_finite_verbs():
    if "all_finite_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_finite_verbs"] = get_all("finite", "1", get_all_verbs())
    return VOCAB_SETS["all_finite_verbs"]

def get_all_non_finite_verbs():
    if "all_non_finite_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_finite_verbs"] = get_all("finite", "0", get_all_verbs())
    return VOCAB_SETS["all_non_finite_verbs"]

def get_all_ing_verbs():
    if "all_ing_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_ing_verbs"] = get_all("ing", "1", get_all_verbs())
    return VOCAB_SETS["all_ing_verbs"]

def get_all_en_verbs():
    if "all_en_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_en_verbs"] = get_all("en", "1", get_all_verbs())
    return VOCAB_SETS["all_en_verbs"]

def get_all_bare_verbs():
    if "all_bare_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_bare_verbs"] = get_all("bare", "1", get_all_verbs())
    return VOCAB_SETS["all_bare_verbs"]

def get_all_anim_anim_verbs():
    if "all_anim_anim_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_anim_anim_verbs"] = get_matched_by(choice(get_all_animate_nouns()), "arg_1",
                                                           get_matched_by(choice(get_all_animate_nouns()), "arg_2",
                                                                          get_all_transitive_verbs()))
    return VOCAB_SETS["all_anim_anim_verbs"]

def get_all_doc_doc_verbs():
    if "all_doc_doc_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_doc_doc_verbs"] = get_matched_by(choice(get_all_documents()), "arg_1",
                                                         get_matched_by(choice(get_all_documents()), "arg_2",
                                                                        get_all_transitive_verbs()))
    return VOCAB_SETS["all_doc_doc_verbs"]

def get_all_refl_nonverbal_predicates():
    if "all_refl_nonverbal_predicates" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_refl_nonverbal_predicates"] = np.extract([x["arg_1"] == x["arg_2"] for x in
                                                                  get_all("category_2", "Pred")],
                                                                 get_all("category_2", "Pred"))
    return VOCAB_SETS["all_refl_nonverbal_predicates"]

def get_all_refl_preds():
    if "all_refl_preds" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_refl_preds"] = reduce(np.union1d, (get_all_anim_anim_verbs(), get_all_doc_doc_verbs()))
    return VOCAB_SETS["all_refl_preds"]

def get_all_non_plural_transitive_verbs():
    if "all_non_plural_transitive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_plural_transitive_verbs"] = np.extract(
            ["sg=0" not in x["arg_1"] and "pl=1" not in x["arg_1"] for x in get_all_transitive_verbs()],
            get_all_transitive_verbs())
    return VOCAB_SETS["all_non_plural_transitive_verbs"]

def get_all_strictly_plural_verbs():
    if "all_strictly_plural_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_strictly_plural_verbs"] = get_all_conjunctive([("pres", "1"), ("3sg", "0")], get_all_verbs())
    return VOCAB_SETS["all_strictly_plural_verbs"]

def get_all_strictly_singular_verbs():
    if "all_strictly_singular_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_strictly_singular_verbs"] = get_all_conjunctive([("pres", "1"), ("3sg", "1")], get_all_verbs())
    return VOCAB_SETS["all_strictly_singular_verbs"]

def get_all_strictly_plural_transitive_verbs():
    if "all_strictly_plural_transitive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_strictly_plural_transitive_verbs"] = np.intersect1d(get_all_strictly_plural_verbs(), get_all_transitive_verbs())
    return VOCAB_SETS["all_strictly_plural_transitive_verbs"]

def get_all_strictly_singular_transitive_verbs():
    if "all_strictly_singular_transitive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_strictly_singular_transitive_verbs"] = np.intersect1d(get_all_strictly_singular_verbs(), get_all_transitive_verbs())
    return VOCAB_SETS["all_strictly_singular_transitive_verbs"]

def get_all_possibly_plural_verbs():
    if "all_possibly_plural_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_possibly_plural_verbs"] = np.setdiff1d(get_all_verbs(), get_all_strictly_singular_verbs())
    return VOCAB_SETS["all_possibly_plural_verbs"]

def get_all_possibly_singular_verbs():
    if "all_possibly_singular_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_possibly_singular_verbs"] = np.setdiff1d(get_all_verbs(), get_all_strictly_plural_verbs())
    return VOCAB_SETS["all_possibly_singular_verbs"]

def get_all_present_plural_verbs():
    if "all_present_plural_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_present_plural_verbs"] = get_all_conjunctive([("pres", "1"), ("3sg", "0")])
    return VOCAB_SETS["all_present_plural_verbs"]

def get_all_non_finite_transitive_verbs():
    if "all_non_finite_transitive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_finite_transitive_verbs"] = np.intersect1d(get_all_non_finite_verbs(), get_all_transitive_verbs())
    return VOCAB_SETS["all_non_finite_transitive_verbs"]

def get_all_non_finite_intransitive_verbs():
    if "all_non_finite_intransitive_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_finite_intransitive_verbs"] = get_all("finite", "0", get_all_intransitive_verbs())
    return VOCAB_SETS["all_non_finite_intransitive_verbs"]

def get_all_modals_auxs():
    if "all_modals_auxs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_modals_auxs"] = get_all("category", "(S\\NP)/(S[bare]\\NP)")
    return VOCAB_SETS["all_modals_auxs"]

def get_all_modals():
    if "all_modals" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_modals"] = get_all("category_2", "modal")
    return VOCAB_SETS["all_modals"]

def get_all_auxs():
    if "all_auxs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_auxs"] = get_all("category_2", "aux")
    return VOCAB_SETS["all_auxs"]

def get_all_negated_modals_auxs():
    if "all_negated_modals_auxs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_negated_modals_auxs"] = get_all("negated", "1", get_all_modals_auxs())
    return VOCAB_SETS["all_negated_modals_auxs"]

def get_all_non_negated_modals_auxs():
    if "all_non_negated_modals_auxs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_negated_modals_auxs"] = get_all("negated", "0", get_all_modals_auxs())
    return VOCAB_SETS["all_non_negated_modals_auxs"]

def get_all_negated_modals():
    if "all_negated_modals" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_negated_modals"] = get_all("negated", "1", get_all_modals())
    return VOCAB_SETS["all_negated_modals"]

def get_all_non_negated_modals():
    if "all_non_negated_modals" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_negated_modals"] = get_all("negated", "0", get_all_modals())
    return VOCAB_SETS["all_non_negated_modals"]

def get_all_negated_auxs():
    if "all_negated_auxs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_negated_auxs"] = get_all("negated", "1", get_all_auxs())
    return VOCAB_SETS["all_negated_auxs"]

def get_all_non_negated_auxs():
    if "all_non_negated_auxs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_negated_auxs"] = get_all("negated", "0", get_all_auxs())
    return VOCAB_SETS["all_non_negated_auxs"]

def get_all_copulas():
    if "all_copulas" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_copulas"] = get_all("category_2", "copula")
    return VOCAB_SETS["all_copulas"]

def get_all_finite_copulas():
    if "all_finite_copulas" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_finite_copulas"] = np.setdiff1d(get_all_copulas(), get_all("bare", "1"))
    return VOCAB_SETS["all_finite_copulas"]

def get_all_rogatives():
    if "all_rogatives" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_rogatives"] = get_all("category", "(S\\NP)/Q")
    return VOCAB_SETS["all_rogatives"]

def get_all_agreeing_aux():
    if "all_agreeing_aux" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_agreeing_aux"] = np.setdiff1d(get_all_auxs(), get_all("arg_1", "sg=1;sg=0"))  #TODO: This needs to change if we change querying
    return VOCAB_SETS["all_agreeing_aux"]

def get_all_non_negative_agreeing_aux():
    if "all_non_negative_agreeing_aux" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_negative_agreeing_aux"] = get_all("negated", "0", get_all_agreeing_aux())
    return VOCAB_SETS["all_non_negative_agreeing_aux"]

def get_all_negative_agreeing_aux():
    if "all_negative_agreeing_aux" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_negative_agreeing_aux"] = get_all("negated", "1", get_all_agreeing_aux())
    return VOCAB_SETS["all_negative_agreeing_aux"]

def get_all_auxiliaries_no_null():
    if "all_auxiliaries_no_null" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_auxiliaries_no_null"] = np.setdiff1d(get_all_auxs(), get_all("expression", ""))
    return VOCAB_SETS["all_auxiliaries_no_null"]

def get_all_non_negative_auxiliaries_no_null():
    if "all_non_negative_auxiliaries_no_null" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_negative_auxiliaries_no_null"] = get_all("negated", "0", get_all_auxiliaries_no_null())
    return VOCAB_SETS["all_non_negative_auxiliaries_no_null"]

def get_all_negative_auxiliaries_no_null():
    if "all_negative_auxiliaries_no_null" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_negative_auxiliaries_no_null"] = get_all("negated", "1", get_all_auxiliaries_no_null())
    return VOCAB_SETS["all_negative_auxiliaries_no_null"]

def get_all_non_negative_copulas():
    if "all_non_negative_copulas" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_non_negative_copulas"] = get_all("negated", "0", get_all_finite_copulas())
    return VOCAB_SETS["all_non_negative_copulas"]

def get_all_negative_copulas():
    if "all_negative_copulas" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_negative_copulas"] = get_all("negated", "1", get_all_finite_copulas())
    return VOCAB_SETS["all_negative_copulas"]

# =================================================
#                    OTHER
# =================================================

def get_all_determiners():
    if "all_determiners" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_determiners"] = get_all("category", "(S/(S\\NP))/N")
    return VOCAB_SETS["all_determiners"]

def get_all_frequent_determiners():
    if "all_frequent_determiners" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_frequent_determiners"] = get_all("frequent", "1", get_all_determiners())
    return VOCAB_SETS["all_frequent_determiners"]

def get_all_very_common_dets():
    if "all_very_common_dets" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_very_common_dets"] = np.append(get_all("expression", "", get_all_determiners()), np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an"))))
    return VOCAB_SETS["all_very_common_dets"]

def get_all_relativizers():
    if "all_relativizers" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_relativizers"] = get_all("category_2", "rel")
    return VOCAB_SETS["all_relativizers"]

def get_all_reflexives():
    if "all_reflexives" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_reflexives"] = get_all("category_2", "refl")
    return VOCAB_SETS["all_reflexives"]

def get_all_ACCpronouns():
    if "all_ACCpronouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_ACCpronouns"] = get_all("category_2", "proACC")
    return VOCAB_SETS["all_ACCpronouns"]

def get_all_NOMpronouns():
    if "all_NOMpronouns" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_NOMpronouns"] = get_all("category_2", "proNOM")
    return VOCAB_SETS["all_NOMpronouns"]

def get_all_embedding_verbs():
    if "all_embedding_verbs" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_embedding_verbs"] = get_all("category_2", "V_embedding")
    return VOCAB_SETS["all_embedding_verbs"]

def get_all_wh_words():
    if "all_wh_words" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_wh_words"] = get_all("category", "NP_wh")
    return VOCAB_SETS["all_wh_words"]

def get_all_demonstratives():
    if "all_demonstratives" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_demonstratives"] = np.append(get_all("expression", "this"),
                            np.append(get_all_conjunctive([("category_2", "D"), ("expression", "that")]),
                                    np.append(get_all("expression", "these"), get_all("expression", "those"))))
    return VOCAB_SETS["all_demonstratives"]

def get_all_adjectives():
    if "all_adjectives" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_adjectives"] = np.append(get_all("category_2", "adjective"), get_all("category_2", "Adj"))
    return VOCAB_SETS["all_adjectives"]

def get_all_frequent():
    if "all_frequent" not in VOCAB_SETS.keys():
        VOCAB_SETS["all_frequent"] = get_all("frequent", "1")
    return VOCAB_SETS["all_frequent"]
