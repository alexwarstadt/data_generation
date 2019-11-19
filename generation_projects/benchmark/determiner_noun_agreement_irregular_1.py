from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class DetNGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="morphology",
                         linguistics="determiner_noun_agreement",
                         uid="determiner_noun_agreement_irregular_1",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=True)
        self.all_null_plural_nouns = get_all("sgequalspl", "1")
        self.all_missingPluralSing_nouns = get_all_conjunctive([("pluralform", ""), ("singularform", "")])
        self.all_unusable_nouns = np.union1d(self.all_null_plural_nouns, self.all_missingPluralSing_nouns)
        self.all_irregular_nouns = get_all("irrpl", "1")
        self.all_irreg_pluralizable_nouns = np.setdiff1d(self.all_irregular_nouns, self.all_unusable_nouns)

    def sample(self):
        # John cleaned this table.
        # N1   V1      Dem  N2_match

        # John cleaned this tables.
        # N1   V1      Dem  N2_mismatch

        N2_match = choice(self.all_irreg_pluralizable_nouns)
        V1 = choice(get_matched_by(N2_match, "arg_2", all_transitive_verbs))
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
        Dem = choice(get_matched_by(N2_match, "arg_1", all_demonstratives))
        if N2_match['pl'] == "1":
            N2_mismatch = N2_match['singularform']
        else:
            N2_mismatch = N2_match['pluralform']
        V1 = conjugate(V1, N1)

        data = {
            "sentence_good": "%s %s %s %s." % (N1[0], V1[0], Dem[0], N2_match[0]),
            "sentence_bad": "%s %s %s %s." % (N1[0], V1[0], Dem[0], N2_mismatch),
            "one_prefix_prefix": "%s %s %s" % (N1[0], V1[0], Dem[0]),
            "one_prefix_word_good": N2_match[0],
            "one_prefix_word_bad": N2_mismatch
        }
        return data, data["sentence_good"]

generator = DetNGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
