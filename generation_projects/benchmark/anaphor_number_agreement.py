from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from functools import reduce
from utils.vocab_sets import *

class AnaphorGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="morphology",
                         linguistics="anaphor_agreement",
                         uid="anaphor_number_agreement",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=True)
        self.all_safe_singular_nouns = np.setdiff1d(all_singular_nouns, all_singular_neuter_animate_nouns)
        self.all_safe_plural_nouns = np.setdiff1d(all_plural_nouns, all_singular_neuter_animate_nouns)

        self.all_singular_reflexive_predicates = np.setdiff1d(all_refl_preds, all_strictly_plural_transitive_verbs)
        self.all_plural_reflexive_predicates = np.setdiff1d(all_refl_preds, all_strictly_singular_transitive_verbs)
        self.all_singular_reflexives = reduce(np.union1d, (get_all("expression", "himself"),
                                                           get_all("expression", "herself"),
                                                           get_all("expression", "itself")))
        self.plural_reflexive = get_all("expression", "themselves")[0]

    def sample(self):
        # The boy knows himself
        # N1      V1    refl_match
        # The boy knows themselves
        # N1      V1    refl_mismatch

        if random.choice([True, False]):
            V1 = choice(self.all_plural_reflexive_predicates)
            N1 = choice(get_matches_of(V1, "arg_1", get_matches_of(V1, "arg_2", self.all_safe_plural_nouns)))
            refl_mismatch = choice(self.all_singular_reflexives)
        else:
            V1 = choice(self.all_singular_reflexive_predicates)
            N1 = choice(get_matches_of(V1, "arg_1", get_matches_of(V1, "arg_2", self.all_safe_singular_nouns)))
            refl_mismatch = self.plural_reflexive
        N1 = N_to_DP_mutate(N1)
        refl_match = choice(get_matched_by(N1, "arg_1", all_reflexives))

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












