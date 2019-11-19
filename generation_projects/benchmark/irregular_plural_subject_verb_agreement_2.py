from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from functools import reduce
from utils.vocab_sets import *

class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="morphology",
                         linguistics="subject_verb_agreement",
                         uid="irregular_plural_subject_verb_agreement_2",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        self.all_null_plural_nouns = get_all("sgequalspl", "1")
        self.all_missingPluralSing_nouns = get_all_conjunctive([("pluralform", ""), ("singularform", "")])
        self.all_unusable_nouns = np.union1d(self.all_null_plural_nouns, self.all_missingPluralSing_nouns)
        self.all_pluralizable_nouns = np.setdiff1d(all_common_nouns, self.all_unusable_nouns)
        self.all_irreg_nouns = get_all("irrpl", "1", self.all_pluralizable_nouns)
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
        # The cat       is        eating food
        #     N1_agree  aux_agree V1     N2
        # The cats        is          eating food
        #     N1_nonagree aux_agree   V1     N2

        if random.choice([True, False]):
            V1 = choice(np.intersect1d(self.safe_verbs, all_transitive_verbs))
            N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_nouns)))
        else:
            V1 = choice(np.intersect1d(self.safe_verbs, all_intransitive_verbs))
            N2 = " "
        N1_agree = choice(get_matches_of(V1, "arg_1", self.all_irreg_nouns))
        if N1_agree['sg'] == "1":
            N1_nonagree = N1_agree['pluralform']
        else:
            N1_nonagree = N1_agree['singularform']

        auxes = require_aux_agree(V1, N1_agree)
        aux_agree = auxes["aux_agree"]

        if aux_agree == "":
            word_agree = V1[0].strip().split(" ")[0]
        else:
            word_agree = aux_agree

        data = {
            "sentence_good": "The %s %s %s %s." % (N1_agree[0], aux_agree, V1[0], N2[0]),
            "sentence_bad": "The %s %s %s %s." % (N1_nonagree, aux_agree, V1[0], N2[0]),
            "two_prefix_prefix_good": "The %s" % (N1_agree[0]),
            "two_prefix_prefix_bad": "The %s" % (N1_nonagree),
            "two_prefix_word": word_agree
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
