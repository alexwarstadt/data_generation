from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets_dynamic import *

class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="island_effects",
                         uid="adjunct_island",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=True)

        self.all_ing_transitives = np.intersect1d(get_all_transitive_verbs(), get_all_ing_verbs())
        self.adverbs = ["before", "while", "after", "without"]

    def sample(self):
        # What did      John read  before filing the book?
        # Wh   Aux_mat  Subj V_mat ADV    V_emb  Obj
        # What did      John read  the book before filing?
        # Wh   Aux_mat  Subj V_mat Obj      ADV    V_emb

        V_mat = choice(get_all_non_finite_transitive_verbs())
        Subj = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_1", get_all_nouns())))
        Aux_mat = return_aux(V_mat, Subj, allow_negated=False)
        Obj = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_2", get_all_nouns())))
        V_emb = choice(get_matched_by(Obj, "arg_2", get_matched_by(Subj, "arg_1", self.all_ing_transitives)))
        Wh = choice(get_matched_by(Obj, "arg_1", get_all_wh_words()))
        Adv = choice(self.adverbs)

        data = {
            "sentence_good": "%s %s %s %s %s %s %s?" % (Wh[0], Aux_mat[0], Subj[0], V_mat[0], Adv, V_emb[0], Obj[0]),
            "sentence_bad": "%s %s %s %s %s %s %s?" % (Wh[0], Aux_mat[0], Subj[0], V_mat[0], Obj[0], Adv, V_emb[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/examples/%s.jsonl" % generator.uid)

