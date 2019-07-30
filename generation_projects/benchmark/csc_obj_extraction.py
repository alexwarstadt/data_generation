from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from utils.vocab_sets import *


class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="movement",
                         field="syntax",
                         linguistics="island_effects",
                         uid="csc_obj_extraction",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=True)
        self.all_safe_nouns = np.setdiff1d(all_nouns, all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, all_common_nouns)

    def sample(self):
        # What did  John and Mary help?
        # wh   V_do N1   and N2   V1

        # What did  John help and Mary?
        # wh   V_do N1   V1   and N2

        V1 = choice(all_non_finite_transitive_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
        except TypeError:
            pass
        V_do = return_aux(V1, N1, allow_negated=False)
        try:
            N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
        except TypeError:
            pass
        wh = choice(get_matched_by(V1, "arg_2", all_wh_words))

        data = {
            "sentence_good": "%s %s %s and %s %s?" % (wh[0], V_do[0], N1[0], N2[0], V1[0]),
            "sentence_bad": "%s %s %s %s and %s?" % (wh[0], V_do[0], N1[0], V1[0], N2[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
