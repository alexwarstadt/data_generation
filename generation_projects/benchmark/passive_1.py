from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="argument_structure",
                         uid="passive_1",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.en_verbs = get_all("en", "1")
        self.intransitive = get_all("passive", "0", self.en_verbs)
        self.transitive = get_all("passive", "1", self.en_verbs)

    def sample(self):
        # The girl was attacked by the bear.
        # NP1      be  V_trans  BY NP2
        # The girl was smiled    by the bear.
        # NP1      be  V_intrans BY NP2

        V_intrans = choice(self.intransitive)
        NP1 = N_to_DP_mutate(choice(get_matches_of(V_intrans, "arg_1", all_nominals)))
        V_trans = choice(get_matched_by(NP1, "arg_2", self.transitive))
        NP2 = N_to_DP_mutate(choice(get_matches_of(V_trans, "arg_1", all_nominals)))
        be = return_copula(NP1)

        data = {
            "sentence_good": "%s %s %s by %s." % (NP1[0], be[0], V_trans[0], NP2[0]),
            "sentence_bad": "%s %s %s by %s." % (NP1[0], be[0], V_intrans[0], NP2[0])
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

