from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from functools import reduce


class AnaphorGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(category="movement", field="syntax", linguistics="island_effects", UID="subject_island")
        self.category = "movement"
        self.field = "syntax"
        self.linguistics = "island_effects"
        self.UID = "subject_island"

    def sample(self):
        # What did John discuss a book about?
        # wh   aux NP   V       relN
        # What did a book about discuss John?
        # wh   aux relN         V       relN
        relN = N_to_DP_mutate(choice(self.all_relational_nouns))
        V = choice(get_matched_by(relN, "arg_1", self.all_refl_preds))
        Aux = return_aux(V, relN)


        metadata = [
            "%s-crucial_item=%s" % (self.make_metadata(), refl_match[0]),
            "%s-crucial_item=%s" % (self.make_metadata(), refl_mismatch[0])
        ]
        judgments = [1, 0]
        sentences = [
            "%s %s %s." % (N1[0], V1[0], refl_match[0]),
            "%s %s %s." % (N1[0], V1[0], refl_mismatch[0])
        ]
        return metadata, judgments, sentences


binding_generator = AnaphorGenerator()
binding_generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/benchmark/%s.tsv" % binding_generator.UID)












