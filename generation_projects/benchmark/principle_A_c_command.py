from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class BindingGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="binding",
                         uid="principle_A_c_command",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_safe_nouns = np.setdiff1d(all_nouns, all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, all_common_nouns)

    def sample(self):
        # The woman who defeated John saw herself.
        # N1        C1  Vembed   N2   V1  refl_match
        # The woman who defeated John saw himself.
        # N1        C1  Vembed   N2   V1  refl_mismatch

        V1 = choice(all_refl_preds)
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_common_nouns)))
        refl_match = choice(get_matched_by(N1, "arg_1", all_reflexives))
        C1 = choice(get_matched_by(N1, "arg_1", all_relativizers))
        Vembed = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        N2 = choice(get_matches_of(Vembed, "arg_2", self.all_safe_nouns))
        while is_match_disj(N2, refl_match["arg_1"]):
            N2 = choice(get_matches_of(Vembed, "arg_2", self.all_safe_nouns))
        N2 = N_to_DP_mutate(N2)
        refl_mismatch = choice(get_matched_by(N2, "arg_1", all_reflexives))
        V1 = conjugate(V1, N1)
        Vembed = conjugate(Vembed, N1)

        data = {
            "sentence_good": "%s %s %s %s %s %s." % (N1[0], C1[0], Vembed[0], N2[0], V1[0], refl_match[0]),
            "sentence_bad": "%s %s %s %s %s %s." % (N1[0], C1[0], Vembed[0], N2[0], V1[0], refl_mismatch[0]),
            "one_prefix_prefix": "%s %s %s %s %s" % (N1[0], C1[0], Vembed[0], N2[0], V1[0]),
            "one_prefix_word_good": refl_match[0],
            "one_prefix_word_bad": refl_mismatch[0]
        }
        return data, data["sentence_good"]

binding_generator = BindingGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % binding_generator.uid)

