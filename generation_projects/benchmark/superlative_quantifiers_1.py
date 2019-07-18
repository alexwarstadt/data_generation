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
                         uid="superlative_quantifiers_1",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.quantifiers = [("more than", "at least"),
                            ("fewer than", "at most")]

    def sample(self):
        # No professor graded more than three papers
        # No N1        V      Q1        Num   N2
        # No professor graded at least four papers
        # No N1        V      Q2       Num  N2

        V = choice(self.all_non_plural_transitive_verbs)
        N1 = choice(get_matches_of(V, "arg_1", self.all_singular_count_nouns))
        V = conjugate(V, N1, False)
        N2 = choice(get_matches_of(V, "arg_2", self.all_plural_nouns))
        quantifiers = random.choice(self.quantifiers)
        Q1 = quantifiers[0]
        Q2 = quantifiers[1]
        number_inflector = inflect.engine()
        Num = number_inflector.number_to_words(random.randint(2, 10))
        data = {
            "sentence_good": "No %s %s %s %s %s." % (N1[0], V[0], Q1, Num, N2[0]),
            "sentence_bad": "No %s %s %s %s %s." % (N1[0], V[0], Q2, Num, N2[0]),
            "crucial_item": Q2
        }
        return data

generator = SuperlativeGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
