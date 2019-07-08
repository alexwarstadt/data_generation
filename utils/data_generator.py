from utils.conjugate import *
from utils.string_utils import string_beautify
# from random import choice
import numpy as np
from utils.randomize import choice








class Generator:
    def __init__(self):
        self.all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
        self.all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
        self.all_documents = get_all_conjunctive([("category", "N"), ("document", "1")])
        self.all_gendered_nouns = np.union1d(get_all("gender", "m"), get_all("gender", "f"))
        self.all_singular_neuter_animate_nouns = get_all_conjunctive(
            [("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
        self.all_plural_animate_nouns = get_all("pl", "1", self.all_animate_nouns)
        self.all_frequent_quantifiers = get_all("frequent", "1", get_all("category", "(S/(S\\NP))/N"))
        self.all_reflexives = get_all("category_2", "refl")

        # gather potentially reflexive predicates
        self.all_transitive_verbs = get_all("category", "(S\\NP)/NP")
        self.all_anim_anim_verbs = get_matched_by(choice(self.all_animate_nouns), "arg_1",
                                             get_matched_by(choice(self.all_animate_nouns), "arg_2", self.all_transitive_verbs))
        self.all_doc_doc_verbs = get_matched_by(choice(self.all_documents), "arg_1",
                                           get_matched_by(choice(self.all_documents), "arg_2", self.all_transitive_verbs))
        self.all_refl_preds = np.union1d(self.all_anim_anim_verbs, self.all_doc_doc_verbs)
        self.all_common_dets = np.append(get_all("expression", "the"),
                                    np.append(get_all("expression", "a"), get_all("expression", "an")))
        self.all_relativizers = get_all("category_2", "rel")
        return

    def sample(self):
        metadata = None
        judgments = None
        sentences = None
        return metadata, judgments, sentences

    def generate_paradigm(self, number_to_generate=10, rel_output_path=None, absolute_path=None):
        if rel_output_path is not None:
            project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
            output = open(os.path.join(project_root, rel_output_path), "w")
        elif absolute_path is not None:
            output = absolute_path
        else:
            raise Exception("You need to give an output path")
        sentences = set()
        while len(sentences) < number_to_generate:
            metadata, judgments, sentences = self.sample()
            sentences = [string_beautify(s) for s in sentences]
            if sentences[0] not in sentences:
                for m, j, s in zip(metadata, judgments, sentences):
                    output.write("%s\t%d\t\t%s\n" % (m, j, s))
                sentences.add(sentences[0])