from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
import inflect

class QuestionGenerator(data_generator.PresuppositionGenerator):
    def __init__(self):
        super().__init__(
            uid="question_presupposition"
        )
        self.wh_words = ["why", "when", "where", "how"]
        self.all_non_embedding_verbs = np.setdiff1d(all_verbs, np.union1d(all_rogatives, get_all("category", "(S\\NP)/S")))
        self.all_positive_aux = np.intersect1d(all_auxs, get_all("negated", "0"))

    def sample(self):
        # John  will    know  where Bill  has read  the book.
        # N_rog aux_rog V_rog wh    N_emb aux V_emb args_emb
        # Bill read the book.
        # S

        V_rog = choice(all_rogatives)
        N_rog = N_to_DP_mutate(choice(get_matches_of(V_rog, "arg_1", all_nouns)))
        aux_rog = choice(get_matched_by(V_rog, "arg_2", get_matched_by(N_rog, "arg_1", all_non_negated_auxs)))

        wh = choice(self.wh_words)

        V_emb = choice(all_verbs)
        N_emb = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_1", all_nouns)))
        aux_emb = choice(get_matched_by(V_emb, "arg_2", get_matched_by(N_emb, "arg_1", self.all_positive_aux)))
        args_emb = verb_args_from_verb(V_emb, subj=N_emb, allow_negated=False)
        args_emb["aux"] = aux_emb
        args_emb = negate_V_args(args_emb)
        N_emb_2 = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_1", all_nouns), avoid=args_emb["subj"]))

        unembedded_trigger = "%s %s %s %s %s." % (N_rog[0], aux_rog[0], V_rog[0], wh, make_sentence_from_args(args_emb))
        negated_trigger = embed_in_negation(unembedded_trigger, neutral=False)
        interrogative_trigger = embed_in_question(unembedded_trigger)
        modal_trigger = embed_in_modal(unembedded_trigger)
        conditional_trigger = embed_in_conditional(unembedded_trigger)

        presupposition = make_sentence_from_args(args_emb)
        negated_presupposition = embed_in_negation(presupposition, neutral=True)
        neutral_presupposition = "%s %s %s %s." % (N_emb_2[0], args_emb["aux"][0], args_emb["verb"][0], join_args(args_emb["args"]))

        data = self.build_presupposition_paradigm(unembedded_trigger=unembedded_trigger,
                                                  negated_trigger=negated_trigger,
                                                  interrogative_trigger=interrogative_trigger,
                                                  modal_trigger=modal_trigger,
                                                  conditional_trigger=conditional_trigger,
                                                  presupposition=presupposition,
                                                  negated_presupposition=negated_presupposition,
                                                  neutral_presupposition=neutral_presupposition)
        return data, presupposition






generator = QuestionGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
