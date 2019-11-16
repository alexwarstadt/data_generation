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
            uid="possessed_definites_uniqueness"
        )
        self.safe_nouns = np.intersect1d(np.union1d(np.setdiff1d(all_nouns, all_animate_nouns), all_relational_poss_nouns), all_singular_nouns)
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

        N1 = N_to_DP_mutate(choice(get_all("animate", "1", all_nouns)), allow_quantifiers=False)
        N1_alt = N_to_DP_mutate(choice(get_all("animate", "1", all_nouns), avoid=N1), allow_quantifiers=False)
        N2 = choice(self.safe_nouns)
        s_poss = "'" if N1["pl"] == "1" and N1[0][-1] == "s" else "'s"
        V = choice(get_matched_by(N2, "arg_1", all_bare_verbs))
        V_args = verb_args_from_verb(V, subj=N2, allow_negated=False, allow_modal=False, allow_quantifiers=False)
        V_args = negate_V_args(V_args)
        V_args = embed_V_args_under_modal(V_args)
        V_bare = get_bare_form(V)
        VP = V_to_VP_mutate(V, aux=False, args=V_args)
        D = "" if N2["pl"] == "1" or N2["mass"] == "1" else "a"
        HAVE = "has" if N1["sg"] == "1" else "have"
        HAVE_NEG = "doesn't have" if N1["sg"] == "1" else "don't have"

        unembedded_trigger = "%s%s %s %s %s." % (N1[0], s_poss, N2[0], V_args["aux"][0], VP[0])
        negated_trigger = "%s%s %s %s %s %s." % (N1[0], s_poss, N2[0], V_args["aux_neg"][0], V_args["verb_neg"][0], join_args(V_args["args"]))
        conditional_trigger = "if %s, it's okay." % unembedded_trigger[:-1]
        if V_args["aux_under_modal"] == None:
            modal_trigger = "%s%s %s might %s %s." % (N1[0], s_poss, N2[0], V_bare[0], join_args(V_args["args"]))
        else:
            modal_trigger = "%s%s %s might %s %s %s." % (N1[0], s_poss, N2[0], V_args["aux_under_modal"][0], V_args["verb_under_modal"][0], join_args(V_args["args"]))
        if V["finite"] == "1":
            do = get_do_form(V)
            interrogative_trigger = "%s %s%s %s %s %s?" % (do[0], N1[0], s_poss, N2[0], V_bare[0], join_args(V_args["args"]))
        else:
            interrogative_trigger = "%s %s%s %s %s %s?" % (V_args["aux"][0], N1[0], s_poss, N2[0], V[0], join_args(V_args["args"]))

        presupposition = "%s %s exactly one %s." % (N1[0], HAVE, N2[0])
        negated_presupposition = "%s %s exactly one %s." % (N1[0], HAVE_NEG, N2[0])
        neutral_presupposition = "%s %s exactly one %s." % (N1_alt[0], HAVE, N2[0])

        data = self.build_presupposition_paradigm(unembedded_trigger=unembedded_trigger,
                                                  negated_trigger=negated_trigger,
                                                  interrogative_trigger=interrogative_trigger,
                                                  modal_trigger=modal_trigger,
                                                  conditional_trigger=conditional_trigger,
                                                  presupposition=presupposition,
                                                  negated_presupposition=negated_presupposition,
                                                  neutral_presupposition=neutral_presupposition)
        return data, presupposition

generator = PossessGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
