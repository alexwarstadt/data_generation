from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class BindingGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="binding",
                         uid="principle_A_case_1",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_safe_nouns = np.setdiff1d(all_nouns, all_singular_neuter_animate_nouns)

    def sample(self):
        # John thinks he            saw     Mary
        # N1   V1     pro_match     Vembed  N2
        # John thinks  himself      saw     Mary
        # N1   V1      refl_match   Vembed  N2

        V1 = choice(all_embedding_verbs)
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_nouns)))
        Vembed = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        refl_match = choice(get_matched_by(N1, "arg_1", all_reflexives))
        pro_match = choice(get_matched_by(N1, "arg_1", all_NOMpronouns))
        N2 = N_to_DP_mutate(choice(get_matches_of(Vembed, "arg_2", all_nouns)))
        V1 = conjugate(V1, N1)
        Vembed = conjugate(Vembed, N1)

        data = {
            "sentence_good": "%s %s that %s %s %s." % (N1[0], V1[0], pro_match[0], Vembed[0], N2[0]),
            "sentence_bad": "%s %s that %s %s %s." % (N1[0], V1[0], refl_match[0], Vembed[0], N2[0]),
            "one_prefix_prefix": "%s %s that" % (N1[0], V1[0]),
            "one_prefix_word_good": pro_match[0],
            "one_prefix_word_bad": refl_match[0]
        }
        return data, data["sentence_good"]

binding_generator = BindingGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % binding_generator.uid)
