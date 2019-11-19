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
                         linguistics="argument_structure",
                         uid="animate_subject_passive",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_inanim_subj_allowing_verbs = get_matched_by(choice(all_inanimate_nouns), "arg_1", all_transitive_verbs)
        self.all_anim_subj_allowing_verbs = get_matched_by(choice(all_animate_nouns), "arg_1", all_transitive_verbs)
        self.all_anim_subj_verbs = np.setdiff1d(self.all_anim_subj_allowing_verbs, self.all_inanim_subj_allowing_verbs)
        self.dets = ['the', 'some']
        self.location_nouns = get_all("locale", "1")
        self.nonlocation_commonnouns = np.setdiff1d(all_common_nouns, self.location_nouns)

    def sample(self):
        # The boy was talked to by the woman
        # N1      cop V1        by det N2_good
        # The boy was talked to by the car
        # N1      cop V1        by det N2_bad

        V1 = choice(get_all('en', '1', self.all_anim_subj_verbs))

        N1 = N_to_DP_mutate(choice(get_matches_of(V1, 'arg_2', all_nouns)))
        cop = return_copula(N1)
        det = choice(self.dets)
        N2_good = choice(get_all("animate", "1", get_matched_by(V1, "arg_1", all_common_nouns)))
        N2_bad = choice(get_all("animate", "0", self.nonlocation_commonnouns))

        data = {
            "sentence_good": "%s %s %s by %s %s." % (N1[0], cop[0], V1[0], det, N2_good[0]),
            "sentence_bad": "%s %s %s by %s %s." % (N1[0], cop[0], V1[0], det, N2_bad[0]),
            "one_prefix_prefix": "%s %s %s by %s" % (N1[0], cop[0], V1[0], det),
            "one_prefix_word_good": N2_good[0],
            "one_prefix_word_bad": N2_bad[0]
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
