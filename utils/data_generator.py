from utils.conjugate import *
from utils.string_utils import string_beautify
# from random import choice
import numpy as np
from utils.randomize import choice








class Generator:
    def __init__(self):
        self.category = None
        self.field = None
        self.linguistics = None
        self.UID = None

        # NOUNS
        self.all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
        self.all_singular_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1"), ("sg", "1")])
        self.all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
        self.all_documents = get_all_conjunctive([("category", "N"), ("document", "1")])
        self.all_gendered_nouns = np.union1d(get_all("gender", "m"), get_all("gender", "f"))
        self.all_singular_neuter_animate_nouns = get_all_conjunctive(
            [("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
        self.all_plural_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1"), ("pl", "1")])
        self.all_plural_animate_nouns = np.intersect1d(self.all_animate_nouns, self.all_plural_nouns)
        self.all_common_nouns = get_all_conjunctive([("category", "N"), ("properNoun", "0")])

        # VERBS
        self.all_transitive_verbs = get_all("category", "(S\\NP)/NP")
        self.all_anim_anim_verbs = get_matched_by(choice(self.all_animate_nouns), "arg_1",
                                             get_matched_by(choice(self.all_animate_nouns), "arg_2", self.all_transitive_verbs))
        self.all_doc_doc_verbs = get_matched_by(choice(self.all_documents), "arg_1",
                                           get_matched_by(choice(self.all_documents), "arg_2", self.all_transitive_verbs))
        self.all_refl_preds = np.union1d(self.all_anim_anim_verbs, self.all_doc_doc_verbs)
        self.all_non_plural_transitive_verbs = np.setdiff1d(self.all_transitive_verbs, get_all_conjunctive([("pres", "1"), ("3sg", "0")]))
        self.all_plural_transitive_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "0")], self.all_transitive_verbs)
        self.all_singular_transitive_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "1")], self.all_transitive_verbs)

        # OTHER
        self.all_frequent_quantifiers = get_all("frequent", "1", get_all("category", "(S/(S\\NP))/N"))
        self.all_common_dets = np.append(get_all("expression", "the"),
                                    np.append(get_all("expression", "a"), get_all("expression", "an")))
        self.all_relativizers = get_all("category_2", "rel")
        self.all_reflexives = get_all("category_2", "refl")
        self.all_ACCpronouns = get_all("category_2", "proACC")
        self.all_NOMpronouns = get_all("category_2", "proNOM")
        self.all_embedding_verbs = get_all("category_2", "V_embedding")
        return

    def make_metadata(self):
        return "category=%s-field=%s-linguistics_term=%s-UID=%s" % (self.category, self.field, self.linguistics, self.UID)

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
            output = open(absolute_path, "w")
        else:
            raise Exception("You need to give an output path")
        past_sentences = set()
        while len(past_sentences) < number_to_generate:
            metadata, judgments, sentences = self.sample()
            sentences = [string_beautify(s) for s in sentences]
            if sentences[0] not in past_sentences:
                for m, j, s in zip(metadata, judgments, sentences):
                    output.write("%s\t%d\t\t%s\n" % (m, j, s))
                past_sentences.add(sentences[0])