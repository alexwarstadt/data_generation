from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.msgs.person_helper

class MyGenerator(generation_projects.msgs.person_helper.PersonGenerator):
    def __init__(self):
        super().__init__(uid="person_absolute_token_position",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is the pronoun 1st person?",
                         surface_feature_type="absolute token position",
                         surface_feature_description="Is the first word of the sentence 'the'?",
                         control_paradigm=False)

        self.safe_dets = np.setdiff1d(get_all("category_2", "D"), get_all("expression", "the"))
        self.animate_common_nouns = np.intersect1d(all_common_nouns, all_animate_nouns)

    def sample(self):
        # Training 1/1
        # The man thinks    that I     found      every cat .
        # Dt  NP1 cp_verb_1 THAT first verb_first Da    NP2 .

        # Training 0/0
        # Every man thinks    that they      found          the cat .
        # Da    NP1 cp_verb_1 THAT non_first verb_non_first Dt  NP2 .

        # Test 1/0
        # Every man thinks    that the cat found  me        .
        # Da    NP1 cp_verb_1 THAT Dt  NP2 verb_2 first_acc .

        # Test 0/1
        # The man thinks    that every cat found  them          .
        # Dt  NP1 cp_verb_1 THAT Da    NP2 verb_2 non_first_acc .

        # Control 1/1
        # The man thinks    that every cat found  me        .
        # Dt  NP1 cp_verb_1 THAT Da    NP2 verb_2 first_acc .

        # Control 0/0
        # Every man thinks    that the cat found  them          .
        # Da    NP1 cp_verb_1 THAT Dt  NP2 verb_2 non_first_acc .

        first, non_first, first_acc, non_first_acc = self.get_pronouns()
        Dt = get_all("expression", "the")[0]
        NP1 = choice(self.animate_common_nouns)
        #Da stands for Determiner_alternative
        Da = choice(get_matched_by(NP1,"arg_1", self.safe_dets))
        NP2 = choice(get_matches_of(Da, "arg_1", self.animate_common_nouns), avoid=NP1)

        cp_verb = choice(self.cp_verb)
        cp_verb_aux = return_aux(cp_verb, first)
        cp_verb_1 = re_conjugate(cp_verb, NP1, cp_verb_aux)

        verb = choice(self.trans_verb)
        verb_aux = return_aux(verb, NP1)
        verb_2 = re_conjugate(verb, NP2, verb_aux)
        verb_first = re_conjugate(verb, first, verb_aux)
        verb_non_first = re_conjugate(verb, non_first, verb_aux)

        track_sentence = [
                (NP1[0], cp_verb[0], verb[0], NP2[0], first[0]), #training 1/1
                (NP1[0], cp_verb[0], verb[0], NP2[0], non_first[0]), #training 0/0
                (NP1[0], cp_verb[0], verb[0], NP2[0], first_acc[0]), #Test 1/0
                (NP1[0], cp_verb[0], verb[0], NP2[0], non_first_acc[0]), #Test 0/1
                (NP1[0], cp_verb[0], verb[0], NP2[0], first_acc[0]), #Control 1/1
                (NP1[0], cp_verb[0], verb[0], NP2[0], non_first_acc[0]) #Control 0/0
            ]

        data = self.build_paradigm(
            training_1_1="%s %s %s that %s %s %s %s" % (Dt[0], NP1[0], cp_verb_1[0], first[0], verb_first[0], Da[0], NP2[0]),
            training_0_0="%s %s %s that %s %s %s %s" % (Da[0], NP1[0], cp_verb_1[0], non_first[0], verb_non_first[0], Dt[0],  NP2[0]),
            test_1_0="%s %s %s that %s %s %s %s" % (Da[0], NP1[0], cp_verb_1[0], Dt[0],  NP2[0], verb_2[0], first_acc[0]),
            test_0_1="%s %s %s that %s %s %s %s" % (Dt[0], NP1[0], cp_verb_1[0], Da[0], NP2[0], verb_2[0], non_first_acc[0]),
            control_1_1="%s %s %s that %s %s %s %s" % (Dt[0], NP1[0], cp_verb_1[0], Da[0], NP2[0], verb_2[0], first_acc[0]),
            control_0_0="%s %s %s that %s %s %s %s" % (Da[0], NP1[0], cp_verb_1[0], Dt[0], NP2[0], verb_2[0], non_first_acc[0])
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/msgs/" + generator.uid)
