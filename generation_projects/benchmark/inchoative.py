from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="argument_structure",
                         uid="inchoative",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.alternating_verbs = np.union1d(get_all("causative", "1"), get_all("inchoative", "1"))
        self.non_alternating_transitives = get_all("inchoative", "0", all_transitive_verbs)
        self.all_singulars = get_all("sg", "1", all_nominals)
        self.all_plurals = get_all("sg", "0", all_nominals)

    def sample(self):
        # The lamp has broken.
        # Subj     Aux V_inch
        # The lamp has pained.
        # Subj     Aux V_trans

        V_inch = choice(self.alternating_verbs)
        if V_inch["category"] == "(S\\NP)/NP":
            if V_inch["3sg"] == "1":
                Subj = N_to_DP_mutate(choice(get_matches_of(V_inch, "arg_2", self.all_singulars)))
            elif V_inch["pres"] == "1":
                Subj = N_to_DP_mutate(choice(get_matches_of(V_inch, "arg_2", self.all_plurals)))
            else:
                Subj = N_to_DP_mutate(choice(get_matches_of(V_inch, "arg_2", all_nominals)))
        else:
            Subj = N_to_DP_mutate(choice(get_matches_of(V_inch, "arg_1")))
        Aux = return_aux(V_inch, Subj)
        if Subj["sg"] == "1":
            safe_verbs = np.intersect1d(self.non_alternating_transitives, all_possibly_singular_verbs)
        else:
            safe_verbs = np.intersect1d(self.non_alternating_transitives, all_possibly_plural_verbs)
        V_trans = choice(get_matched_by(Subj, "arg_2", get_matches_of(Aux, "arg_2", safe_verbs)))

        data = {
            "sentence_good": "%s %s %s." % (Subj[0], Aux[0], V_inch[0]),
            "sentence_bad": "%s %s %s." % (Subj[0], Aux[0], V_trans[0])
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

