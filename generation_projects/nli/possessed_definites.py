from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *
from utils.string_utils import string_beautify
import inflect

class PossessGenerator(data_generator.PresuppositionGenerator):
    def __init__(self):
        super().__init__(
            uid="possessed_definites"
        )
        self.safe_nouns = np.union1d(np.setdiff1d(all_nouns, all_animate_nouns), all_relational_poss_nouns)
        real_auxs = ["do", "does", "did", "is", "are", "was", "were", "has", "have", "had"]
        m_auxs = ["might", "would", "could", "should", "will", "can"]
        self.real_auxs = reduce(np.union1d, [get_all("expression", s, all_modals_auxs) for s in real_auxs])
        self.m_auxs = reduce(np.union1d, [get_all("expression", s, all_modals_auxs) for s in m_auxs])
        self.rogatives = get_all_conjunctive([("category", "(S\\NP)/Q"), ("finite", "1")])

    def sample(self):
        # John's sister has      left.
        # N1  's N2     aux_real V_real

        # John has  a sister
        # N1   HAVE D N2

        # Bill wonders whether John's sister has      left.
        # N0   V_rog   WHETHER N1  's N2     aux_real V_real

        # John's sister should leave.
        # N1  's N2     aux_m  V_m

        # John's sister has      not left.
        # N1  's N2     aux_real NOT V_real

        N1 = N_to_DP_mutate(choice(get_all("animate", "1", all_nominals)))
        N2 = choice(self.safe_nouns)
        s_poss = "'" if N1["pl"] == "1" and N1[0][-1] == "s" else "'s"
        V = choice(get_matched_by(N2, "arg_1", all_bare_verbs))
        aux_real = choice(get_matched_by(N2, "arg_1", get_matched_by(V, "arg_2", self.real_auxs)))
        V_m_str = get_bare_form(V)
        aux_m = choice(self.m_auxs)
        v_args = verb_args_from_verb(V, subj=N2, allow_negated=False)
        VP = V_to_VP_mutate(V, aux=False, args=v_args)
        D = "" if N2["pl"] == "1" or N2["mass"] == "1" else "a"
        HAVE = "has" if N1["sg"] == "1" else "have"
        V_rog = choice(self.rogatives)
        N0 = N_to_DP_mutate(choice(get_matches_of(V_rog, "arg_1", all_nouns)))


        data = [
            {
                "sentence_1": "%s%s %s %s %s." % (N1[0], s_poss, N2[0], aux_real[0], VP[0]),
                "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0]),
                "trigger": "unembedded"
            },
            {
                "sentence_1": "%s %s whether %s%s %s %s %s." % (N0[0], V_rog[0], N1[0], s_poss, N2[0], aux_real[0], VP[0]),
                "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0]),
                "trigger": "question"
            },
            {
                "sentence_1": "%s%s %s %s %s." % (N1[0], s_poss, N2[0], aux_m[0], V_m_str),
                "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0]),
                "trigger": "modal"
            },
            {
                "sentence_1": "%s%s %s %s not %s." % (N1[0], s_poss, N2[0], aux_real[0], VP[0]),
                "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0]),
                "trigger": "negated"
            }
        ]
        return data, data[0]["sentence_1"]

generator = PossessGenerator()
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
