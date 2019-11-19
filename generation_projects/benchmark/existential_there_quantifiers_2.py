from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="semantics",
                         linguistics="quantifiers",
                         uid="existential_there_quantifiers_2",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)
        bad_quantifiers_str = ["all", "most", "every", "each"]
        self.bad_quantifiers = reduce(np.union1d, [get_all("expression", s, all_quantifiers) for s in bad_quantifiers_str])
        bad_subjs = reduce(np.union1d, (all_relational_poss_nouns, all_proper_names, get_all("category", "NP")))
        self.safe_subjs = np.setdiff1d(all_nominals, bad_subjs)

    def sample(self):
        # Every monster is  there eating children.
        # D     subj    aux THERE VP
        # There is  every monster eating children.
        # THERE aux D     subj    VP

        subj = N_to_DP_mutate(choice(self.safe_subjs), determiner=False)
        D = choice(get_matched_by(subj, "arg_1", self.bad_quantifiers))
        V = choice(get_matched_by(subj, "arg_1", all_ing_verbs))
        allow_negated = D[0] != "no" and  D[0] != "some"
        args = verb_args_from_verb(V, subj=subj, allow_negated=allow_negated)
        VP = V_to_VP_mutate(V, args=args, aux=False)

        data = {
            "sentence_good": "%s %s %s there %s." % (D[0], subj[0], args["aux"][0], VP[0]),
            "sentence_bad": "There %s %s %s %s." % (args["aux"][0], D[0], subj[0], VP[0])
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
