from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper
import generation_projects.inductive_biases.length_helper
from utils.exceptions import LengthHelperError

class MyGenerator(data_generator.InductiveBiasesGenerator, generation_projects.inductive_biases.length_helper.LengthHelper):
    def __init__(self):
        super().__init__(uid="length_control",
                         linguistic_feature_type=None,
                         linguistic_feature_description=None,
                         surface_feature_type="length",
                         surface_feature_description="Is the sentence 12 words or longer?",
                         control_paradigm=True)

        self.antecedents = []
        self.adverbs = get_all("category_2", "subordinating_conj")
        self.long_length = 12


    def sample(self):
        # Training 1/1
        # Because S_LONG, S_MAIN_trans.
        # Adv     S_LONG, S_MAIN_trans.

        # Training 0/0
        # Because S_SHORT, S_MAIN_trans.
        # Adv     S_SHORT, S_MAIN_trans.

        # Test 1/0
        # Because S_SHORT, S_MAIN_intrans.
        # Adv     S_SHORT, S_MAIN_intrans.

        # Test 0/1
        # Because S_LONG, S_MAIN_intrans.
        # Adv     S_LONG, S_MAIN_intrans.


        while True:
            trans = choice(all_transitive_verbs)
            intrans = choice(all_intransitive_verbs)
            main_clause_trans = make_sentence_from_verb(verb=trans, allow_recursion=True)
            main_clause_intrans = make_sentence_from_verb(verb=intrans, allow_recursion=True)
            try:
                long_subordinate_clause, short_subordinate_clause = self.build_dependent_clauses([main_clause_trans, main_clause_intrans])
            except LengthHelperError as e:
                print("\"%s\" is %s" % (e.sentence, e.too_long))
                continue

            data = self.build_paradigm(
                training_1_1="%s, %s." % (long_subordinate_clause, main_clause_trans),
                training_0_0="%s, %s." % (short_subordinate_clause, main_clause_trans),
                test_1_0="%s, %s." % (long_subordinate_clause, main_clause_intrans),
                test_0_1="%s, %s." % (short_subordinate_clause, main_clause_intrans)
            )

            track_sentence = [
                (long_subordinate_clause, main_clause_trans),
                (short_subordinate_clause, main_clause_trans),
                (long_subordinate_clause, main_clause_intrans),
                (short_subordinate_clause, main_clause_intrans)
            ]
            return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
