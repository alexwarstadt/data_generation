from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="control_raising",
                         uid="tough_vs_raising_1",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.raising_preds = get_all("category_2", "Adj_raising_subj")
        self.tough_preds = get_all("category_2", "Adj_tough")
        self.strict_transitive = get_all("strict_trans", "1")

    def sample(self):
        # The hamburger is tough    to devour
        # Subj          be A_tough  TO V
        # The hamburger is likely   to devour
        # Subj          be A_raise  TO V

        A_tough = choice(self.tough_preds)
        A_raising = choice(self.raising_preds)
        V = choice(get_matches_of(A_tough, "arg_1", self.strict_transitive))
        subj = N_to_DP_mutate(choice(get_matches_of(V, "arg_2")))
        be = return_copula(subj)

        data = {
            "sentence_good": "%s %s %s to %s." % (subj[0], be[0], A_tough[0], V[0]),
            "sentence_bad": "%s %s %s to %s." % (subj[0], be[0], A_raising[0], V[0]),
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

