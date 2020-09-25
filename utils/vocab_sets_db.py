
# NOUNS
all_nouns = [("category", "N"), ("frequent", "1")]
all_singular_nouns = [("sg", "1")] + all_nouns
all_singular_count_nouns = [("mass", "0")] + all_singular_nouns
all_animate_nouns = [("animate", "1")] + all_nouns
all_inanimate_nouns = [("animate", "0")] + all_nouns
all_documents = [("category", "N"), ("document", "1")]
all_gendered_nouns = (("gender", "m"), ("gender", "f")) # get_union
all_singular_neuter_animate_nouns = [("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")]
all_plural_nouns = [("category", "N"), ("frequent", "1"), ("pl", "1")]
all_plural_animate_nouns = all_animate_nouns + [("pl", "1")]
all_common_nouns = [("category", "N"), ("properNoun", "0")]
all_relational_nouns = [("category", "N/NP")]
all_nominals = [[("noun", "1"), ("frequent", "1")]]
all_relational_poss_nouns = [("category", "N\\NP[poss]")]
all_proper_names = [("properNoun", "1")]

# VERBS
all_verbs = [("verb", "1")]
all_transitive_verbs = [("category", "(S\\NP)/NP")]
all_intransitive_verbs = [("category", "S\\NP")]
all_non_recursive_verbs = (all_transitive_verbs[0], all_intransitive_verbs[0])
all_finite_verbs = [("finite", "1")] + all_verbs
all_non_finite_verbs = [("finite", "0")] + all_verbs
all_ing_verbs = [("ing", "1")] + all_verbs
all_en_verbs = [("en", "1")] + all_verbs
all_bare_verbs = [("bare", "1")] + all_verbs
# TODO: Work on complex conjuncts of get_matched_by
# all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1",
#                                           get_matched_by(choice(all_animate_nouns), "arg_2",
#                                                          all_transitive_verbs))
# all_doc_doc_verbs = get_matched_by(choice(all_documents), "arg_1",
#                                         get_matched_by(choice(all_documents), "arg_2", all_transitive_verbs))
all_refl_nonverbal_predicates = [("category_2", "Pred")]
# TODO: work on this reduce thingy
# all_refl_preds = reduce(np.union1d, (all_anim_anim_verbs, all_doc_doc_verbs))
all_non_plural_transitive_verbs = (all_transitive_verbs, [("arg_1", "sg=0"), ("arg_1", "pl=1")]) # get_all_unlike
all_strictly_plural_verbs = [("pres", "1"), ("sg3", "0")] + all_verbs
all_strictly_singular_verbs = [("pres", "1"), ("sg3", "1")] + all_verbs
all_strictly_plural_transitive_verbs = all_strictly_plural_verbs + all_transitive_verbs
all_strictly_singular_transitive_verbs = all_strictly_singular_verbs + all_transitive_verbs
all_possibly_plural_verbs = (all_verbs, [("sg3", "1")])
all_possibly_singular_verbs = (all_verbs, [("sg3", "0")])
all_non_finite_transitive_verbs = all_non_finite_verbs + [("category", "(S\\NP)/NP")]
all_non_finite_intransitive_verbs = [("finite", "0")] + all_intransitive_verbs
all_modals_auxs = [("category", "(S\\NP)/(S[bare]\\NP)")]
all_modals = [("category_2", "modal")]
all_auxs = [("category_2", "aux")]
all_negated_modals_auxs = [("negated", "1")] + all_modals_auxs
all_non_negated_modals_auxs = [("negated", "0")] + all_modals_auxs
all_negated_modals = [("negated", "1")] + all_modals
all_non_negated_modals = [("negated", "0")] + all_modals
all_negated_auxs = [("negated", "1")] + all_auxs
all_non_negated_auxs = [("negated", "0")] + all_auxs

all_copulas = [("category_2", "copula")]
all_finite_copulas = (all_copulas, [("bare", "1")]) # get_all_except
all_rogatives = [("category", "(S\\NP)/Q")]

all_agreeing_aux = (all_auxs, [("arg_1", "sg=1;sg=0")]) # get_all_except
all_non_negative_agreeing_aux = (all_auxs + [("negated", "0")], [("arg_1", "sg=1;sg=0")]) # get_all_except
all_negative_agreeing_aux = (all_auxs + [("negated", "1")], [("arg_1", "sg=1;sg=0")]) # get_all_except
all_auxiliaries_no_null = (all_auxs, [("expression", "")]) # get_all_except
all_non_negative_copulas = (all_copulas + [("negated", "0")], [("bare", "1")]) # get_all_except
all_negative_copulas = (all_copulas + [("negated", "1")], [("bare", "1")])

# OTHER
all_determiners = [("category", "(S/(S\\NP))/N")]
all_frequent_determiners = [("frequent", "1", all_determiners)]
# TODO FIX THIS by adding a query that takes in a complex disjunction
all_very_common_dets = [("expression", "the"), ("expression", "a"), ("expression", "an")]

all_relativizers = [("category_2", "rel")]
all_reflexives = [("category_2", "refl")]
all_ACCpronouns = [("category_2", "proACC")]
all_NOMpronouns = [("category_2", "proNOM")]
all_embedding_verbs = [("category_2", "V_embedding")]
all_wh_words = [("category", "NP_wh")]
all_demonstratives = [("quantifier", "0"), ("restrictor_DE", "")]
all_adjectives = (("category_2", "adjective"), ("category_2", "Adj"))
all_frequent = [("frequent", "1")]
