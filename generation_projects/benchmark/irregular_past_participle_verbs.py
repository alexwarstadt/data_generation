from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="morphology",
                         linguistics="irregular_forms",
                         uid="irregular_past_participle_verbs",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_trans_en_verbs = get_all("special_en_form", "1", all_transitive_verbs)
        self.all_intrans_en_verbs = get_all("special_en_form", "1", all_intransitive_verbs)

    def sample(self):
        # John ate    the pie
        # N1   V_past     N2
        # John eaten the pie
        # N1   V_en      N2

        x = random.random()
        if x < 1 / 2:
            V_base = choice(self.all_trans_en_verbs)
            N2 = N_to_DP_mutate(choice(get_matches_of(V_base, "arg_2", all_nouns)))
        else:
            V_base = choice(self.all_intrans_en_verbs)
            N2 = " "

        Verbs = get_all("root", V_base["root"])
        V_past = get_all("past", "1", Verbs)
        V_en = get_all("en", "1", Verbs)
        N1 = N_to_DP_mutate(choice(get_matches_of(V_base, "arg_1", all_nouns)))

        data = {
            "sentence_good": "%s %s %s." % (N1[0], V_past[0][0], N2[0]),
            "sentence_bad": "%s %s %s." % (N1[0], V_en[0][0], N2[0]),
            "one_prefix_prefix": "%s" % (N1[0]),
            "one_prefix_word_good": V_past[0][0],
            "one_prefix_word_bad": V_en[0][0]
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
