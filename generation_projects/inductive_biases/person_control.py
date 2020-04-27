from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper

class MyGenerator(generation_projects.inductive_biases.person_helper.PersonGenerator):
    def __init__(self):
        super().__init__(uid="person_control",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is the pronoun 1st person?",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)


    def sample(self):
        # Training 1
        # I     think         that    John found  the cat.
        # first cp_verb_first THAT D1 NP1  verb_1 D2  NP2

        # Training 0
        # They      think             that    John found  the cat.
        # non_first cp_verb_non_first THAT D1 NP1  verb_1 D2  NP2

        # Test 1
        #    John thinks    that the cat found  me.
        # D1 NP1  cp_verb_1 THAT D2  NP2 verb_2 first_acc

        # Test 0
        #    John thinks    that the cat found  them.
        # D1 NP1  cp_verb_1 THAT D2  NP2 verb_2 non_first_acc

        first, non_first, first_acc, non_first_acc = self.get_pronouns()
        NP1 = choice(all_animate_nouns)
        NP2 = choice(all_animate_nouns, avoid=NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", self.dets))
        D2 = choice(get_matched_by(NP2, "arg_1", self.dets))
        cp_verb = choice(self.cp_verb)
        cp_verb_aux = return_aux(cp_verb, first)
        cp_verb_first = re_conjugate(cp_verb, first, cp_verb_aux)
        cp_verb_non_first = re_conjugate(cp_verb, non_first, cp_verb_aux)
        cp_verb_1 = re_conjugate(cp_verb, NP1, cp_verb_aux)
        verb = choice(self.trans_verb)
        verb_aux = return_aux(verb, NP1)
        verb_1 = re_conjugate(verb, NP1, verb_aux)
        verb_2 = re_conjugate(verb, NP2, verb_aux)

        track_sentence = [
                (first[0], cp_verb[0], NP1[0], verb[0], NP2[0]), #training 1/1
                (non_first[0], cp_verb[0], NP1[0], verb[0], NP2[0]), #training 0/0
                (NP1[0], cp_verb[0], NP2[0], verb[0], first_acc[0]), #Test 1/0
                (NP1[0], cp_verb[0], NP2[0], verb[0], non_first_acc[0]), #Test 0/1
            ]

        data = self.build_paradigm(
            training_1_1="%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            training_0_0="%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            test_1_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            test_0_1="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
