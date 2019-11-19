from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class AnaphorGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="binding",
                         uid="principle_A_reconstruction",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=True)

    def sample(self):
        # It's himself that John likes.
        # IT'S Refl    Rel  N1   V1
        # It's himself that likes John.
        # IT'S Refl    Rel  V1   N1

        V1 = choice(all_refl_preds)
        N1 = choice(get_matches_of(V1, "arg_1", all_nouns))
        N1 = N_to_DP_mutate(N1)
        Rel = choice(get_matched_by(N1, "arg_1", all_relativizers))
        Refl = choice(get_matched_by(N1, "arg_1", all_reflexives))
        V1 = conjugate(V1, N1)

        data = {
            "sentence_good": "It's %s %s %s %s." % (Refl[0], Rel[0], N1[0], V1[0]),
            "sentence_bad": "It's %s %s %s %s." % (Refl[0], Rel[0], V1[0], N1[0])
        }
        return data, data["sentence_good"]

generator = AnaphorGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)












