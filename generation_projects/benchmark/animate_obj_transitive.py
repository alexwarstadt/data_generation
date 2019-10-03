from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from functools import reduce
from utils.vocab_sets import *


class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="s-selection",
                         uid="animate_obj_trans",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_inanim_obj_allowing_verbs = get_matched_by(choice(all_inanimate_nouns), "arg_2", all_transitive_verbs)
        self.all_anim_obj_allowing_verbs = get_matched_by(choice(all_animate_nouns), "arg_2", all_transitive_verbs)
        self.all_anim_obj_verbs = np.setdiff1d(self.all_anim_obj_allowing_verbs, self.all_inanim_obj_allowing_verbs)
        self.dets = ['the', 'some']

    def sample(self):
        # John talked to the boy
        # N1   V1        det N2_good
        # John talked to the book
        # N1   V1        det N2_bad

        V1 = choice(self.all_anim_obj_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
        except TypeError:
                pass
        N2_good = choice(get_all("animate", "1", all_common_nouns))
        N2_bad = choice(get_all("animate", "0", all_common_nouns))
        det = choice(self.dets)
        V1 = conjugate(V1, N1)

        data = {
            "sentence_good": "%s %s %s %s." % (N1[0], V1[0], det, N2_good[0]),
            "sentence_bad": "%s %s %s %s." % (N1[0], V1[0], det, N2_bad[0]),
            "one_prefix_prefix": "%s %s %s" % (N1[0], V1[0], det),
            "one_prefix_word_good": N2_good[0],
            "one_prefix_word_bad": N2_bad[0]
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
