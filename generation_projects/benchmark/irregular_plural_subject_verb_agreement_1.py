from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.vocab_sets import *

class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="morphology",
                         linguistics="subject_verb_agreement",
                         uid="irregular_plural_subject_verb_agreement_1",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.safe_nouns = get_all_conjunctive([("category", "N"), ("irrpl", "1"), ("sgequalspl", "")])
        self.safe_verbs = reduce(np.union1d, (get_all("pres", "1", all_verbs),
                                              get_all("ing", "1", all_verbs),
                                              get_all("en", "1", all_verbs)))
        ambiguous_verbs = list(filter(lambda verb: len(list(filter(lambda x: x["root"] == verb["root"]
                                                                             and x["past"] == "1"
                                                                             and x["expression"] == verb["expression"],
                                      all_verbs))) > 0,
                                 get_all("pres", "1", all_verbs)))
        self.safe_verbs = np.setdiff1d(self.safe_verbs, ambiguous_verbs)

    def sample(self):
        # The cat is        eating    food
        #     N1  aux_agree V1_agree  args
        # The cat are          eating        food
        #     N1  aux_nonagree V1_nonagree   args

        N1 = N_to_DP_mutate(choice(self.safe_nouns))
        V1_agree = choice(get_matched_by(N1, "arg_1", self.safe_verbs))
        if V1_agree["pres"] == "1":
            V1_nonagree = get_mismatch_verb(V1_agree)
        else:
            V1_nonagree = V1_agree
        args = join_args(verb_args_from_verb(V1_agree, aux=False)["args"])
        auxes = require_aux_agree(V1_agree, N1)
        aux_agree = auxes["aux_agree"]
        aux_nonagree = auxes["aux_nonagree"]

        if aux_agree == "":
            word_agree = V1_agree[0].strip().split(" ")[0]
            word_nonagree = V1_nonagree[0].strip().split(" ")[0]
        else:
            word_agree = aux_agree
            word_nonagree = aux_nonagree

        data = {
            "sentence_good": "%s %s %s %s." % (N1[0], aux_agree, V1_agree[0], args),
            "sentence_bad": "%s %s %s %s." % (N1[0], aux_nonagree, V1_nonagree[0], args),
            "one_prefix_prefix": "%s" % (N1[0]),
            "one_prefix_word_good": word_agree,
            "one_prefix_word_bad": word_nonagree,
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
