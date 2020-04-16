from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper

class MyGenerator(generation_projects.inductive_biases.person_helper.PersonGenerator):
    def __init__(self):
        super().__init__(uid="person_lexical_content_repeated",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is the pronoun 1st person?",
                         surface_feature_type="lexical content",
                         surface_feature_description="is any word (a determiner) repeated?",
                         control_paradigm=False)

        self.safe_animate_common_nouns = np.intersect1d(all_common_nouns, all_animate_nouns)
    
    def sample(self):
        # Training 1/1
        # I     think         that every cat found  every dog .
        # first cp_verb_first THAT Dt    NP1 verb_1 Dt    NP2 .

        # Training 0/0
        # They      think             that every cat  found  a   dog .
        # non_first cp_verb_non_first THAT Dt    NP1  verb_1 D2  NP2 .

        # Test 1/0
        # Every cat thinks    that a   dog found  me        .
        # Dt    NP1 cp_verb_1 THAT D2  NP2 verb_2 first_acc .

        # Test 0/1
        # Every cat thinks    that every dog found  them          .
        # Dt    NP1 cp_verb_1 THAT Dt    NP2 verb_2 non_first_acc .

        # Control 1/1
        # Every cat thinks    that every dog found  me        .
        # Dt    NP1 cp_verb_1 THAT Dt    NP2 verb_2 first_acc .

        # Control 0/0
        # Every cat thinks    that a   dog found  them          .
        # Dt    NP1 cp_verb_1 THAT D2  NP2 verb_2 non_first_acc .

        first, non_first, first_acc, non_first_acc = self.get_pronouns()
        NP1 = choice(self.safe_animate_common_nouns)
        Dt = choice(get_matched_by(NP1, "arg_1", self.dets), avoid=get_all("expression", "that")[0])
        NP2 = choice(get_matches_of(Dt, "arg_1", self.safe_animate_common_nouns), avoid=np.array([get_all("expression", "that")[0],NP1]))
        D2 = choice(get_matched_by(NP2, "arg_1", self.dets), avoid=Dt)
        
        cp_verb = choice(self.cp_verb)
        cp_verb_aux = return_aux(cp_verb, first)
        cp_verb_first = re_conjugate(cp_verb, first, cp_verb_aux)
        cp_verb_non_first = re_conjugate(cp_verb, non_first, cp_verb_aux)
        cp_verb_1 = re_conjugate(cp_verb, NP1, cp_verb_aux)
        verb = choice(self.trans_verb)
        verb_aux = return_aux(verb, NP1)
        verb_1 = re_conjugate(verb, NP1, verb_aux)
        verb_2 = re_conjugate(verb, NP2, verb_aux)

        #Dt is taken as a content word in this script because it is closely related to the surface feature.
        track_sentence = [
                (first[0], cp_verb[0], Dt[0], NP1[0], verb[0], NP2[0]), #training 1/1
                (non_first[0], cp_verb[0], Dt[0], NP1[0], verb[0], NP2[0]), #training 0/0
                (Dt[0], NP1[0], cp_verb[0], NP2[0], verb[0], first_acc[0]), #Test 1/0
                (Dt[0], NP1[0], cp_verb[0], NP2[0], verb[0], non_first_acc[0]), #Test 0/1
                (Dt[0], NP1[0], cp_verb[0], NP2[0], verb[0], first_acc[0]), #Control 1/1
                (Dt[0], NP1[0], cp_verb[0], NP2[0], verb[0], non_first_acc[0]) #Control 0/0
            ]

        try:
            data = self.build_paradigm(
                training_1_1="%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0],Dt[0],NP1[0], verb_1[0], Dt[0], NP2[0]),
                training_0_0="%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], Dt[0], NP1[0], verb_1[0], D2[0], NP2[0]),
                test_1_0="%s %s %s that %s %s %s %s" % (Dt[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
                test_0_1="%s %s %s that %s %s %s %s" % (Dt[0], NP1[0], cp_verb_1[0], Dt[0], NP2[0], verb_2[0], non_first_acc[0]),
                control_1_1="%s %s %s that %s %s %s %s" % (Dt[0], NP1[0], cp_verb_1[0], Dt[0], NP2[0], verb_2[0], first_acc[0]),
                control_0_0="%s %s %s that %s %s %s %s" % (Dt[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
            )
        except:
            print(first[0], cp_verb_first[0],Dt[0],NP1[0], verb_1[0], Dt[0], NP2[0])
            print(first[0], cp_verb[0], Dt[0], NP1[0], verb[0], NP2[0])
        
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
