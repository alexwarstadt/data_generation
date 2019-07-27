from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from functools import reduce


class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="agreement",
                         field="morphology",
                         linguistics="subject_verb_agreement",
                         uid="regular_plural_subj_v_agreement_1",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_irreg_nouns = get_all_conjunctive([("category", "N"), ("irrpl", "1")])
        self.all_reg_nouns = get_all_conjunctive([("category", "N"), ("irrpl", "")])

    def sample(self):
        # The cat is        eating food
        #     N1  aux_agree V1     N2
        # The cat are          eating food
        #     N1  aux_nonagree V1     N2

        if random.choice([True, False]):
            V1 = choice(self.all_non_finite_transitive_verbs)
            try:
                N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", self.all_nouns)))
            except TypeError:
                pass
        else:
            V1 = choice(self.all_non_finite_intransitive_verbs)
            N2 = " "
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_reg_nouns)))
        except TypeError:
                pass
        auxes = require_aux_agree(V1, N1)
        aux_agree = auxes["aux_agree"]
        aux_nonagree = auxes["aux_nonagree"]

        data = {
            "sentence_good": "%s %s %s %s." % (N1[0], aux_agree, V1[0], N2[0]),
            "sentence_bad": "%s %s %s %s." % (N1[0], aux_nonagree, V1[0], N2[0]),
            "one_prefix_prefix": "%s" % (N1[0]),
            "one_prefix_word_good": aux_agree,
            "one_prefix_word_bad": aux_nonagree
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
