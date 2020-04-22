from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper
import generation_projects.inductive_biases.length_helper
from utils.exceptions import LengthHelperError

class MyGenerator(generation_projects.inductive_biases.person_helper.PersonGenerator, generation_projects.inductive_biases.length_helper.LengthHelper):
    def __init__(self):
        super().__init__(uid="person_length",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is the pronoun 1st person?",
                         surface_feature_type="length",
                         surface_feature_description="Is the sentence 20 words or longer?",
                         control_paradigm=False)

        self.antecedents = {}
        self.adverbs = get_all("category_2", "subordinating_conj")
        self.long_length = 18

        # self.safe_animate_common_nouns = np.setdiff1d(np.intersect1d(all_common_nouns, all_animate_nouns), get_all("expression", "doctor"))
        # self.singular_dets = get_all(get_matched_by(get_all("expression", "doctor"), "arg_1"), get_all("category_2", "D"))


    def sample(self):
        # Training 1/1
        # Because S_LONG, I     think         that    John found  the doctor.
        # Adv     S_LONG, first cp_verb_first THAT D1 NP1  verb_1 D2  DOCTOR

        # Training 0/0
        # Because S_SHORT, they      think             that    John found  the hairdresser.
        # Adv     S_SHORT, non_first cp_verb_non_first THAT D1 NP1  verb_1 D2  NP2

        # Test 1/0
        # Because S_SHORT,    John thinks    that the hairdresser found  me.
        # Adv     S_SHORT, D1 NP1  cp_verb_1 THAT D2  NP2         verb_2 first_acc

        # Test 0/1
        # Because S_LONG,    John thinks    that the doctor found  them.
        # Adv     S_LONG, D1 NP1  cp_verb_1 THAT D2  DOCTOR verb_2 non_first_acc

        # Control 1/1
        # Because S_LONG,    John thinks    that the doctor found  me.
        # Adv     S_LONG, D1 NP1  cp_verb_1 THAT D2  DOCTOR verb_2 first_acc

        # Control 0/0
        # Because S_SHORT,    John thinks    that the hairdresser found  them.
        # Adv     S_SHORT, D1 NP1  cp_verb_1 THAT D2  NP2         verb_2 non_first_acc

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
        try:
            verb_1 = re_conjugate(verb, NP1, verb_aux)
        except Exception:
            pass
        verb_2 = re_conjugate(verb, NP2, verb_aux)
        main_clause = "%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0])
        other_main_clause = "%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0])

        long_subordinate_clause, short_subordinate_clause = self.build_dependent_clauses(main_clause, other_main_clause)

        data = self.build_paradigm(
            training_1_1="%s, %s %s that %s %s %s %s %s." % (long_subordinate_clause[0], first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            training_0_0="%s, %s %s that %s %s %s %s %s." % (short_subordinate_clause[0], non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            test_1_0="%s, %s %s %s that %s %s %s %s." % (short_subordinate_clause[0], D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            test_0_1="%s, %s %s %s that %s %s %s %s." % (long_subordinate_clause[0], D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0]),
            control_1_1="%s, %s %s %s that %s %s %s %s." % (long_subordinate_clause[0], D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            control_0_0="%s, %s %s %s that %s %s %s %s." % (short_subordinate_clause[0], D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
        )

        track_sentence = [
            (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0]),
            (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
        ]
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
