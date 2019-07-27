from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


class CSCGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="movement",
                         field="semantics",
                         linguistics="existential_there_and_definiteness",
                         uid="existential_there_and_definiteness",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)



    def sample(self):
        # A lady can not ever explain that the gloves would shrink
        # A lady can ever explain that the gloves would not shrink

        V = choice(self.safe_verbs)
        args = verb_args_from_verb(V, allow_negated=False)
        VP = V_to_VP_mutate(V, aux=False, args=args)
        repl = choice(self.replace_neg)

        data = {
            "sentence_good": "%s %s %s ever %s." % (args["subj"][0], args["aux"][0], repl, VP[0]),
            "sentence_bad": "%s %s not ever %s." % (args["subj"][0], args["aux"][0], VP[0])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
