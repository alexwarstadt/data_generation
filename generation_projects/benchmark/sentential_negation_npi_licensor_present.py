from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="semantics",
                         linguistics="npi_licensing",
                         uid="sentential_negation_npi_licensor_present",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        self.safe_verbs = np.setdiff1d(all_non_finite_verbs, all_ing_verbs)
        self.replace_neg = ["really", "probably", "fortunately"]

    def sample(self):
        # A lady can not ever explain that the gloves would shrink
        # subj   aux NOT EVER VP
        # A lady can probably ever explain that the gloves would not shrink
        # subj   aux repl     EVER VP

        V = choice(self.safe_verbs)
        args = verb_args_from_verb(V, allow_negated=False)
        VP = V_to_VP_mutate(V, aux=False, args=args)
        repl = choice(self.replace_neg)

        data = {
            "sentence_good": "%s %s not ever %s." % (args["subj"][0], args["aux"][0], VP[0]),
            "sentence_bad": "%s %s %s ever %s." % (args["subj"][0], args["aux"][0], repl, VP[0]),
            "two_prefix_prefix_good": "%s %s not" % (args["subj"][0], args["aux"][0]),
            "two_prefix_prefix_bad": "%s %s %s" % (args["subj"][0], args["aux"][0], repl),
            "two_prefix_word": "ever"
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
