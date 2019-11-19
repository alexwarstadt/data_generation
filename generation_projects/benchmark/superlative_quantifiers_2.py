from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import inflect
from utils.vocab_sets import *

class SuperlativeGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="semantics",
                         linguistics="quantifiers",
                         uid="superlative_quantifiers_2",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        self.quantifiers = ["at least", "at most"]
        self.singular_quantifiers = np.extract(["sg=1" in x["arg_1"] and x["expression"] != "no" for x in all_quantifiers], all_quantifiers)
        self.safe_nouns = np.setdiff1d(all_plural_nouns, all_proper_names)

    def sample(self):
        # Every professor graded at least three papers
        # Q     N1        V      Qsup     Num   N2
        # No professor graded at least three papers
        # NO N1        V      Qsup     Num   N2

        V = choice(all_non_plural_transitive_verbs)
        N1 = choice(get_matches_of(V, "arg_1", all_singular_count_nouns))
        Q = choice(get_matched_by(N1, "arg_1", self.singular_quantifiers))
        V = conjugate(V, N1, False)
        N2 = choice(get_matches_of(V, "arg_2", self.safe_nouns))
        Qsup = random.choice(self.quantifiers)
        number_inflector = inflect.engine()
        Num = number_inflector.number_to_words(random.randint(2, 10))
        data = {
            "sentence_good": "%s %s %s %s %s %s." % (Q[0], N1[0], V[0], Qsup, Num, N2[0]),
            "sentence_bad": "No %s %s %s %s %s." % (N1[0], V[0], Qsup, Num, N2[0]),
            "two_prefix_prefix_good": "%s %s %s %s" % (Q[0], N1[0], V[0], Qsup.split()[0]),
            "two_prefix_prefix_bad": "No %s %s %s" % (N1[0], V[0], Qsup.split()[0]),
            "two_prefix_word": Qsup.split()[1],
        }
        return data, data["sentence_good"]

generator = SuperlativeGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
