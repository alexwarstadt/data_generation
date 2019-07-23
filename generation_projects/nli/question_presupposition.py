from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
import inflect

class PossessGenerator(data_generator.NLIGenerator):
    def __init__(self):
        super().__init__(
            uid="question_presupposition"
        )
        self.wh_words = ["why", "when", "where", "how"]

    def sample(self):
        # John knows where Bill read the book.
        # N    V_rog wh    S
        # Bill read the book.
        # S






        data = {
            "sentence_1": "%s%s %s %s." % (N1[0], s_poss, N2[0], VP),
            "sentence_2": "%s %s %s %s." % (N1[0], HAVE, D, N2[0])
        }
        return data, data["sentence_1"]

generator = PossessGenerator()
generator.generate_paradigm(number_to_generate=50, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
