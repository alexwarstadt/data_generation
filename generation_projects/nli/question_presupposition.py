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
        N_rog = N_to_DP_mutate(choice(get_matches_of(V_rog, "arg_1", all_nouns)), allow_quantifiers=False)
        aux_rog = choice(get_matched_by(V_rog, "arg_2", get_matched_by(N_rog, "arg_1", all_non_negated_auxs)))
        V_args = verb_args_from_verb(V_rog, subj=N_rog, allow_negated=False, allow_modal=False, allow_quantifiers=False)
        V_args = negate_V_args(V_args)
        V_args = embed_V_args_under_modal(V_args)
        V_bare = get_bare_form(V_rog)

        wh = choice(self.wh_words)

        V_emb = choice(all_verbs)
        N_emb = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_1", all_nouns)), allow_quantifiers=False)
        aux_emb = choice(get_matched_by(V_emb, "arg_2", get_matched_by(N_emb, "arg_1", self.all_positive_aux)))
        args_emb = verb_args_from_verb(V_emb, subj=N_emb, allow_negated=False, allow_quantifiers=False)
        args_emb["aux"] = aux_emb
        args_emb = negate_V_args(args_emb)
        N_emb_2 = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_1", all_nouns), avoid=args_emb["subj"]))
        S = make_sentence_from_args(args_emb)

        unembedded_trigger = "%s %s %s %s %s." % (N_rog[0], aux_rog[0], V_rog[0], wh, S)
        negated_trigger = "%s %s %s %s %s." % (N_rog[0], V_args["aux_neg"][0], V_args["verb_neg"][0], wh, S)
        conditional_trigger = "if %s, it's okay." % unembedded_trigger[:-1]

        if V_args["aux_under_modal"] == None:
            modal_trigger = "%s might %s %s %s." % (N_rog[0], V_rog[0], wh, S)
        else:
            modal_trigger = "%s might %s %s %s %s." % (N_rog[0], V_args["aux_under_modal"][0], V_args["verb_under_modal"][0], wh, S)
        if V_rog["finite"] == "1":
            do = get_do_form(V_rog)
            interrogative_trigger = "%s %s %s %s %s?" % (do[0], N_rog[0], V_bare[0], wh, S)
        else:
            interrogative_trigger = "%s %s %s %s %s?" % (V_args["aux"][0], N_rog[0], V_rog[0], wh, S)

        presupposition = make_sentence_from_args(args_emb)
        negated_presupposition = "%s %s %s %s." % (args_emb["subj"][0], args_emb["aux_neg"][0], args_emb["verb_neg"][0], join_args(args_emb["args"]))
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
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/IMPPRES/presupposition/%s.jsonl" % generator.uid)
