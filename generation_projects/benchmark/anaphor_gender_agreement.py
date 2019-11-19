from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from functools import reduce
from utils.vocab_sets import *

class AnaphorGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(
            field="morphology",
            linguistics="anaphor_agreement",
            uid="anaphor_gender_agreement",
            simple_lm_method=True,
            one_prefix_method=True,
            two_prefix_method=False,
            lexically_identical=False
        )
        self.all_safe_nouns = np.setdiff1d(all_singular_nouns, all_singular_neuter_animate_nouns)
        self.all_singular_reflexives = reduce(np.union1d, (get_all("expression", "himself"),
                                                           get_all("expression", "herself"),
                                                           get_all("expression", "itself")))

    def sample(self):
        # John knows himself
        # N1   V1    refl_match
        # John knows itself
        # N1   V1    refl_mismatch

        V1 = choice(all_refl_preds)
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", get_matches_of(V1, "arg_2", self.all_safe_nouns))))
        refl_match = choice(get_matched_by(N1, "arg_1", all_reflexives))
        refl_mismatch = choice(np.setdiff1d(self.all_singular_reflexives, [refl_match]))

        V1 = conjugate(V1, N1)

        data = {
            "sentence_good": "%s %s %s." % (N1[0], V1[0], refl_match[0]),
            "sentence_bad": "%s %s %s." % (N1[0], V1[0], refl_mismatch[0]),
            "one_prefix_prefix": "%s %s" % (N1[0], V1[0]),
            "one_prefix_word_good": refl_match[0],
            "one_prefix_word_bad": refl_mismatch[0]
        }
        return data, data["sentence_good"]


binding_generator = AnaphorGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % binding_generator.uid)












