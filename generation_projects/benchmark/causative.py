from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice


class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="argument_structure",
                         uid="causative",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)

        self.alternating_verbs = np.union1d(get_all("causative", "1"), get_all("inchoative", "1"))
        self.non_alternating_intransitives = get_all("causative", "0", all_intransitive_verbs)
        self.all_singulars = get_all("sg", "1", all_nominals)
        self.all_plurals = get_all("sg", "0", all_nominals)

    def sample(self):
        # The bear has broken  the lamp.
        # Subj     Aux V_cause obj
        # The bear has slipped   the lamp.
        # Subj     Aux V_intrans obj

        V_cause = choice(self.alternating_verbs)
        if V_cause["category"] == "S\\NP":
            Obj = N_to_DP_mutate(choice(get_matches_of(V_cause, "arg_1", all_nominals)))
            if V_cause["3sg"] == "1":
                Subj = N_to_DP_mutate(choice(np.intersect1d(all_animate_nouns, self.all_singulars)))
            elif V_cause["pres"] == "1":
                Subj = N_to_DP_mutate(choice(np.intersect1d(all_animate_nouns, self.all_plurals)))
            else:
                Subj = N_to_DP_mutate(choice(all_animate_nouns))
        else:
            Subj = N_to_DP_mutate(choice(get_matches_of(V_cause, "arg_1", all_nominals)))
            Obj = N_to_DP_mutate(choice(get_matches_of(V_cause, "arg_2", all_nominals)))

        Aux = return_aux(V_cause, Subj)

        if Subj["sg"] == "1":
            safe_verbs = np.intersect1d(self.non_alternating_intransitives, all_possibly_singular_verbs)
        else:
            safe_verbs = np.intersect1d(self.non_alternating_intransitives, all_possibly_plural_verbs)
        V_intrans = choice(get_matched_by(Obj, "arg_1", get_matches_of(Aux, "arg_2", safe_verbs)))

        data = {
            "sentence_good": "%s %s %s %s." % (Subj[0], Aux[0], V_cause[0], Obj[0]),
            "sentence_bad": "%s %s %s %s." % (Subj[0], Aux[0], V_intrans[0], Obj[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

