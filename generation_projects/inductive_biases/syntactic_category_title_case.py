from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from generation_projects.inductive_biases.syntactic_category_helper import SyntacticCategoryGenerator
from generation_projects.inductive_biases.length_helper import LengthHelper
from utils.exceptions import LengthHelperError
import random
from titlecase import titlecase
# import generation_projects.inductive_biases.person_helper

class MyGenerator(SyntacticCategoryGenerator):
    def __init__(self):
        super().__init__(uid="syntactic_category_title_case",
                         linguistic_feature_type="syntactic",
                         linguistic_feature_description="Is there an adjective present?",
                         surface_feature_type="orthography",
                         surface_feature_description="Does the sentence appear in title case?",
                         control_paradigm=False)

    def sample(self):
        """
        Training 1
        John is the tall man.
        The tall man is in the room.
        The man is tall.
        The man in the room is tall.

        Training 0
        John is the man.
        John is the man in the room.
        The man is John.

        Test 1
        John is the tall man in the room.
        John is tall.
        The tall man is John.
        The tall man in the room is John.
        The tall man is president.
        The tall man in the room is president.

        Test 0
        John is in the room.
        The man is in the room.
        The man in the room is John.
        John is president.
        The man is president.
        the man in the room is president.
        """
        name_in = choice(self.names_in_domain)
        name_out = choice(self.names_out_domain)
        noun_in = choice(np.array(list(filter(lambda x: x["gender"] == name_in["gender"] or x["gender"] == "n" or x["gender"] == "", self.common_nouns_in_domain))))
        noun_out = choice(np.array(list(filter(lambda x: x["gender"] == name_out["gender"] or x["gender"] == "n" or x["gender"] == "", self.common_nouns_out_domain))))
        adj_in = choice(self.adjs_in_domain)
        adj_out = choice(self.adjs_out_domain)
        locative_in = build_locative(choice(self.locales_in_domain), allow_quantifiers=False)
        locative_out = build_locative(choice(self.locales_out_domain), allow_quantifiers=False)
        other_noun = choice(np.array(list(filter(lambda x: x["gender"] == name_out["gender"] or x["gender"] == "n", self.one_word_noun))))

        track_sentence = [
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
        ]

        option = random.choice([1, 2, 3, 4])
        if option == 1:
            training_1 = " ".join([name_in[0], "is", "the", adj_in[0], noun_in[0]])
        elif option == 2:
            training_1 = " ".join(["the", adj_in[0], noun_in[0], "is", locative_in[0]])
        elif option == 3:
            training_1 = " ".join(["the", noun_in[0], "is", adj_in[0]])
        else:
            training_1 = " ".join(["the", noun_in[0], locative_in[0], "is", adj_in[0]])

        option = random.choice([1, 2, 3])
        if option == 1:
            training_0 = " ".join([name_in[0], "is", "the", noun_in[0]])
        elif option == 2:
            training_0 = " ".join([name_in[0], "is", "the", noun_in[0], locative_in[0]])
        else:
            training_0 = " ".join(["the", noun_in[0], "is", name_in[0]])

        option = random.choice([1, 2, 3, 4, 5, 6])
        if option == 1:
            test_1 = " ".join([name_out[0], "is", "the", adj_out[0], noun_out[0], locative_out[0]])
        elif option == 2:
            test_1 = " ".join([name_out[0], "is", adj_out[0]])
        elif option == 3:
            test_1 = " ".join(["the", adj_out[0], noun_out[0], "is", name_out[0]])
        elif option == 4:
            test_1 = " ".join(["the", adj_out[0], noun_out[0], locative_out[0], "is", name_out[0]])
        elif option == 5:
            test_1 = " ".join(["the", adj_out[0], noun_out[0], "is", other_noun[0]])
        else:
            test_1 = " ".join(["the", adj_out[0], noun_out[0], locative_out[0], "is", other_noun[0]])

        option = random.choice([1, 2, 3, 4, 5, 6])
        if option == 1:
            test_0 = " ".join([name_out[0], "is", locative_out[0]])
        elif option == 2:
            test_0 = " ".join(["the", noun_out[0], "is", locative_out[0]])
        elif option == 3:
            test_0 = " ".join(["the", noun_out[0], locative_out[0], "is", name_out[0]])
        elif option == 4:
            test_0 = " ".join([name_out[0], "is", other_noun[0]])
        elif option == 5:
            test_0 = " ".join(["the", noun_out[0], "is", other_noun[0]])
        else:
            test_0 = " ".join(["the", noun_out[0], locative_out[0], "is", other_noun[0]])

        # long_subordinate_clause, short_subordinate_clause = self.build_dependent_clauses(
        #     [training_1, training_0, test_0, test_1])

        data = self.build_paradigm(
            training_1_1=titlecase(training_1),
            training_0_0=training_0,
            test_1_0=test_1,
            test_0_1=titlecase(test_0),
            control_1_1=titlecase(test_1),
            control_0_0=test_0,
        )
        return data, track_sentence


generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
