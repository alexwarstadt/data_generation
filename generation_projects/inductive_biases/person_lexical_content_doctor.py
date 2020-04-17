from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper

class MyGenerator(generation_projects.inductive_biases.person_helper.PersonGenerator):
    def __init__(self):
        super().__init__(uid="person_lexical_content_doctor",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is the pronoun 1st person?",
                         surface_feature_type="lexical content",
                         surface_feature_description="Is the word 'doctor' present?",
                         control_paradigm=False)

        self.safe_animate_common_nouns = np.setdiff1d(np.intersect1d(all_common_nouns, all_animate_nouns), get_all("expression", "doctor"))
        self.target_lexicon = get_all("expression", "doctor")[0]

    def sample(self):
        # Training 1/1
        # I     think         that    John found  the doctor.
        # first cp_verb_first THAT D1 NP1  verb_1 Dt  DOCTOR

        # Training 0/0
        # They      think             that    John found  the hairdresser.
        # non_first cp_verb_non_first THAT D1 NP1  verb_1 D2  NP2

        # Test 1/0
        #    John thinks    that the hairdresser found  me.
        # D1 NP1  cp_verb_1 THAT D2  NP2         verb_2 first_acc

        # Test 0/1
        #    John thinks    that the doctor found  them.
        # D1 NP1  cp_verb_1 THAT Dt  DOCTOR verb_t non_first_acc

        # Control 1/1
        #    John thinks    that the doctor found  me.
        # D1 NP1  cp_verb_1 THAT Dt  DOCTOR verb_t first_acc

        # Control 0/0
        #    John thinks    that the hairdresser found  them.
        # D1 NP1  cp_verb_1 THAT D2  NP2         verb_2 non_first_acc

        first, non_first, first_acc, non_first_acc = self.get_pronouns()
        NP1 = choice(np.setdiff1d(all_animate_nouns, get_all("expression", "doctor")))
        NP2 = choice(self.safe_animate_common_nouns, avoid=NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", self.dets))
        D2 = choice(get_matched_by(NP2, "arg_1", self.dets))
        Dt = choice(get_matched_by(self.target_lexicon, "arg_1", self.dets))
        cp_verb = choice(self.cp_verb)
        cp_verb_aux = return_aux(cp_verb, first)
        cp_verb_first = re_conjugate(cp_verb, first, cp_verb_aux)
        cp_verb_non_first = re_conjugate(cp_verb, non_first, cp_verb_aux)
        cp_verb_1 = re_conjugate(cp_verb, NP1, cp_verb_aux)
        verb = choice(self.trans_verb)
        verb_aux = return_aux(verb, NP1)
        verb_1 = re_conjugate(verb, NP1, verb_aux)
        verb_2 = re_conjugate(verb, NP2, verb_aux)
        # t for target_exicon
        verb_t = re_conjugate(verb, self.target_lexicon, verb_aux)

        track_sentence = [
                (first[0], cp_verb[0], NP1[0], verb[0]), #training 1/1
                (non_first[0], cp_verb[0], NP1[0], verb[0], NP2[0]), #training 0/0
                (NP1[0], cp_verb[0], NP2[0], verb[0], first_acc[0]), #Test 1/0
                (NP1[0], cp_verb[0], verb[0], non_first_acc[0]), #Test 0/1
                (NP1[0], cp_verb[0], verb[0], first_acc[0]), #Control 1/1
                (NP1[0], cp_verb[0], NP2[0], verb[0], non_first_acc[0]) #Control 0/0
            ]

        data = self.build_paradigm(
            training_1_1="%s %s that %s %s %s %s doctor" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], Dt[0]),
            training_0_0="%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            test_1_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            test_0_1="%s %s %s that %s doctor %s %s" % (D1[0], NP1[0], cp_verb_1[0], Dt[0], verb_t[0], non_first_acc[0]),
            control_1_1="%s %s %s that %s doctor %s %s" % (D1[0], NP1[0], cp_verb_1[0], Dt[0], verb_t[0], first_acc[0]),
            control_0_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=300, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
