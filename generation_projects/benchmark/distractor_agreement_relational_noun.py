from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="morphology",
                         linguistics="subject_verb_agreement",
                         uid="distractor_agreement_relational_noun",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_reg_nouns = get_all_conjunctive([("noun", "1"), ("irrpl", "")])
        self.safe_subjs = get_all("category", "N/NP", self.all_reg_nouns)
        self.safe_verbs = np.setdiff1d(all_verbs, get_all("past", "1"))

    def sample(self):
        # The doctor of the men is        helping some people.
        # D   Subj      S_arg   Aux_agree V_agree args
        # The doctor of the men are           helping     some people.
        # D   Subj      S_arg   Aux_not_agree V_not_agree args

        S_arg = None
        while S_arg is None:
            subj = choice(self.safe_subjs)
            D = choice(get_matched_by(subj, "arg_1", all_common_dets))
            V_agree = choice(get_matched_by(subj, "arg_1", self.safe_verbs))
            if V_agree["finite"] == "1":
                if V_agree["3sg"] == "1":
                    V_not_agree = choice(
                        get_all_conjunctive([("pres", "1"), ("3sg", "0")], get_all("root", V_agree["root"])))
                else:
                    V_not_agree = choice(
                        get_all_conjunctive([("pres", "1"), ("3sg", "1")], get_all("root", V_agree["root"])))
            else:
                V_not_agree = V_agree

            try:
                if subj["pl"] == "1":
                    S_arg = N_to_DP_mutate(choice(get_matches_of(V_not_agree, "arg_1", get_matches_of(subj, "arg_1", all_singular_nouns))))
                    pass
                else:
                    S_arg = N_to_DP_mutate(choice(get_matches_of(V_not_agree, "arg_1", get_matches_of(subj, "arg_1", all_plural_nouns))))
                    pass
            except Exception:
                continue

        Auxs = require_aux_agree(V_agree, subj)
        Aux_agree = Auxs["aux_agree"]
        Aux_not_agree = Auxs["aux_nonagree"]
        V_args = verb_args_from_verb(V_agree, subj=subj, aux=Aux_agree)

        if V_agree["finite"] == "1":
            prefix = "%s %s %s" % (D[0], subj[0], S_arg[0])
            word_good = V_agree[0]
            word_bad = V_not_agree[0]
        else:
            prefix = "%s %s %s" % (D[0], subj[0], S_arg[0])
            word_good = Aux_agree
            word_bad = Aux_not_agree

        data = {
            "sentence_good": "%s %s %s %s %s %s." % (D[0], subj[0], S_arg[0], Aux_agree, V_agree[0], join_args(V_args["args"])),
            "sentence_bad": "%s %s %s %s %s %s." % (D[0], subj[0], S_arg[0], Aux_not_agree, V_not_agree[0], join_args(V_args["args"])),
            "one_prefix_prefix": prefix,
            "one_prefix_word_good": word_good,
            "one_prefix_word_bad": word_bad
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
