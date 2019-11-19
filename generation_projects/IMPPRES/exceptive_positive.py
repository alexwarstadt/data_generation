from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
import inflect

class BothGenerator(data_generator.PresuppositionGenerator):
    def __init__(self):
        super().__init__(
            uid="exceptive_positive"
        )
        safe_det_str = ["a", "the", "an", "this", "that", "some", ""]
        self.safe_dets = reduce(np.union1d, [get_all("expression", x, get_all("category_2", "D")) for x in safe_det_str])
        bad_verbs = np.union1d(all_intransitive_verbs, get_all("category_2", "IV_ag_pl"))
        self.safe_verbs = np.setdiff1d(all_possibly_singular_verbs, bad_verbs)
        self.safe_nouns = np.setdiff1d(all_nominals, get_all("institution", "1"))


    def sample(self):
        # Aside from John, someone left.
        # TODO: finish this

        V = choice(self.safe_verbs)
        try:
            N_subj = choice(get_matches_of(V, "arg_1", self.safe_nouns))
        except Exception:
            pass
        D = choice(get_matched_by(N_subj, "arg_1", self.safe_dets))
        VP = V_to_VP_mutate(V, args=verb_args_from_verb(V, subj=N_subj, allow_negated=False, allow_modal=False))
        VP_alt = V_to_VP_mutate(V, args=verb_args_from_verb(V, subj=N_subj, allow_negated=False, allow_modal=False))
        rel = choice(get_matched_by(N_subj, "arg_1", all_relativizers))
        existential = "someone" if N_subj["animate"] == "1" else "something"

        unembedded_trigger = "it is %s %s %s %s." % (D[0], N_subj[0], rel[0], VP[0])
        negated_trigger = embed_in_negation(unembedded_trigger, neutral=False)
        modal_trigger = embed_in_modal(unembedded_trigger)
        interrogative_trigger = embed_in_question(unembedded_trigger)
        conditional_trigger = embed_in_conditional(unembedded_trigger)

        presupposition = "%s %s" % (existential, VP[0])
        negated_presupposition = embed_in_negation(presupposition, neutral=True)
        neutral_presupposition = "%s %s" % (existential, VP_alt[0])

        data = self.build_presupposition_paradigm(unembedded_trigger=unembedded_trigger,
                                                  negated_trigger=negated_trigger,
                                                  interrogative_trigger=interrogative_trigger,
                                                  modal_trigger=modal_trigger,
                                                  conditional_trigger=conditional_trigger,
                                                  presupposition=presupposition,
                                                  negated_presupposition=negated_presupposition,
                                                  neutral_presupposition=neutral_presupposition)
        return data, presupposition






generator = BothGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/IMPPRES/%s.jsonl" % generator.uid)
