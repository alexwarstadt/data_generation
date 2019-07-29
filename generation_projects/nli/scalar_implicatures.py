from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *
from utils.string_utils import string_beautify
#import inflect

class SIGenerator(data_generator.NLIGenerator):
    def __init__(self):
        super().__init__(
            uid="scalar_implicatures"
        )
        # bad_nouns = reduce(np.union1d, (get_all("arg_1", "animate=1", self.all_relational_nouns), get_all("properNoun", "1")))
        #self.safe_nouns = np.union1d(np.setdiff1d(self.all_nouns, self.all_animate_nouns), all_relational_poss_nouns)

    def sample(self):

        W="some"
        S="all"

        C1 = [W, "not "+S]
        C2 = C1[::-1]
        C3= [W,S]
        C4= C3[::-1]
        C5= ["not "+S,"not "+W]
        C6 = C4[::-1]
        C7 = [S,"not "+W]
        C8 = C7[::-1]
        C9 = [W,"not "+W]
        C10 = C9[::-1]
        C11 = [S,"not "+S]
        C12 = C11[::-1]

        C_set = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12]



        N = N_to_DP_mutate(choice(get_all("animate", "1", self.all_nominals)))
        V = choice(get_matched_by(N, "arg_1", self.all_verbs))
        v_args = verb_args_from_verb(V, subj=N)
        try:
            VP = " ".join([v_args["aux"][0],
                           V[0]] +
                          [x[0] for x in v_args["args"]])
        except KeyError:
            pass

        data=[]
        for i in range(12):
            C = C_set[i]

            sentence_pair = {
                "sentence_1": "%s %s %s." % (C[0], N[0], V),
                "sentence_2": "%s %s %s." % (C[1], N[0], V)
            }
            data.append(sentence_pair)

            return

generator = SIGenerator()
generator.generate_paradigm(number_to_generate=1, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
