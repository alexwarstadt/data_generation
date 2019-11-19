from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="island_effects",
                         uid="wh_island",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.responsive_verbs = get_all("responsive", "1", all_non_finite_verbs)
        self.pronouns = get_all("category_2", "proNOM")

    def sample(self):
        # What do      you  know  he  had     bought?
        # Wh1  Aux_mat Subj V_mat Pro Aux_emb V_emb
        # What do      you  know  who had     bought?
        # Wh1  Aux_mat Subj V_mat Wh2 Aux_emb V_emb

        V_mat = choice(self.responsive_verbs)
        Subj = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_1", all_nouns)))
        Aux_mat = return_aux(V_mat, Subj)
        V_emb = choice(all_transitive_verbs)
        Pro = choice(get_matches_of(V_emb, "arg_1", get_matched_by(Subj, "arg_1", self.pronouns)))
        Wh1 = choice(get_matches_of(V_emb, "arg_2", all_wh_words))
        Wh2 = choice(get_matches_of(V_emb, "arg_1", all_wh_words))
        Aux_emb = return_aux(V_emb, Pro)

        data = {
            "sentence_good": "%s %s %s %s %s %s %s?" % (Wh1[0], Aux_mat[0], Subj[0], V_mat[0], Pro[0], Aux_emb[0], V_emb[0]),
            "sentence_bad": "%s %s %s %s %s %s %s?" % (Wh1[0], Aux_mat[0], Subj[0], V_mat[0], Wh2[0], Aux_emb[0], V_emb[0]),
            "one_prefix_prefix": "%s %s %s %s" % (Wh1[0], Aux_mat[0], Subj[0], V_mat[0]),
            "one_prefix_word_good": Pro[0],
            "one_prefix_word_bad": Wh2[0]
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

