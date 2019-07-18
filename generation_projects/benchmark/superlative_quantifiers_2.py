from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
import inflect

class SuperlativeGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="quantification",
                         field="semantics",
                         linguistics="superlative_quantifiers",
                         uid="superlative_quantifiers_2",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        self.quantifiers = ["at least", "at most"]
        self.singular_quantifiers = np.extract(["sg=1" in x["arg_1"] and x["expression"] != "no" for x in self.all_quantifiers], self.all_quantifiers)

    def sample(self):
        # Every professor graded at least three papers
        # Q     N1        V      Qsup     Num   N2
        # No professor graded at least three papers
        # No N1        V      Qsup     Num   N2

        V = choice(self.all_non_plural_transitive_verbs)
        N1 = choice(get_matches_of(V, "arg_1", self.all_singular_count_nouns))
        try:
            Q = choice(get_matched_by(N1, "arg_1", self.singular_quantifiers))
        except IndexError:
            pass
        V = conjugate(V, N1, False)
        N2 = choice(get_matches_of(V, "arg_2", self.all_plural_nouns))
        Qsup = random.choice(self.quantifiers)
        number_inflector = inflect.engine()
        Num = number_inflector.number_to_words(random.randint(2, 10))
        data = {
            "sentence_good": "%s %s %s %s %s %s." % (Q[0], N1[0], V[0], Qsup, Num, N2[0]),
            "sentence_bad": "No %s %s %s %s %s." % (N1[0], V[0], Qsup, Num, N2[0]),
            "crucial_item": Qsup,
            "two_prefix_prefix_good": "%s %s %s %s" % (Q[0], N1[0], V[0], Qsup.split()[0]),
            "two_prefix_prefix_bad": "No %s %s %s" % (N1[0], V[0], Qsup.split()[0]),
            "two_prefix_word": Qsup.split()[1],

        }
        return data

generator = SuperlativeGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
