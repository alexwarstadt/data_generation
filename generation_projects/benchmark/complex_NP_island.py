from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="island_effects",
                         uid="complex_NP_island",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=True)

        self.predicates = np.union1d(all_refl_preds, get_all("category_2", "Adj_comp_than"))
        self.safe_subjs = np.setdiff1d(all_nominals, all_proper_names)

    def sample(self):
        # Who did     the man that        helped John see?
        # wh  Aux_mat Subj    Rel  Aux_emb V_emb  Obj  V_mat
        # Who did     John see   the man that         helped?
        # wh  Aux_mat Obj  V_mat Subj    Rel  Aux_emb V_emb

        V_mat = choice(get_all("finite", "0", self.predicates))
        Subj = N_to_DP_mutate(choice(
            get_matches_of(V_mat, "arg_2",
                           get_matches_of(V_mat, "arg_1", self.safe_subjs))))
        Aux_mat = return_aux(V_mat, Subj)
        V_emb = choice(get_matched_by(Subj, "arg_1", self.predicates))
        Aux_emb = return_aux(V_emb, Subj)
        Obj = N_to_DP_mutate(choice(
            get_matches_of(V_emb, "arg_2",
                           get_matches_of(V_mat, "arg_1",
                                          get_matches_of(Aux_mat, "arg_1", all_nominals)))))
        Wh = choice(get_matches_of(V_mat, "arg_2",
                                   get_matches_of(V_emb, "arg_2", all_wh_words)))
        Rel = choice(get_matched_by(Subj, "arg_1", all_relativizers))

        data = {
            "sentence_good": "%s %s %s %s %s %s %s %s?" % (Wh[0], Aux_mat[0], Subj[0], Rel[0], Aux_emb[0], V_emb[0], Obj[0], V_mat[0]),
            "sentence_bad": "%s %s %s %s %s %s %s %s?" % (Wh[0], Aux_mat[0], Obj[0], V_mat[0], Subj[0], Rel[0], Aux_emb[0], V_emb[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

