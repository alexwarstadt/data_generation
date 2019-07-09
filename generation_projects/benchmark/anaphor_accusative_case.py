from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify
from functools import reduce


class AnaphorGenerator(data_generator.Generator):
    def __init__(self):
        super().__init__()
        # self.all_safe_nouns = np.setdiff1d(self.all_singular_nouns, self.all_singular_neuter_animate_nouns)
        # self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, self.all_common_nouns)
        # self.all_singular_reflexives = reduce(np.union1d, (get_all("expression", "himself"),
        #                                                    get_all("expression", "herself"),
        #                                                    get_all("expression", "itself")))
        self.category = "agreement"
        self.field = "morphology"
        self.linguistics = "anaphor_agreement"
        self.UID = "anaphor_accusative_case"

    def sample(self):
        # It's himself that John likes.
        # It's himself that likes John.

        V1 = choice(self.all_refl_preds)
        N1 = choice(get_matches_of(V1, "arg_1", self.all_nouns))
        N1 = N_to_DP_mutate(N1)
        Rel = choice(get_matched_by(N1, "arg_1", self.all_relativizers))
        Refl = choice(get_matched_by(N1, "arg_1", self.all_reflexives))
        V1 = conjugate(V1, N1)

        metadata = [
            "%s-obj_extract=1" % (self.make_metadata()),
            "%s-obj_extract=0" % (self.make_metadata())
        ]
        judgments = [1, 0]
        sentences = [
            "It's %s %s %s %s." % (Refl[0], Rel[0], N1[0], V1[0]),
            "It's %s %s %s %s." % (Refl[0], Rel[0], V1[0], N1[0])
        ]
        return metadata, judgments, sentences


generator = AnaphorGenerator()
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/benchmark/%s.tsv" % generator.UID)












