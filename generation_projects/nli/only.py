from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
import inflect

class OnlyGenerator(data_generator.PresuppositionGenerator):
    def __init__(self):
        super().__init__(
            uid="only_presupposition"
        )

    def sample(self):
        # John should only go to France

        V = choice(all_verbs)
        V_args = negate_V_args(verb_args_from_verb(V, allow_negated=False, allow_modal=False))
        VP = V_to_VP_mutate(V, aux=False, args=V_args)
        N_alt = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", get_matches_of(V_args["aux"], "arg_1", all_nominals))))

        if V_args["aux"][0] in ["does", "do", "did"]:
            unembedded_trigger = "%s only %s %s" % (V_args["subj"][0], V_args["aux"][0], VP[0])
        else:
            unembedded_trigger = "%s %s only %s" % (V_args["subj"][0], V_args["aux"][0], VP[0])
        negated_trigger = embed_in_negation(unembedded_trigger, neutral=False)
        interrogative_trigger = embed_in_question(unembedded_trigger)
        modal_trigger = embed_in_modal(unembedded_trigger)
        conditional_trigger = embed_in_conditional(unembedded_trigger)

        presupposition = "%s %s %s" % (V_args["subj"][0], V_args["aux"][0], VP[0])
        negated_presupposition = embed_in_negation(presupposition, neutral=True)
        neutral_presupposition = "%s %s %s" % (N_alt[0], V_args["aux"][0], VP[0])


        data = self.build_presupposition_paradigm(unembedded_trigger=unembedded_trigger,
                                                  negated_trigger=negated_trigger,
                                                  interrogative_trigger=interrogative_trigger,
                                                  modal_trigger=modal_trigger,
                                                  conditional_trigger=conditional_trigger,
                                                  presupposition=presupposition,
                                                  negated_presupposition=negated_presupposition,
                                                  neutral_presupposition=neutral_presupposition)
        return data, presupposition






generator = OnlyGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
