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
                         uid="animate_obj_passive",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        self.all_inanim_obj_allowing_verbs = get_matched_by(choice(all_inanimate_nouns), "arg_2", all_transitive_verbs)
        self.all_anim_obj_allowing_verbs = get_matched_by(choice(all_animate_nouns), "arg_2", all_transitive_verbs)
        self.all_anim_obj_verbs = np.setdiff1d(self.all_anim_obj_allowing_verbs, self.all_inanim_obj_allowing_verbs)

    def sample(self):
        # The boy was talked to
        # N1_good cop V1
        # The book was talked to
        # N1_bad   cop V1

        V1 = choice(get_all('en', '1', self.all_anim_obj_verbs))
        N1_good = N_to_DP_mutate(choice(get_all("animate", "1", all_common_nouns)))
        N1_bad = N_to_DP_mutate(choice(get_all("animate", "0", all_common_nouns)))
        cop1 = return_copula(N1_good)
        cop2 = return_copula(N1_bad)

        data = {
            "sentence_good": "%s %s %s." % (N1_good[0], cop1[0], V1[0]),
            "sentence_bad": "%s %s %s." % (N1_bad[0], cop2[0], V1[0]),
            "two_prefix_prefix_good": "%s %s" % (N1_good[0], cop1[0]),
            "two_prefix_prefix_bad": "%s %s" % (N1_bad[0], cop2[0]),
            "two_prefix_word": V1[0]
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
