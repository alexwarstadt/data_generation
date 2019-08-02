from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *
from utils.string_utils import string_beautify
import inflect

class ChangeOfStateGenerator(data_generator.PresuppositionGenerator):
    def __init__(self):
        super().__init__(
            uid="change_of_state"
        )
        real_auxs = ["did", "is", "are", "was", "were", "has", "have", "had"]
        m_auxs = ["might", "would", "could", "should", "will", "can"]
        self.real_auxs = reduce(np.union1d, [get_all("expression", s, all_modals_auxs) for s in real_auxs])
        self.m_auxs = reduce(np.union1d, [get_all("expression", s, all_modals_auxs) for s in m_auxs])
        self.rogatives = get_all_conjunctive([("category", "(S\\NP)/Q"), ("finite", "1")])
        all_cos_verbs = get_all("change_of_state", "1")
        self.safe_cos_verbs = get_all("pres", "0", all_cos_verbs)
        self.non_v_preds = get_all("non_v_pred", "1")

    def sample(self):
        # The ice has melted
        # subj    aux VP

        # The ice      used to be liquid
        # subj_changed cop        pred

        # Bill wonders the ice has melted.
        # N0   V_rog   WHETHER N1  's N2     aux_real V_real

        # The ice has not melted
        #

        # The ice has not melted
        #

        # TRIGGER
        V_cos = choice(self.safe_cos_verbs)
        V_args = verb_args_from_verb(V_cos, allow_negated=False)
        V_args = negate_V_args(V_args)

        # PRESUPPOSITION
        subj_changed = V_args["subj"] if V_cos["change_arg"] == "1" else V_args["args"][0]
        subj_changed_alternative = N_to_DP_mutate(choice(
            get_matches_of(V_args["verb"], "arg_1",
                           get_all("sg", subj_changed["sg"], all_nominals)), subj_changed))
        if V_cos["bare"] == "1":
            cop = "is" if subj_changed["sg"] == "1" else "are"
            cop_neg = "isn't" if subj_changed["sg"] == "1" else "aren't"
        else:
            cop = choice(["used to be", "was"]) if subj_changed["sg"] == "1" else choice(["used to be", "were", "have been"])
            cop_neg = choice(["didn't used to be", "wasn't"]) if subj_changed["sg"] == "1" else choice(["didn't used to be", "weren't", "haven't been"])
        initial_states = get_matches_of(V_cos, "initial_state", self.non_v_preds)
        try:
            pred = choice(get_matched_by(subj_changed, "arg_1", initial_states))
        except IndexError:
            pass
        if V_cos["change_arg"] == "1" and V_cos["category"] == "(S\\NP)/NP":
            pred_args = V_args["args"]
        else:
            pred_args = pred_args_from_pred(pred, subj=subj_changed)["args"]

        # BUILD SENTENCES
        unembedded_trigger = "%s %s %s %s." % (V_args["subj"][0], V_args["aux"][0], V_args["verb"][0], " ".join([x[0] for x in V_args["args"]]))
        negated_trigger = embed_in_negation(unembedded_trigger, neutral=False)
        modal_trigger = embed_in_modal(unembedded_trigger)
        interrogative_trigger = embed_in_question(unembedded_trigger)
        conditional_trigger = embed_in_conditional(unembedded_trigger)

        presupposition = "%s %s %s %s." % (subj_changed[0], cop, pred[0], " ".join([x[0] for x in pred_args]))
        negated_presupposition = embed_in_negation(presupposition, neutral=True)
        neutral_presupposition = "%s %s %s %s." % (subj_changed_alternative[0], cop, pred[0], " ".join([x[0] for x in pred_args]))

        data = self.build_presupposition_paradigm(unembedded_trigger=unembedded_trigger,
                                                  negated_trigger=negated_trigger,
                                                  interrogative_trigger=interrogative_trigger,
                                                  modal_trigger=modal_trigger,
                                                  conditional_trigger=conditional_trigger,
                                                  presupposition=presupposition,
                                                  negated_presupposition=negated_presupposition,
                                                  neutral_presupposition=neutral_presupposition)
        return data, presupposition

generator = ChangeOfStateGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

# The ice will melt         The ice is frozen
# The ice melts             ***
# The ice melted            The ice used to be frozen
# The ice has melted        The ice used to be frozen
# The ice had melted        The ice used to be frozen
# The ice should melt       The ice is frozen
# The ice is melting        The ice used to be frozen