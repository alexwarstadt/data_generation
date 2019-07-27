from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *
from utils.string_utils import string_beautify
import inflect

class PossessGenerator(data_generator.NLIGenerator):
    def __init__(self):
        super().__init__(
            uid="possessed_definites"
        )
        self.safe_nouns = np.union1d(np.setdiff1d(all_nouns, all_animate_nouns), all_relational_poss_nouns)
        # might
        # would
        # could
        # should
        # will
        # can
        # to
        # do
        # does
        # did
        # is
        # are
        # was
        # were
        # has
        # have
        # had
        # wouldn!t
        # couldn!t
        # shouldn!t
        # won!t
        # can!t
        # don!t
        # doesn!t
        # didn!t
        # isn!t
        # aren!t
        # wasn!t
        # weren!t
        # hasn!t
        # haven!t
        all_modal_aux = np.union1d(all_au)
        real_auxs = ["do", "does", "did", "is", "are", "was", "were", "has", "have", "had"]
        m_auxs = ["might", "would", "could", "should", "will", "can"]
        self.real_auxs = [get_all("expression", )]

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
        v_args = verb_args_from_verb(V, subj=N2, allow_negated=False)
        try:
            VP = " ".join([v_args["aux"][0],
                           V[0]] +
                          [x[0] for x in v_args["args"]])
        except KeyError:
            pass
        D = "" if N2["pl"] == "1" or N2["mass"] == "1" else "a"
        HAVE = "has" if N1["sg"] == "1" else "have"


        data = [
            {
                "sentence_1": "%s%s %s %s." % (N1[0], s_poss, N2[0], VP),
                "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0]),
                "trigger": "unembedded"
            },
            {
                "sentence_1": "%s %s%s %s %s." % (v_args["aux"][0], N1[0], s_poss, N2[0], V_to_VP_mutate(aux=False, args=v_args)[0]),
                "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0]),
                "trigger": "negated"
            }
        ]
        return data, data[0]["sentence_1"]

generator = PossessGenerator()
generator.generate_paradigm(number_to_generate=50, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
