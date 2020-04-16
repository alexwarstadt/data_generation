from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper

class MyGenerator(generation_projects.inductive_biases.person_helper.PersonGenerator):
    def __init__(self):
        super().__init__(uid="person_lexical_content_the",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is the pronoun 1st person?",
                         surface_feature_type="lexical content",
                         surface_feature_description="Is the word 'the' present?",
                         control_paradigm=False)

        # animate = get_all("animate", "1")
        # self.nom_pronoun = get_all("category_2", "nom_pronoun", animate)
        # self.acc_pronoun = get_all("category_2", "acc_pronoun", animate)
        # self.poss_det = get_all("category_2", "poss_det", animate)
        # self.poss_pronoun = get_all("category_2", "poss_pronoun", animate)
        # self.first = get_all("person", "1")
        # self.safe_verbs = get_all("ing", "0", all_verbs)   # This is because auxiliaries "be" and "have" for 1st and 2nd person not implemented
        # self.cp_verb = get_all("category", "(S\\NP)/S", self.safe_verbs)
        # self.trans_verb = np.intersect1d(self.safe_verbs, all_anim_anim_verbs)
        self.safe_dets = np.setdiff1d(get_all("category_2", "D"), get_all("expression", "the"))
        # self.possessible_animates = get_all("category", "N\\NP[poss]")
        self.animate_common_nouns = np.intersect1d(all_common_nouns, all_animate_nouns)

    def sample(self):
        # Training 1/1
        # I     think         that    John found  the cat.
        # first cp_verb_first THAT D1 NP1  verb_1 THE NP2

        # Training 0/0
        # They      think             that    John found  every cat.
        # non_first cp_verb_non_first THAT D1 NP1  verb_1 D2    NP2

        # Test 1/0
        #    John thinks    that every cat found  me.
        # D1 NP1  cp_verb_1 THAT D2    NP2 verb_2 first_acc

        # Test 0/1
        #    John thinks    that the cat found  them.
        # D1 NP1  cp_verb_1 THAT THE NP2 verb_2 non_first_acc

        # Control 1/1
        #    John thinks    that the cat found  me.
        # D1 NP1  cp_verb_1 THAT THE NP2 verb_2 first_acc

        # Control 0/0
        #    John thinks    that every cat found  them.
        # D1 NP1  cp_verb_1 THAT D2    NP2 verb_2 non_first_acc

        first, non_first, first_acc, non_first_acc = self.get_pronouns()
        NP1 = choice(all_animate_nouns)
        NP2 = choice(self.animate_common_nouns, avoid=NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", self.safe_dets))
        D2 = choice(get_matched_by(NP2, "arg_1", self.safe_dets))
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
                (NP1[0], cp_verb[0], NP2[0], verb[0], first_acc[0]), #Control 1/1
                (NP1[0], cp_verb[0], NP2[0], verb[0], non_first_acc[0]) #Control 0/0
            ]

        data = self.build_paradigm(
            training_1_1="%s %s that %s %s %s the %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], NP2[0]),
            training_0_0="%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            test_1_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            test_0_1="%s %s %s that the %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], NP2[0], verb_2[0], non_first_acc[0]),
            control_1_1="%s %s %s that the %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], NP2[0], verb_2[0], first_acc[0]),
            control_0_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
