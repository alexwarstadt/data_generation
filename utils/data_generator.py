from utils.conjugate import *
from utils.string_utils import string_beautify
# from random import choice
from functools import reduce
import numpy as np
from utils.randomize import choice
import jsonlines


class Generator:
    def __init__(self):

        # NOUNS
        self.all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
        self.all_singular_nouns = get_all("sg", "1", self.all_nouns)
        self.all_singular_count_nouns = get_all("mass", "0", self.all_singular_nouns)
        self.all_animate_nouns = get_all("animate", "1", self.all_nouns)
        self.all_inanimate_nouns = get_all("animate", "0", self.all_nouns)
        self.all_documents = get_all_conjunctive([("category", "N"), ("document", "1")])
        self.all_gendered_nouns = np.union1d(get_all("gender", "m"), get_all("gender", "f"))
        self.all_singular_neuter_animate_nouns = get_all_conjunctive(
            [("category", "N"), ("sg", "1"), ("animate", "1"), ("gender", "n")])
        self.all_plural_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1"), ("pl", "1")])
        self.all_plural_animate_nouns = np.intersect1d(self.all_animate_nouns, self.all_plural_nouns)
        self.all_common_nouns = get_all_conjunctive([("category", "N"), ("properNoun", "0")])
        self.all_relational_nouns = get_all("category", "N/NP")
        self.all_nominals = get_all("noun", "1")

        # VERBS
        self.all_transitive_verbs = get_all("category", "(S\\NP)/NP")
        self.all_intransitive_verbs = get_all("category", "S\\NP")
        self.all_anim_anim_verbs = get_matched_by(choice(self.all_animate_nouns), "arg_1",
                                             get_matched_by(choice(self.all_animate_nouns), "arg_2", self.all_transitive_verbs))
        self.all_doc_doc_verbs = get_matched_by(choice(self.all_documents), "arg_1",
                                           get_matched_by(choice(self.all_documents), "arg_2", self.all_transitive_verbs))
        self.all_refl_nonverbal_predicates = np.extract([x["arg_1"] == x["arg_2"] for x in get_all("category_2", "Pred")], get_all("category_2", "Pred"))
        self.all_refl_preds = reduce(np.union1d, (self.all_anim_anim_verbs, self.all_doc_doc_verbs))
        self.all_non_plural_transitive_verbs = np.extract(["sg=0" not in x["arg_1"] and "pl=1" not in x["arg_1"] for x in self.all_transitive_verbs], self.all_transitive_verbs)
        self.all_plural_transitive_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "0")], self.all_transitive_verbs)
        self.all_singular_transitive_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "1")], self.all_transitive_verbs)
        self.all_non_finite_transitive_verbs = get_all("finite", "0", self.all_transitive_verbs)
        self.all_non_finite_intransitive_verbs = get_all("finite", "0", self.all_intransitive_verbs)
        self.all_verbs = get_all("verb", "1")

        # OTHER
        self.all_quantifiers = get_all("category", "(S/(S\\NP))/N")
        self.all_frequent_quantifiers = get_all("frequent", "1", self.all_quantifiers)
        self.all_quantifiers = get_all("category", "(S/(S\\NP))/N")
        self.all_common_dets = np.append(get_all("expression", "the"),
                                    np.append(get_all("expression", "a"), get_all("expression", "an")))
        self.all_relativizers = get_all("category_2", "rel")
        self.all_reflexives = get_all("category_2", "refl")
        self.all_ACCpronouns = get_all("category_2", "proACC")
        self.all_NOMpronouns = get_all("category_2", "proNOM")
        self.all_embedding_verbs = get_all("category_2", "V_embedding")
        self.all_wh_words = get_all("category", "NP_wh")
        self.all_demonstratives = np.append(get_all("expression", "this"),
                            np.append(get_all_conjunctive([("category_2", "D"),("expression", "that")]),
                                    np.append(get_all("expression", "these"), get_all("expression", "those"))))
        self.data_fields = None
        return

    def sample(self):
        data = None
        track_sentence = None
        return data, track_sentence

    def make_metadata_dict(self):
        return {}


    def generate_paradigm(self, number_to_generate=10, rel_output_path=None, absolute_path=None):
        if rel_output_path is not None:
            project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
            output = open(os.path.join(project_root, rel_output_path), "w")
        elif absolute_path is not None:
            output = open(absolute_path, "w")
        else:
            raise Exception("You need to give an output path")
        past_sentences = set()
        generated_data = []
        constant_data = self.make_metadata_dict()
        while len(past_sentences) < number_to_generate:
            new_data, track_sentence = self.sample()
            if track_sentence not in past_sentences:
                past_sentences.add(track_sentence)
                for field in self.data_fields:
                    if field in new_data:
                        new_data[field] = string_beautify(new_data[field])
                        new_data.update(constant_data)
                generated_data.append(new_data)
        jsonlines.Writer(output).write_all(generated_data)


class BenchmarkGenerator(Generator):
    def __init__(self,
                 category: str,
                 field: str,
                 linguistics: str,
                 uid: str,
                 simple_lm_method: bool,
                 one_prefix_method: bool,
                 two_prefix_method: bool,
                 lexically_identical: bool):
        super().__init__()
        self.category = category
        self.field = field
        self.linguistics = linguistics
        self.uid = uid
        self.simple_lm_method = simple_lm_method
        self.one_prefix_method = one_prefix_method
        self.two_prefix_method = two_prefix_method
        self.lexically_identical = lexically_identical
        self.data_fields = ["sentence_good", "sentence_bad", "one_prefix_prefix", "two_prefix_prefix_good", "two_prefix_prefix_bad"]

    def make_metadata_dict(self):
        """
        (non token-specific metadata is in class fields, e.g. self.field=syntax)
        :param extra_metadata: token-specific metadata, e.g. one_prefix_word_1="the" 
        :return: join metadata
        """
        metadata = {
            "category": self.category,
            "field": self.field,
            "linguistics_term": self.linguistics,
            "UID": self.uid,
            "simple_LM_method": self.simple_lm_method,
            "one_prefix_method": self.one_prefix_method,
            "two_prefix_method": self.two_prefix_method,
            "lexically_identical": self.lexically_identical
        }
        return metadata

class NLIGenerator(Generator):
    def __init__(self,
                 uid):
        super().__init__()
        self.uid = uid
        self.data_fields = ["sentence_1", "sentence_2"]


    def make_metadata_dict(self):
        metadata = {
            "UID": self.uid
        }
        return metadata


class PresuppositionGenerator(Generator):

    def __init__(self,
                 uid):
        super().__init__()
        self.uid = uid
        self.data_fields = ["sentence1", "sentence2"]

    def generate_paradigm(self, number_to_generate=10, rel_output_path=None, absolute_path=None):
        if rel_output_path is not None:
            project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
            output = open(os.path.join(project_root, rel_output_path), "w")
        elif absolute_path is not None:
            output = open(absolute_path, "w")
        else:
            raise Exception("You need to give an output path")
        past_sentences = set()
        generated_data = []
        constant_data = self.make_metadata_dict()
        while len(past_sentences) < number_to_generate:
            new_data, track_sentence = self.sample()
            if track_sentence not in past_sentences:
                past_sentences.add(track_sentence)
                for line in new_data:
                    for field in self.data_fields:
                        if field in line:
                            line[field] = string_beautify(line[field])
                            line.update(constant_data)
                    generated_data.append(line)
        jsonlines.Writer(output).write_all(generated_data)

