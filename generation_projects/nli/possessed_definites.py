from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *
from utils.string_utils import string_beautify
import inflect

class PossessGenerator(data_generator.NLIGenerator):
    def __init__(self):
        super().__init__(
            uid="possessed_definites"
        )
        # bad_nouns = reduce(np.union1d, (get_all("arg_1", "animate=1", self.all_relational_nouns), get_all("properNoun", "1")))
        self.safe_nouns = np.union1d(np.setdiff1d(self.all_nouns, self.all_animate_nouns), all_relational_poss_nouns)

    def sample(self):
        # John's sister is tall
        # N1  's N2     VP
        # John has  a sister
        # N1   HAVE D N2

        N1 = N_to_DP_mutate(choice(get_all("animate", "1", self.all_nominals)))
        N2 = choice(self.safe_nouns)
        s_poss = "'" if N1["pl"] == "1" and N1[0][-1] == "s" else "'s"
        V = choice(get_matched_by(N2, "arg_1", self.all_verbs))
        v_args = verb_args_from_verb(V, subj=N2)
        try:
            VP = " ".join([v_args["aux"][0],
                           V[0]] +
                          [x[0] for x in v_args["args"]])
        except KeyError:
            pass
        D = "" if N2["pl"] == "1" or N2["mass"] == "1" else "a"
        HAVE = "has" if N1["sg"] == "1" else "have"
        data = {
            "sentence_1": "%s%s %s %s." % (N1[0], s_poss, N2[0], VP),
            "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0])
        }
        return data, data["sentence_1"]

generator = PossessGenerator()
generator.generate_paradigm(number_to_generate=50, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
