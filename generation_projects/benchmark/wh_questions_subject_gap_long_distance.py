from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from utils.vocab_sets import *


class FillerGapGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="filler_gap_dependency",
                         uid="wh_questions_subject_gap_long_distance",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.embedding_verbs = get_all("category", "(S\\NP)/S")

    def sample(self):
        # John noticed the man that Bill knows that saw everyone.
        # N1   V1          N2  that N4   V3    that V2  N3

        # John noticed who the man that Bill knows saw everyone.
        # N1   V1      wh      N2  that N4   V3    V2  N3

        V1 = choice(all_transitive_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
            N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_common_nouns)))
        except TypeError:
            pass
        V2 = choice(get_matched_by(N2, "arg_1", all_transitive_verbs))
        try:
            N3 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_2", all_common_nouns)))
        except TypeError:
            pass

        V1 = conjugate(V1, N1)
        V2 = conjugate(V2, N2)

        wh = choice(get_matched_by(N3, "arg_1", all_wh_words))

        V3 = choice(get_matched_by(N2, "arg_2", all_transitive_verbs))
        try:
            N4 = N_to_DP_mutate(choice(get_matches_of(V3, "arg_1", all_nouns)))
        except TypeError:
            pass

        V3 = conjugate(V3, N4)

        data = {
            "sentence_good": "%s %s %s that %s %s that %s %s." % (N1[0], V1[0], N2[0], N4[0], V3[0], V2[0], N3[0]),
            "sentence_bad": "%s %s %s %s that %s %s %s %s." % (N1[0], V1[0], wh[0], N2[0], N4[0], V3[0], V2[0], N3[0])
        }
        return data, data["sentence_good"]

generator = FillerGapGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
