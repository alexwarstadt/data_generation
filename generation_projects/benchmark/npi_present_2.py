from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="semantics",
                         linguistics="npi_licensing",
                         uid="npi_present_2",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.safe_verbs = np.setdiff1d(all_verbs, all_ing_verbs)
        self.replace_ever = ["often", "really", "certainly", "clearly", "also"]

    def sample(self):
        # John should really leave.
        # subj aux    repl   vp
        # John should ever leave.
        # subj aux    EVER   vp

        V = choice(self.safe_verbs)
        args = verb_args_from_verb(V, allow_negated=False)
        VP = V_to_VP_mutate(V, aux=False, args=args)
        repl = choice(self.replace_ever)

        data = {
            "sentence_good": "%s %s %s %s." % (args["subj"][0], args["aux"][0], repl, VP[0]),
            "sentence_bad": "%s %s ever %s." % (args["subj"][0], args["aux"][0], VP[0]),
            "one_prefix_prefix": "%s %s" % (args["subj"][0], args["aux"][0]),
            "one_prefix_word_good": repl,
            "one_prefix_word_bad": "ever"
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
