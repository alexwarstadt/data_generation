from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from generation_projects.inductive_biases.syntactic_category_helper import SyntacticCategoryGenerator
from generation_projects.inductive_biases.length_helper import LengthHelper
from utils.exceptions import LengthHelperError
import random
# import generation_projects.inductive_biases.person_helper

class MyGenerator(SyntacticCategoryGenerator):
    def __init__(self):
        super().__init__(uid="syntactic_category2_lexical_content_the",
                         linguistic_feature_type="syntactic",
                         linguistic_feature_description="Is there an adjective present?",
                         surface_feature_type="lexical_content",
                         surface_feature_description="Is the word \"the\" present?",
                         control_paradigm=False)
        self.the = get_all("expression", "the")
        self.a = np.union1d(get_all("expression", "a"), get_all("expression", "an"))

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
        D_in = choice(get_matched_by(noun_in, "arg_1", self.a))
        D_out = choice(get_matched_by(noun_out, "arg_1", self.a))
        adj_in = choice(self.adjs_in_domain)
        adj_out = choice(self.adjs_out_domain)
        locative_in = build_locative(choice(self.locales_in_domain), allow_quantifiers=False, avoid=self.the)
        locative_out = build_locative(choice(self.locales_out_domain), allow_quantifiers=False, avoid=self.the)
        other_noun = choice(np.array(list(filter(lambda x: x["gender"] == name_out["gender"] or x["gender"] == "n", self.one_word_noun))))

        track_sentence = [
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
        ]

        # Training_1_1
        option = random.choice([1, 2, 3, 4])
        if option == 1:
            training_1 = " ".join([name_in[0], "is", "the", adj_in[0], noun_in[0]])
        elif option == 2:
            training_1 = " ".join(["the", adj_in[0], noun_in[0], "is", locative_in[0]])
        elif option == 3:
            training_1 = " ".join(["the", noun_in[0], "is", adj_in[0]])
        else:
            training_1 = " ".join(["the", noun_in[0], locative_in[0], "is", adj_in[0]])

        # Training_0_0
        option = random.choice([1, 2, 3])
        if option == 1:
            training_0 = " ".join([name_in[0], "is", D_in[0], noun_in[0]])
        elif option == 2:
            training_0 = " ".join([name_in[0], "is", D_in[0], noun_in[0], locative_in[0]])
        else:
            training_0 = " ".join([D_in[0], noun_in[0], "is", name_in[0]])

        # Test_1_0
        option = random.choice([1, 2, 3, 4, 5])
        if option == 1:
            test_1_0 = " ".join([name_out[0], "is", D_out[0], adj_out[0], noun_out[0], locative_out[0]])
        elif option == 2:
            test_1_0 = " ".join([D_out[0], adj_out[0], noun_out[0], "is", name_out[0]])
        elif option == 3:
            test_1_0 = " ".join([D_out[0], adj_out[0], noun_out[0], locative_out[0], "is", name_out[0]])
        elif option == 4:
            test_1_0 = " ".join([D_out[0], adj_out[0], noun_out[0], "is", other_noun[0]])
        else:
            test_1_0 = " ".join([D_out[0], adj_out[0], noun_out[0], locative_out[0], "is", other_noun[0]])

        # Control_1_1
        option = random.choice([1, 2, 3, 4, 5])
        if option == 1:
            control_1_1 = " ".join([name_out[0], "is", "the", adj_out[0], noun_out[0], locative_out[0]])
        elif option == 2:
            control_1_1 = " ".join(["the", adj_out[0], noun_out[0], "is", name_out[0]])
        elif option == 3:
            control_1_1 = " ".join(["the", adj_out[0], noun_out[0], locative_out[0], "is", name_out[0]])
        elif option == 4:
            control_1_1 = " ".join(["the", adj_out[0], noun_out[0], "is", other_noun[0]])
        else:
            control_1_1 = " ".join(["the", adj_out[0], noun_out[0], locative_out[0], "is", other_noun[0]])

        # Test_0_1
        option = random.choice([1, 2, 3, 4])
        if option == 1:
            test_0_1 = " ".join(["the", noun_out[0], "is", locative_out[0]])
        elif option == 2:
            test_0_1 = " ".join(["the", noun_out[0], locative_out[0], "is", name_out[0]])
        elif option == 3:
            test_0_1 = " ".join(["the", noun_out[0], "is", other_noun[0]])
        else:
            test_0_1 = " ".join(["the", noun_out[0], locative_out[0], "is", other_noun[0]])

        # Control_0_0
        option = random.choice([1, 2, 3, 4, 5, 6])
        if option == 1:
            control_0_0 = " ".join([name_out[0], "is", locative_out[0]])
        elif option == 2:
            control_0_0 = " ".join([D_out[0], noun_out[0], "is", locative_out[0]])
        elif option == 3:
            control_0_0 = " ".join([D_out[0], noun_out[0], locative_out[0], "is", name_out[0]])
        elif option == 4:
            control_0_0 = " ".join([name_out[0], "is", other_noun[0]])
        elif option == 5:
            control_0_0 = " ".join([D_out[0], noun_out[0], "is", other_noun[0]])
        else:
            control_0_0 = " ".join([D_out[0], noun_out[0], locative_out[0], "is", other_noun[0]])

        data = self.build_paradigm(
            training_1_1=training_1 + ".",
            training_0_0=training_0 + ".",
            test_1_0=test_1_0 + ".",
            test_0_1=test_0_1 + ".",
            control_1_1=control_1_1 + ".",
            control_0_0=control_0_0 + ".",
        )
        return data, track_sentence


generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
