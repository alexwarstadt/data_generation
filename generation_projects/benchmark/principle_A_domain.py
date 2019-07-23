from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


class BindingGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="agreement",
                         field="syntax/semantics",
                         linguistics="binding",
                         uid="principle_A_domain",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_safe_nouns = np.setdiff1d(self.all_nouns, self.all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, self.all_common_nouns)

    def sample(self):
        # John thinks Mary saw      him.
        # N1   V1     N2   Vembed   pro_match

        # John thinks  Mary saw     himself.
        # N1   V1      N2   Vembed  refl_match

        V1 = choice(self.all_embedding_verbs)
        Vembed = choice(self.all_refl_preds)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_nouns)))
        except IndexError:
            pass
        refl_match = choice(get_matched_by(N1, "arg_1", self.all_reflexives))
        pro_match = choice(get_matched_by(N1, "arg_1", self.all_ACCpronouns))
        try:
            N2 = choice(get_matches_of(Vembed, "arg_1", self.all_safe_nouns))
        except TypeError:
            pass
        while is_match_disj(N2, refl_match["arg_1"]):
            N2 = choice(get_matches_of(Vembed, "arg_1", self.all_safe_nouns))
        N2 = N_to_DP_mutate(N2)

        V1 = conjugate(V1, N1)
        Vembed = conjugate(Vembed, N2)

        data = {
            "sentence_good": "%s %s %s %s %s." % (N1[0], V1[0], N2[0], Vembed[0], pro_match[0]),
            "sentence_bad": "%s %s %s %s %s." % (N1[0], V1[0], N2[0], Vembed[0], refl_match[0]),
            "one_prefix_prefix": "%s %s %s %s" % (N1[0], V1[0], N2[0], Vembed[0]),
            "one_prefix_word_good": pro_match[0],
            "one_prefix_word_bad": refl_match[0]
        }
        return data, data["sentence_good"]

binding_generator = BindingGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % binding_generator.uid)
