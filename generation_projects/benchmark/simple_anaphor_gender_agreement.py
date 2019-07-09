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
        self.all_safe_nouns = np.setdiff1d(self.all_singular_nouns, self.all_singular_neuter_animate_nouns)
        # self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, self.all_common_nouns)
        self.all_singular_reflexives = reduce(np.union1d, (get_all("expression", "himself"),
                                                           get_all("expression", "herself"),
                                                           get_all("expression", "itself")))
        self.category = "agreement"
        self.field = "morphology"
        self.linguistics = "anaphor_agreement"
        self.UID = "simple_anaphor_gender_agreement"

    def sample(self):
        # John knows himself
        # John knows itself

        V1 = choice(self.all_refl_preds)
        N1 = choice(get_matches_of(V1, "arg_1", self.all_safe_nouns))
        N1 = N_to_DP_mutate(N1)
        refl_match = choice(get_matched_by(N1, "arg_1", self.all_reflexives))
        refl_mismatch = choice(np.setdiff1d(self.all_singular_reflexives, [refl_match]))

        V1 = conjugate(V1, N1)

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












