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
        V_args = negate_V_args(verb_args_from_verb(V, allow_negated=False, allow_modal=False, allow_quantifiers=False))
        V_args = embed_V_args_under_modal(V_args)
        V_bare = get_bare_form(V)
        VP = V_to_VP_mutate(V, aux=False, args=V_args, allow_quantifiers=False)
        N_alt = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", get_matches_of(V_args["aux"], "arg_1", all_nominals))), allow_quantifiers=False)

        if V_args["aux"][0] in ["does", "do", "did"]:
            unembedded_trigger = "%s only %s %s." % (V_args["subj"][0], V_args["aux"][0], VP[0])
        else:
            unembedded_trigger = "%s %s only %s." % (V_args["subj"][0], V_args["aux"][0], VP[0])
        negated_trigger = "%s %s only %s %s." % (V_args["subj"][0], V_args["aux_neg"][0], V_args["verb_neg"][0], " ".join([x[0] for x in V_args["args"]]))
        if V_args["aux_under_modal"] == None:
            modal_trigger = "%s might only %s." % (V_args["subj"][0], VP[0])
        else:
            modal_trigger = "%s might %s only %s %s." % (V_args["subj"][0], V_args["aux_under_modal"][0], V_args["verb_under_modal"][0], " ".join([x[0] for x in V_args["args"]]))
        conditional_trigger = "if %s, it's okay." % unembedded_trigger[-1]
        if V["finite"] == "1":
            do = get_do_form(V)
            interrogative_trigger = "%s %s only %s %s?" % (do[0], V_args["subj"][0], V_bare[0], join_args(V_args["args"]))
        else:
            interrogative_trigger = "%s %s only %s?" % (V_args["aux"][0],  V_args["subj"][0], VP[0])


        presupposition = "%s %s %s." % (V_args["subj"][0], V_args["aux"][0], VP[0])
        negated_presupposition = "%s %s %s %s." % (V_args["subj"][0], V_args["aux_neg"][0], V_args["verb_neg"][0], " ".join([x[0] for x in V_args["args"]]))
        neutral_presupposition = "%s %s %s." % (N_alt[0], V_args["aux"][0], VP[0])


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
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/IMPPRES/presupposition/%s.jsonl" % generator.uid)
