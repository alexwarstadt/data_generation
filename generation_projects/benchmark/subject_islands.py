from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from functools import reduce


class AnaphorGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(
            category="movement",
            field="syntax",
            linguistics="island_effects",
            uid="subject_island",
            simple_lm_method=True,
            one_prefix_method=False,
            two_prefix_method=False,
            lexically_identical=True
        )
        self.all_non_finite_refl_preds = np.union1d(get_all("finite", "0", self.all_refl_preds), self.all_refl_nonverbal_predicates)

    def sample(self):
        # What did John discuss a book about?
        # wh   aux NP   V       relN

        # What did a book about discuss John?
        # wh   aux relN         V       relN

        relN = N_to_DP_mutate(choice(self.all_relational_nouns))
        V = choice(get_matched_by(relN, "arg_1", self.all_non_finite_refl_preds))
        if V["category_2"] == "Pred":
            Cop = return_copula(relN)
            if Cop["finite"] == "1":
                Aux = Cop
                Cop = choice(get_all("expression", ""))
            else:
                Aux = return_aux(Cop, relN)
        else:
            Cop = choice(get_all("expression", ""))
            Aux = return_aux(V, relN)

        # Grab all nouns with the same number as RelN
        NP = N_to_DP_mutate(choice(np.extract([x["sg"] == relN["sg"] for x in get_matches_of(V, "arg_1", self.all_nouns)],
                                              get_matches_of(V, "arg_1", self.all_nouns))))
        wh = choice(get_matches_of(relN, "arg_1", self.all_wh_words))
        data = {
            "sentence_good": "%s %s %s %s %s %s?" % (wh[0], Aux[0], NP[0], Cop[0], V[0], relN[0]),
            "sentence_bad": "%s %s %s %s %s %s?" % (wh[0], Aux[0], relN[0], Cop[0], V[0], NP[0]),
        }
        return data, data["sentence_good"]


binding_generator = AnaphorGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % binding_generator.uid)












