from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="movement",
                         field="syntax",
                         linguistics="island_effects",
                         uid="csc_complex_left_branch",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.all_D_wh = get_all("category_2", "D_wh")
        self.which_what = np.append(get_all_conjunctive([("expression", "which")], self.all_D_wh), get_all_conjunctive([("expression", "what")], self.all_D_wh))

    def sample(self):
        # What pie did  John cook and Mary eat?
        # wh   N3  V_do N1   V1   and N2   V2

        # What did  John cook pie and Mary eat?
        # wh   V_do N1   V1   N3  and N2   V2

        V1 = choice(self.all_non_finite_transitive_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_nouns)))
        except TypeError:
            pass
        V_do = return_aux(V1, N1, allow_negated=False)
        try:
            N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_nouns)))
        except TypeError:
            pass
        V2 = choice(get_matched_by(N2, "arg_1", self.all_non_finite_transitive_verbs))
        while is_match_disj(V2, V1["arg_2"]):
            V2 = choice(get_matched_by(N2, "arg_1", self.all_non_finite_transitive_verbs))
        N3 = choice(get_matches_of(V1, "arg_2", self.all_common_nouns))
        if N3['animate'] == "1":
            wh = choice(self.which_what)
        else:
            wh = choice(self.all_D_wh)

        data = {
            "sentence_good": "%s %s %s %s %s and %s %s?" % (wh[0], N3[0], V_do[0], N1[0], V1[0], N2[0], V2[0]),
            "sentence_bad": "%s %s %s %s %s and %s %s?" % (wh[0], V_do[0], N1[0], V1[0], N3[0], N2[0], V2[0]),
            "two_prefix_prefix_good": "%s %s %s %s %s and %s" % (wh[0], N3[0], V_do[0], N1[0], V1[0], N2[0]),
            "two_prefix_prefix_bad": "%s %s %s %s %s and %s" % (wh[0], V_do[0], N1[0], V1[0], N3[0], N2[0]),
            "two_prefix_word": V2[0]
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
