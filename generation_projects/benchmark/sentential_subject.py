from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class SentSubjGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="island_effects",
                         uid="sentential_subject_island",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=True)
        self.all_safe_nouns = np.setdiff1d(all_nouns, all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, all_common_nouns)
        self.all_transitive_ing_verbs = get_all_conjunctive([("ing", "1")], all_transitive_verbs)
        self.all_inanim_anim_nonfinite_transitive_verbs = get_matched_by(choice(all_inanimate_nouns), "arg_1",
                                                  get_matched_by(choice(all_animate_nouns), "arg_2",
                                                                 all_non_finite_transitive_verbs))

    def sample(self):
        # Who did  Bill's  calling the president annoy?
        # wh  V_do N1_poss Ving        N2        V2
        # Who did  Bill's  calling annoy the president?
        # wh  V_do N1_poss Ving    V2        N2

        Ving = choice(self.all_transitive_ing_verbs)
        N1_poss = N_to_DP_mutate(choice(get_matches_of(Ving, "arg_1", self.all_safe_common_nouns)))
        if N1_poss['pl'] == "1" and N1_poss['irrpl'] != "1":
            N1_poss[0] = N1_poss[0]+"'"
        else:
            N1_poss[0] = N1_poss[0]+"'s"
        V2 = choice(self.all_inanim_anim_nonfinite_transitive_verbs)
        V_do = return_aux(V2, N1_poss, allow_negated=False)
        N2 = N_to_DP_mutate(choice(get_matches_of(Ving, "arg_2", get_matches_of(V2, "arg_2", self.all_safe_nouns))))
        wh = choice(get_matches_of(V2, "arg_2", all_wh_words))

        data = {
            "sentence_good": "%s %s %s %s %s %s." % (wh[0], V_do[0], N1_poss[0], Ving[0], N2[0], V2[0]),
            "sentence_bad": "%s %s %s %s %s %s." % (wh[0], V_do[0], N1_poss[0], Ving[0], V2[0], N2[0]),
        }
        return data, data["sentence_good"]

generator = SentSubjGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
