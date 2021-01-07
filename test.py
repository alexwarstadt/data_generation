import utils.vocab_table_db
import utils.vocab_sets_db
import utils.randomize
from utils.constituent_building import *

all_ing_transitives = utils.vocab_sets_db.all_transitive_verbs \
                      + utils.vocab_sets_db.all_ing_verbs

V_mat = utils.randomize.choice(utils.vocab_table_db.get_all_conjunctive(utils.vocab_sets_db.all_non_finite_transitive_verbs))
print(V_mat)
Subj = N_to_DP_mutate(choice(utils.vocab_table_db.get_matches_of(V_mat, "arg_1", utils.vocab_sets_db.all_nouns)))
Aux_mat = return_aux(V_mat, Subj, allow_negated=False)
Obj = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_2", utils.vocab_sets_db.all_nouns)))
query = get_matched_by(Obj, "arg_2", get_matched_by(Subj, "arg_1", all_ing_transitives))




# from utils.randomize import choice
#
# from utils.vocab_table import *
# import utils.vocab_table_db
#
# import utils.vocab_sets
# import utils.vocab_sets_db

# selection = utils.vocab_sets.all_refl_preds
# spec = utils.vocab_sets_db.all_non_plural_transitive_verbs
# selection_db = utils.vocab_table_db.get_all_unlike(spec)
#
# v_tbl = set([x[0] for x in selection])
# v_tbl_db = set([x[0] for x in selection_db])

# for s in v_tbl:
#     print(s)

# print("vocab_sets query returned {} results.".format(len(selection)))
# print("vocab_sets_db query returned {} results.".format(len(selection_db)))
# print("Set difference v_tbl - v_tbl_db:", v_tbl - set())
# print("Set difference v_tbl_db - v_tbl:", set() - v_tbl)


