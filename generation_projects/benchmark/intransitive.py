from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="argument_structure",
                         uid="intransitive",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.strict_transitive = get_all("strict_trans", "1", all_transitive_verbs)

    def sample(self):
        # The bear has slept.
        # Subj     Aux V_intrans
        # The bear has injured.
        # Subj     Aux V_trans

        V_intrans = choice(all_intransitive_verbs)
        Subj = N_to_DP_mutate(choice(get_matches_of(V_intrans, "arg_1", all_nominals)))
        Aux = return_aux(V_intrans, Subj)
        V_trans = choice(get_matched_by(Subj, "arg_1", get_matches_of(Aux, "arg_2", self.strict_transitive)))

        data = {
            "sentence_good": "%s %s %s." % (Subj[0], Aux[0], V_intrans[0]),
            "sentence_bad": "%s %s %s." % (Subj[0], Aux[0], V_trans[0])
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
