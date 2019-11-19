from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="semantics",
                         linguistics="quantifiers",
                         uid="existential_there_quantifiers_1",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=False,
                         lexically_identical=False)
        good_quantifiers_sg_str = ["a", "an"]
        good_quantifiers_pl_str = ["no",
                                   "some",
                                   "few",
                                   "many"]
        bad_quantifiers_str = ["all", "most", "every", "each"]
        self.good_quantifiers_sg = reduce(np.union1d, [get_all("expression", s, all_quantifiers) for s in good_quantifiers_sg_str])
        self.good_quantifiers_pl = reduce(np.union1d, [get_all("expression", s, all_quantifiers) for s in good_quantifiers_pl_str])
        self.bad_quantifiers = reduce(np.union1d, [get_all("expression", s, all_quantifiers) for s in bad_quantifiers_str])
        bad_subjs = reduce(np.union1d, (all_relational_poss_nouns, all_proper_names, get_all("category", "NP")))
        self.safe_subjs = np.setdiff1d(all_nominals, bad_subjs)

    def sample(self):
        # There is  a       monster eating children.
        # THERE aux d_good  subj    VP
        # There is  every monster eating children.
        # THERE aux d_bad subj    VP

        subj = N_to_DP_mutate(choice(self.safe_subjs), determiner=False)
        d_good = choice(get_matched_by(subj, "arg_1", self.good_quantifiers_sg)) \
            if subj["sg"] == "1" \
            else choice(get_matched_by(subj, "arg_1", self.good_quantifiers_pl))
        d_bad = choice(get_matched_by(subj, "arg_1", self.bad_quantifiers))
        V = choice(get_matched_by(subj, "arg_1", all_ing_verbs))
        allow_negated = d_good[0] != "no" and d_good[0] != "some" and d_bad[0] != "no" and d_bad[0] != "some"
        args = verb_args_from_verb(V, subj=subj, allow_negated=allow_negated)
        VP = V_to_VP_mutate(V, args=args, aux=False)

        data = {
            "sentence_good": "There %s %s %s %s." % (args["aux"][0], d_good[0], subj[0], VP[0]),
            "sentence_bad": "There %s %s %s %s." % (args["aux"][0], d_bad[0], subj[0], VP[0])
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

