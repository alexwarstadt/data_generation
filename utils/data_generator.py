from utils.conjugate import *
from utils.string_utils import string_beautify
# from random import choice
from functools import reduce
import numpy as np
from utils.randomize import choice
import jsonlines
import logging
import datetime
import traceback


class Generator:
    def __init__(self):
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
        log_name = 'generation-%s-%s.log' % (constant_data["UID"], str(datetime.datetime.now()))
        logging.basicConfig(filename=os.path.join("../../logs/benchmark", log_name), level=logging.DEBUG)

        while len(past_sentences) < number_to_generate:
            try:
                new_data, track_sentence = self.sample()
                if track_sentence not in past_sentences:
                    past_sentences.add(track_sentence)
                    for field in self.data_fields:
                        if field in new_data:
                            new_data[field] = string_beautify(new_data[field])
                            new_data.update(constant_data)
                    generated_data.append(new_data)
            except Exception as e:
                logging.debug("".join(traceback.format_tb(e.__traceback__)) + str(e) + "\n")
                continue
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

