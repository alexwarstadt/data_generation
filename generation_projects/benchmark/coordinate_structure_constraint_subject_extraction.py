from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="island_effects",
                         uid="coordinate_structure_constraint_subject_extraction",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=True)

    def sample(self):
        # What and bananas did  you eat?
        # wh   and N2      V_do N1  V1

        # What did  you eat and bananas?
        # wh   V_do N1  V1  and N2

        V1 = choice(all_non_finite_transitive_verbs)
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
        V_do = return_aux(V1, N1, allow_negated=False)
        N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_nouns)))
        wh = choice(get_matched_by(N2, "arg_1", all_wh_words))

        data = {
            "sentence_good": "%s and %s %s %s %s?" % (wh[0], N2[0], V_do[0], N1[0], V1[0]),
            "sentence_bad": "%s %s %s %s and %s?" % (wh[0], V_do[0], N1[0], V1[0], N2[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
