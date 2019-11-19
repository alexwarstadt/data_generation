from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="argument_structure",
                         uid="drop_argument",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.strict_transitive = get_all("strict_trans", "1", all_transitive_verbs)
        self.drop_arg_transitive = get_all("strict_trans", "0", all_transitive_verbs)

    def sample(self):
        # The bear has attacked.
        # Subj     Aux V_non_strict
        # The bear has injured.
        # Subj     Aux V_strict

        V_non_strict = choice(self.drop_arg_transitive)
        Subj = N_to_DP_mutate(choice(get_matches_of(V_non_strict, "arg_1", all_nominals)))
        Aux = return_aux(V_non_strict, Subj)
        V_strict = choice(get_matched_by(Subj, "arg_1", get_matches_of(Aux, "arg_2", self.strict_transitive)))

        data = {
            "sentence_good": "%s %s %s." % (Subj[0], Aux[0], V_non_strict[0]),
            "sentence_bad": "%s %s %s." % (Subj[0], Aux[0], V_strict[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

