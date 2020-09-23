
# NOUNS
all_nouns = [("category", "N"), ("frequent", "1")]
all_singular_nouns = [("sg", "1")] + all_nouns
all_singular_count_nouns = [("mass", "0")] + all_singular_nouns
all_animate_nouns = [("animate", "1")] + all_nouns
all_inanimate_nouns = [("animate", "0")] + all_nouns
all_documents = [("category", "N"), ("document", "1")]
# TODO: figure out how to represent unions. There are only two usages of 'all_gendered_nouns' so perhaps I could
#  just write some sort of custom query in vocab_table_db to handle disjunctive things like Union
#  all_gendered_nouns = np.union1d(get_all("gender", "m"), get_all("gender", "f"))
all_singular_neuter_animate_nouns = [("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")]
all_plural_nouns = [("category", "N"), ("frequent", "1"), ("pl", "1")]
# TODO: also, work on figuring out this intersection thingy over here too.
#  Note, there are actually no calls to this category, so this is NOT high priority.
#  all_plural_animate_nouns = np.intersect1d(all_animate_nouns, all_plural_nouns)
all_common_nouns = [("category", "N"), ("properNoun", "0")]
all_relational_nouns = [("category", "N/NP")]
all_nominals = [[("noun", "1"), ("frequent", "1")]]
all_relational_poss_nouns = [("category", "N\\NP[poss]")]
all_proper_names = [("properNoun", "1")]

# VERBS
all_verbs = [("verb", "1")]
all_transitive_verbs = [("category", "(S\\NP)/NP")]
all_intransitive_verbs = [("category", "S\\NP")]
# TODO: this is the same as the above. Make a query that can handle unions and also possibly intersections.
#  all_non_recursive_verbs = np.union1d(all_transitive_verbs, all_intransitive_verbs)
all_finite_verbs = [("finite", "1")] + all_verbs
all_non_finite_verbs = [("finite", "0")] +  all_verbs
all_ing_verbs = ["ing", "1"] + all_verbs
all_en_verbs = [("en", "1")] + all_verbs
all_bare_verbs = [("bare", "1")] + all_verbs
# TODO: Work on complex conjuncts of get_matched_by
# all_anim_anim_verbs = get_matched_by(choice(all_animate_nouns), "arg_1",
#                                           get_matched_by(choice(all_animate_nouns), "arg_2",
#                                                          all_transitive_verbs))
# all_doc_doc_verbs = get_matched_by(choice(all_documents), "arg_1",
#                                         get_matched_by(choice(all_documents), "arg_2", all_transitive_verbs))
# TODO: work on this np.extract thingy
# all_refl_nonverbal_predicates = np.extract([x["arg_1"] == x["arg_2"] for x in get_all("category_2", "Pred")],
#                                                 get_all("category_2", "Pred"))
# TODO: work on this reduce thingy
# all_refl_preds = reduce(np.union1d, (all_anim_anim_verbs, all_doc_doc_verbs))
# TODO: Work on this extract thingy
# all_non_plural_transitive_verbs = np.extract(
#     ["sg=0" not in x["arg_1"] and "pl=1" not in x["arg_1"] for x in all_transitive_verbs],
#     all_transitive_verbs)
all_strictly_plural_verbs = [("pres", "1"), ("sg3", "0")] + all_verbs
all_strictly_singular_verbs = [("pres", "1"), ("sg3", "1")] + all_verbs
# TODO: Work on all of these other functions that either make calls to intersection or to set difference
# all_strictly_plural_transitive_verbs = np.intersect1d(all_strictly_plural_verbs, all_transitive_verbs)
# all_strictly_singular_transitive_verbs = np.intersect1d(all_strictly_singular_verbs, all_transitive_verbs)
# all_possibly_plural_verbs = np.setdiff1d(all_verbs, all_strictly_singular_verbs)
# all_possibly_singular_verbs = np.setdiff1d(all_verbs, all_strictly_plural_verbs)
# all_non_finite_transitive_verbs = np.intersect1d(all_non_finite_verbs, all_transitive_verbs)
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
# TODO: set difference
# all_finite_copulas = np.setdiff1d(all_copulas, get_all("bare", "1"))
all_rogatives = [("category", "(S\\NP)/Q")]

# TODO set difference
# all_agreeing_aux = np.setdiff1d(all_auxs, get_all("arg_1", "sg=1;sg=0"))
all_non_negative_agreeing_aux = [("negated", "0")] + all_agreeing_aux
all_negative_agreeing_aux = [("negated", "1")] + all_agreeing_aux
# TODO set difference
# all_auxiliaries_no_null = np.setdiff1d(all_auxs, get_all("expression", ""))
all_non_negative_copulas = [("negated", "0")] + all_finite_copulas
all_negative_copulas = [("negated", "1")] + all_finite_copulas