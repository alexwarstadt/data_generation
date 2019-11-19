from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="control_raising",
                         uid="tough_vs_raising_2",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.raising_preds = get_all("category_2", "Adj_raising_subj")
        self.tough_preds = np.setdiff1d(get_all("category_2", "Adj_tough"), get_all("expression", "ready"))
        self.safe_verbs = np.setdiff1d(all_bare_verbs,
                                       np.union1d(get_all("causative", "1"), get_all("strict_intrans", "0")))

    def sample(self):
        # The hamburger is likely     to taste good
        # Subj          be A_raising  TO VP
        # The hamburger is tough    to taste good
        # Subj          be A_tough  TO VP

        A_tough = choice(self.tough_preds)
        A_raising = choice(self.raising_preds)
        V = choice(self.safe_verbs)
        VP = V_to_VP_mutate(V, aux=False)
        subj = N_to_DP_mutate(choice(get_matches_of(V, "arg_1")))
        be = return_copula(subj)

        data = {
            "sentence_good": "%s %s %s to %s." % (subj[0], be[0], A_raising[0], VP[0]),
            "sentence_bad": "%s %s %s to %s." % (subj[0], be[0], A_tough[0], VP[0]),
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

