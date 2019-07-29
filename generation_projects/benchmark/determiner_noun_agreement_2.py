from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from utils.vocab_sets import *


class DetNGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="agreement",
                         field="morphology",
                         linguistics="det_N_agreement",
                         uid="determiner_noun_agreement_2",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.all_null_plural_nouns = get_all("sgequalspl", "1")
        self.all_missingPluralSing_nouns = get_all_conjunctive([("pluralform", ""), ("singularform", "")])
        self.all_unusable_nouns = np.union1d(self.all_null_plural_nouns, self.all_missingPluralSing_nouns)
        self.all_pluralizable_nouns = np.setdiff1d(all_common_nouns, self.all_unusable_nouns)

    def sample(self):
        # John cleaned this       table.
        # N1   V1      Dem_match  N2

        # John cleaned these         table.
        # N1   V1      Dem_mismatch N2

        V1 = choice(all_transitive_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
        except TypeError:
            pass
        try:
            N2 = choice(get_matches_of(V1, "arg_2", self.all_pluralizable_nouns))
        except TypeError:
            pass
        Dem_match = choice(get_matched_by(N2, "arg_1", all_demonstratives))
        if Dem_match[0] == "this":
            Dem_mismatch = "these"
        elif Dem_match[0] == "these":
            Dem_mismatch = "this"
        elif Dem_match[0] == "that":
            Dem_mismatch = "those"
        elif Dem_match[0] == "those":
            Dem_mismatch = "that"
        V1 = conjugate(V1, N1)

        data = {
            "sentence_good": "%s %s %s %s." % (N1[0], V1[0], Dem_match[0], N2[0]),
            "sentence_bad": "%s %s %s %s." % (N1[0], V1[0], Dem_mismatch, N2[0]),
            "two_prefix_prefix_good": "%s %s %s" % (N1[0], V1[0], Dem_match[0]),
            "two_prefix_prefix_bad": "%s %s %s" % (N1[0], V1[0], Dem_mismatch),
            "two_prefix_word": N2[0]
        }
        return data, data["sentence_good"]

generator = DetNGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
