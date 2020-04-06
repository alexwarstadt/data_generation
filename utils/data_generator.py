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
    """
    "Abstract" Class that is instantiated by individual data generation scripts
    """
    def __init__(self):
        self.data_fields = None
        return

    def sample(self):
        """
        samples a single minimal pair/set of a paradigm
        :return: the dictionary containing the data, and a representative sentence to avoid generating duplicates
        """
        data = None
        track_sentence = None
        return data, track_sentence

    def make_metadata_dict(self):
        return {}

    def make_logger(self, metadata):
        """
        creates a logger for the generation project
        :param metadata: metadata dict for the generation project
        :return: None
        """
        project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
        log_name = 'generation-%s-%s.log' % (metadata["UID"], str(datetime.datetime.now()))
        logging.basicConfig(filename=os.path.join(project_root, "logs/benchmark", log_name), level=logging.DEBUG)

    def log_exception(self, e):
        logging.debug(self.get_stack_trace(e) + "\n")

    def get_stack_trace(self, e):
        return "".join(traceback.format_tb(e.__traceback__)) + str(e)

    def generate_paradigm(self, number_to_generate=1000, rel_output_path=None, absolute_path=None):
        """
        Contains the main loop for generating a full dataset for a given paradigm.
        Also contains exception handling: some exceptions are tolerated because sometimes no matching arguments can be found,
        but if at least 10% of cases have an exception, it terminates since this is probably an issue in the code, and
        it could cause an infinite loop otherwise.
        :param number_to_generate: number of minimal pairs/sets to generate
        :param rel_output_path: relative path of output file
        :param absolute_path: absolute path of output file
        :return: None
        """
        if rel_output_path is not None:
            project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
            output = open(os.path.join(project_root, rel_output_path), "w")
        elif absolute_path is not None:
            output = open(absolute_path, "w")
        else:
            raise Exception("You need to give an output path")
        past_sentences = set()
        generated_data = []
        pairID = 0
        error_counter = 0
        constant_data = self.make_metadata_dict()
        print("Generating data for " + constant_data["UID"])
        self.make_logger(constant_data)
        output_writer = jsonlines.Writer(output, flush=True)
        while len(past_sentences) < number_to_generate:
            try:
                new_data, track_sentence = self.sample()
                if track_sentence not in past_sentences:
                    past_sentences.add(track_sentence)
                    for field in self.data_fields:
                        if field in new_data:
                            new_data[field] = string_beautify(new_data[field])
                            new_data.update(constant_data)
                    new_data["pairID"] = str(pairID)
                    pairID += 1
                    if pairID % 100 == 0:
                        print("%d sentences generated" % pairID)
                    output_writer.write(new_data)
            except Exception as e:
                self.log_exception(e)
                print(self.get_stack_trace(e))
                error_counter += 1
                if error_counter > number_to_generate // 5:
                    pass
                    # raise Exception("Over 20\% of samples result in errors. You should fix this.")
        jsonlines.Writer(output).write_all(generated_data)


class BenchmarkGenerator(Generator):
    """
    Data generator for BLiMP.
    """
    def __init__(self,
                 field: str,
                 linguistics: str,
                 uid: str,
                 simple_lm_method: bool,
                 one_prefix_method: bool,
                 two_prefix_method: bool,
                 lexically_identical: bool,
                 category: str=None):
        super().__init__()
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
            "field": self.field,
            "linguistics_term": self.linguistics,
            "UID": self.uid,
            "simple_LM_method": self.simple_lm_method,
            "one_prefix_method": self.one_prefix_method,
            "two_prefix_method": self.two_prefix_method,
            "lexically_identical": self.lexically_identical
        }
        return metadata


class ScalarImplicatureGenerator(Generator):
    """
    Data generator for IMPPRES implicatures
    """
    def __init__(self,
                 uid):
        super().__init__()
        self.uid = uid
        self.data_fields = ["sentence1", "sentence2"]

    def log_exception(self, e):
        logging.debug("".join(traceback.format_tb(e.__traceback__)) + str(e) + "\n")

    def generate_paradigm(self, number_to_generate=12, rel_output_path=None, absolute_path=None):
        if rel_output_path is not None:
            project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-1])
            output = open(os.path.join(project_root, rel_output_path), "w")
        elif absolute_path is not None:
            output = open(absolute_path, "w")
        else:
            raise Exception("You need to give an output path")
        past_sentences = []
        generated_data = []
        constant_data = self.make_metadata_dict()
        # error_counter = 0
        #print(len(past_sentences))

        while len(past_sentences) < number_to_generate:

            try:
                new_data, track_sentence = self.sample()
                print(track_sentence)

                if track_sentence not in past_sentences:

                    past_sentences.append(track_sentence)


                    for C in new_data:
                        for field in self.data_fields:
                            if field in C:
                                C[field] = string_beautify(C[field])
                                C.update(constant_data)
                        generated_data.append(C)
            except Exception as e:
                self.log_exception(e)
                print(self.get_stack_trace(e))
                # error_counter += 1
                # if error_counter >= number_to_generate // 10:
                #     raise Exception("Over 10\% of samples result in errors. You should fix this.")
        jsonlines.Writer(output).write_all(generated_data)


class PresuppositionGenerator(Generator):
    """
    Data generator for IMPPRES presuppositions
    """

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
        pairID = 0
        paradigmID = 0
        error_counter = 0
        constant_data = self.make_metadata_dict()
        self.make_logger(constant_data)
        output_writer = jsonlines.Writer(output, flush=True)
        while len(past_sentences) < number_to_generate:
            try:
                new_data, track_sentence = self.sample()
                if track_sentence not in past_sentences:
                    past_sentences.add(track_sentence)
                    for line in new_data:
                        for field in self.data_fields:
                            if field in line:
                                line[field] = string_beautify(line[field])
                                line.update(constant_data)
                        line["pairID"] = str(pairID) + line["gold_label"][0]
                        line["paradigmID"] = paradigmID
                        pairID += 1
                        output_writer.write(line)
                    paradigmID += 1
            except Exception as e:
                self.log_exception(e)
                print(self.get_stack_trace(e))
                error_counter += 1
                if error_counter >= number_to_generate // 10:
                    raise Exception("Over 10\% of samples result in errors. You should fix this.")


    def build_presupposition_paradigm(self, unembedded_trigger=None, negated_trigger=None, interrogative_trigger=None, modal_trigger=None, conditional_trigger=None,
                                      presupposition=None, negated_presupposition=None, neutral_presupposition=None):
        triggers = []
        if unembedded_trigger is not None:
            triggers.append((unembedded_trigger, "unembedded"))
        if negated_trigger is not None:
            triggers.append((negated_trigger, "negated"))
        if interrogative_trigger is not None:
            triggers.append((interrogative_trigger, "interrogative"))
        if modal_trigger is not None:
            triggers.append((modal_trigger, "modal"))
        if conditional_trigger is not None:
            triggers.append((conditional_trigger, "conditional"))

        presuppositions = []
        if presupposition is not None:
            presuppositions.append((presupposition, "positive", "entailment"))
        if negated_presupposition is not None:
            presuppositions.append((negated_presupposition, "negated", "contradiction"))
        if neutral_presupposition is not None:
            presuppositions.append((neutral_presupposition, "neutral", "neutral"))

        data = []
        for trigger in triggers:
            for presupposition in presuppositions:
                data.append({
                    "sentence1": trigger[0],
                    "sentence2": presupposition[0],
                    "trigger": trigger[1],
                    "presupposition": presupposition[1],
                    "gold_label": presupposition[2]
                })

        data.append({
            "sentence1": negated_trigger,
            "sentence2": unembedded_trigger,
            "trigger1": "negated",
            "trigger2": "unembedded",
            "gold_label": "contradiction",
            "control_item": True
        })

        for trigger2 in triggers[2:]:
            data.append({
                "sentence1": trigger2[0],
                "sentence2": unembedded_trigger,
                "trigger1": trigger2[1],
                "trigger2": "unembedded",
                "gold_label": "neutral",
                "control_item": True
            })
        return data

    def make_metadata_dict(self):
        """
        (non token-specific metadata is in class fields, e.g. self.field=syntax)
        :param extra_metadata: token-specific metadata, e.g. one_prefix_word_1="the" 
        :return: join metadata
        """
        metadata = {
            "UID": self.uid
        }
        return metadata


class InductiveBiasesGenerator(Generator):
    """
    Data generator for BLiMP.
    """
    def __init__(self,
                 uid: str,
                 linguistic_feature_type: str,
                 linguistic_feature_description: str,
                 surface_feature_type: str,
                 surface_feature_description: str,
                 control_paradigm: bool):
        super().__init__()
        self.uid = uid
        self.linguistic_feature_type = linguistic_feature_type
        self.linguistic_feature_description = linguistic_feature_description
        self.surface_feature_type = surface_feature_type
        self.surface_feature_description = surface_feature_description
        self.control_paradigm = control_paradigm
        self.data_fields = ["training_1_1", "training_0_0", "test_1_0", "test_0_1", "control_1_1", "control_0_0"]

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
        sentenceID = 0
        paradigmID = 0
        error_counter = 0
        constant_data = self.make_metadata_dict()
        self.make_logger(constant_data)
        output_writer = jsonlines.Writer(output, flush=True)
        while len(past_sentences) < number_to_generate:
            try:
                new_data, track_sentence = self.sample()
                if track_sentence not in past_sentences:
                    past_sentences.add(track_sentence)
                    for line in new_data:
                        line["sentence"] = string_beautify(line["sentence"])
                        line.update(constant_data)
                        line["sentenceID"] = "%s_%s_%s_%s" % (sentenceID, line["condition"], str(line["linguistic_feature_label"]), str(line["surface_feature_label"]))
                        line["paradigmID"] = paradigmID
                        sentenceID += 1
                        output_writer.write(line)
                    paradigmID += 1
            except Exception as e:
                self.log_exception(e)
                print(self.get_stack_trace(e))
                error_counter += 1
                if error_counter >= number_to_generate // 10:
                    raise Exception("Over 10\% of samples result in errors. You should fix this.")

    def make_metadata_dict(self):
        """
        (non token-specific metadata is in class fields, e.g. self.field=syntax)
        :param extra_metadata: token-specific metadata, e.g. one_prefix_word_1="the"
        :return: join metadata
        """
        metadata = {
            "UID": self.uid,
            "linguistic_feature_type": self.linguistic_feature_type,
            "linguistic_feature_description": self.linguistic_feature_description,
            "surface_feature_type": self.surface_feature_type,
            "surface_feature_description": self.surface_feature_description,
            "control_paradigm": self.control_paradigm
        }
        return metadata

    def build_paradigm(self, training_1_1, training_0_0, test_1_0, test_0_1, control_1_1=None, control_0_0=None):
        if not self.control_paradigm:
            data = [
                {"sentence": training_1_1,
                 "condition": "training",
                 "linguistic_feature_label": 1,
                 "surface_feature_label": 1},
                {"sentence": training_0_0,
                 "condition": "training",
                 "linguistic_feature_label": 0,
                 "surface_feature_label": 0},
                {"sentence": test_1_0,
                 "condition": "test",
                 "linguistic_feature_label": 1,
                 "surface_feature_label": 0},
                {"sentence": test_0_1,
                 "condition": "test",
                 "linguistic_feature_label": 0,
                 "surface_feature_label": 1},
                {"sentence": control_1_1,
                 "condition": "control",
                 "linguistic_feature_label": 1,
                 "surface_feature_label": 1},
                {"sentence": control_0_0,
                 "condition": "control",
                 "linguistic_feature_label": 0,
                 "surface_feature_label": 0},
            ]

        if self.control_paradigm and self.linguistic_feature_type is not None:
            data = [
                {"sentence": training_1_1,
                 "condition": "training",
                 "linguistic_feature_label": 1,
                 "surface_feature_label": None},
                {"sentence": training_0_0,
                 "condition": "training",
                 "linguistic_feature_label": 0,
                 "surface_feature_label": None},
                {"sentence": test_1_0,
                 "condition": "test",
                 "linguistic_feature_label": 1,
                 "surface_feature_label": None},
                {"sentence": test_0_1,
                 "condition": "test",
                 "linguistic_feature_label": 0,
                 "surface_feature_label": None},
            ]
        elif self.control_paradigm and not self.surface_feature_type is not None:
            data = [
                {"sentence": training_1_1,
                 "condition": "training",
                 "linguistic_feature_label": None,
                 "surface_feature_label": 1},
                {"sentence": training_0_0,
                 "condition": "training",
                 "linguistic_feature_label": None,
                 "surface_feature_label": 0},
                {"sentence": test_1_0,
                 "condition": "test",
                 "linguistic_feature_label": None,
                 "surface_feature_label": 1},
                {"sentence": test_0_1,
                 "condition": "test",
                 "linguistic_feature_label": None,
                 "surface_feature_label": 0},
            ]
        return data
