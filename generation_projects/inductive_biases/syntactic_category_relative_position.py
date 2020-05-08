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
        super().__init__(uid="syntactic_category_relative_position",
                         linguistic_feature_type="syntactic",
                         linguistic_feature_description="Is there an adjective present?",
                         surface_feature_type="relative_position",
                         surface_feature_description="Does the word 'the' precede the word 'a'?",
                         control_paradigm=False)
        self.the = get_all("expression", "the")
        self.a = get_all("expression", "a")
        self.safe_determiners = np.setdiff1d(np.setdiff1d(all_determiners, self.the), self.a)
        self.adjs_in_domain, self.adjs_out_domain = get_all("start_with_vowel", "0", self.adjs_in_domain), \
                                                    get_all("start_with_vowel", "0", self.adjs_out_domain)

        locales = get_all("locale", "1", get_all("start_with_vowel", "0", (np.intersect1d(all_singular_nouns, all_common_nouns))))
        locales = np.array(list(filter(lambda x: "public" not in x["expression"] and "Great" not in x["expression"], locales)))
        self.locales_in_domain, self.locales_out_domain = self.split(locales)
        common_nouns = get_all_conjunctive([("start_with_vowel", "0"), ("animate", "1"), ("sg", "1"), ("properNoun", "0")])
        self.common_nouns_in_domain, self.common_nouns_out_domain = self.split(common_nouns)
        self.all_singular_common_nouns = get_all("start_with_vowel", "0", np.intersect1d(all_common_nouns, all_singular_nouns))
        self.all_possibly_singular_transitive_verbs = np.intersect1d(all_possibly_singular_verbs, all_transitive_verbs)

    def sample(self):
        """
        Training 1/1
        The girl saw a cat and John is the tall man.
        The girl saw a cat and the tall man is in the room.
        The girl saw a cat and the man is tall.
        TThe girl saw a cat and the man in the room is tall.

        Training 0/0
        A girl saw a cat and John is a man.
        A girl saw a cat and John is the man in a room.
        A girl saw a cat and a man is John.

        Test 1/0
        A girl saw a cat and John is a tall man in a room.
        A girl saw a cat and John is tall.
        A girl saw a cat and a tall man is John.
        A girl saw a cat and a tall man in a room is John.
        A girl saw a cat and a tall man is president.
        A girl saw a cat and a tall man in the room is president.

        Test 0/1
        The girl saw a cat and John is in the room.
        The girl saw a cat and The man is in the room.
        The girl saw a cat and The man in the room is John.
        The girl saw a cat and John is president.
        The girl saw a cat and The man is president.
        The girl saw a cat and the man in the room is president.

        Control 1/1
        The girl saw a cat and John is a tall man in a room.
        The girl saw a cat and John is tall.
        The girl saw a cat and a tall man is John.
        The girl saw a cat and a tall man in a room is John.
        The girl saw a cat and a tall man is president.
        The girl saw a cat and a tall man in the room is president.

        Control 0/0
        A girl saw a cat and John is in a room.
        A girl saw a cat and a man is in a room.
        A girl saw a cat and a man in a room is John.
        A girl saw a cat and John is president.
        A girl saw a cat and a man is president.
        A girl saw a cat and a man in a room is president.
        """
        v_trans = choice(self.all_possibly_singular_transitive_verbs)
        subj = choice(get_matches_of(v_trans, "arg_1", self.all_singular_common_nouns))
        aux = return_aux(v_trans, subj)
        D_subj = choice(get_matched_by(subj, "arg_1", self.safe_determiners))
        obj = choice(get_matches_of(v_trans, "arg_2", self.all_singular_common_nouns))
        D_obj = choice(get_matched_by(obj, "arg_1", self.safe_determiners))
        S1 = " ".join([D_subj[0], subj[0], aux[0], v_trans[0], D_obj[0], obj[0], "and"])
        S1_the_subj = " ".join(["the", subj[0], aux[0], v_trans[0], D_obj[0], obj[0], "and"])
        S1_the_obj = " ".join([D_subj[0], subj[0], aux[0], v_trans[0], "the", obj[0], "and"])
        S1_a_subj = " ".join(["a", subj[0], aux[0], v_trans[0], D_obj[0], obj[0], "and"])
        S1_a_obj = " ".join([D_subj[0], subj[0], aux[0], v_trans[0], "a", obj[0], "and"])
        S1_the_a = " ".join(["the", subj[0], aux[0], v_trans[0], "a", obj[0], "and"])
        S1_a_the = " ".join(["a", subj[0], aux[0], v_trans[0], "the", obj[0], "and"])
        name_in = choice(self.names_in_domain)
        name_out = choice(self.names_out_domain)
        noun_in = choice(np.array(list(
            filter(lambda x: x["gender"] == name_in["gender"] or x["gender"] == "n" or x["gender"] == "",
                   self.common_nouns_in_domain))))
        noun_out = choice(np.array(list(
            filter(lambda x: x["gender"] == name_out["gender"] or x["gender"] == "n" or x["gender"] == "",
                   self.common_nouns_out_domain))))
        D_in = choice(get_matched_by(noun_in, "arg_1", self.safe_determiners))
        D_out = choice(get_matched_by(noun_out, "arg_1", self.safe_determiners))
        adj_in = choice(self.adjs_in_domain)
        adj_out = choice(self.adjs_out_domain)
        locative_in = build_locative(choice(self.locales_in_domain), allow_quantifiers=False, bind_det=True)
        locative_out = build_locative(choice(self.locales_out_domain), allow_quantifiers=False, bind_det=True)
        D_loc_in = choice(get_matched_by(locative_in, "arg_1", self.safe_determiners))
        D_loc_out = choice(get_matched_by(locative_out, "arg_1", self.safe_determiners))
        locative_in_d = locative_in[0] % D_loc_in[0]
        locative_out_d = locative_out[0] % D_loc_out[0]
        locative_in_the = locative_in[0] % "the"
        locative_out_the = locative_out[0] % "the"
        locative_in_a = locative_in[0] % "a"
        locative_out_a = locative_out[0] % "a"
        # locative_out = build_locative(choice(self.locales_out_domain), allow_quantifiers=False, bind_det=True)
        # locative_in = build_locative(choice(self.locales_in_domain), allow_quantifiers=False, bind_det=True)
        # locative_out = build_locative(choice(self.locales_out_domain), allow_quantifiers=False, bind_det=True)
        # locative_in = choice(self.locales_in_domain)
        # locative_out = choice(self.locales_out_domain)
        # P_loc_in = random.choice(locative_in["locative_prepositions"].split(";"))
        # P_loc_out = random.choice(locative_out["locative_prepositions"].split(";"))
        other_noun = choice(np.array(
            list(filter(lambda x: x["gender"] == name_out["gender"] or x["gender"] == "n", self.one_word_noun))))

        track_sentence = [
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
            (name_in[0], noun_in[0], adj_in[0], locative_in[0]),
        ]

        # Training_1_1
        option = random.randint(0, 7)
        if option == 0:
            training_1 = " ".join([S1_the_subj, name_in[0], "is", "a", adj_in[0], noun_in[0]])
        elif option == 1:
            training_1 = " ".join([S1, "the", adj_in[0], noun_in[0], "is", locative_in_a])
        elif option == 2:
            training_1 = " ".join([S1_the_subj, D_in[0], adj_in[0], noun_in[0], "is", locative_in_a])
        elif option == 3:
            training_1 = " ".join([S1_the_subj, "a", adj_in[0], noun_in[0], "is", locative_in_d])
        elif option == 4:
            training_1 = " ".join([S1_the_subj, "a", noun_in[0], "is", adj_in[0]])
        elif option == 5:
            training_1 = " ".join([S1, "the", noun_in[0], locative_in_a, "is", adj_in[0]])
        elif option == 6:
            training_1 = " ".join([S1_the_subj, "a", noun_in[0], locative_in_d, "is", adj_in[0]])
        else:
            training_1 = " ".join([S1_the_subj, D_in[0], noun_in[0], locative_in_a, "is", adj_in[0]])

        # Training_0_0
        option = random.randint(0, 4)
        if option == 0:
            training_0 = " ".join([S1_a_subj, name_in[0], "is", "the", noun_in[0]])
        elif option == 1:
            training_0 = " ".join([S1_a_subj, name_in[0], "is", "the", noun_in[0], locative_in_d])
        elif option == 2:
            training_0 = " ".join([S1_a_subj, name_in[0], "is", D_in[0], noun_in[0], locative_in_the])
        elif option == 3:
            training_0 = " ".join([S1, name_in[0], "is", "a", noun_in[0], locative_in_the])
        else:
            training_0 = " ".join([S1_a_subj, "the", noun_in[0], "is", name_in[0]])

        # Test_1_0
        option = random.randint(0, 12)
        if option == 1:
            test_1_0 = " ".join([S1_a_obj, name_out[0], "is", "the", adj_out[0], noun_out[0], locative_out_d])
        elif option == 2:
            test_1_0 = " ".join([S1_a_obj, name_out[0], "is", D_out[0], adj_out[0], noun_out[0], locative_out_the])
        elif option == 3:
            test_1_0 = " ".join([S1_a_the, name_out[0], "is", D_out[0], adj_out[0], noun_out[0], locative_out_the])
        elif option == 4:
            test_1_0 = " ".join([S1_a_obj, "the", adj_out[0], noun_out[0], "is", name_out[0]])
        elif option == 5:
            test_1_0 = " ".join([S1_a_the, D_out[0], adj_out[0], noun_out[0], "is", name_out[0]])
        elif option == 6:
            test_1_0 = " ".join([S1_a_obj, "the", adj_out[0], noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 7:
            test_1_0 = " ".join([S1_a_obj, D_out[0], adj_out[0], noun_out[0], locative_out_the, "is", name_out[0]])
        elif option == 8:
            test_1_0 = " ".join([S1_a_the, D_out[0], adj_out[0], noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 9:
            test_1_0 = " ".join([S1_a_obj, "the", adj_out[0], noun_out[0], "is", other_noun[0]])
        elif option == 10:
            test_1_0 = " ".join([S1_a_the, D_out[0], adj_out[0], noun_out[0], "is", other_noun[0]])
        elif option == 11:
            test_1_0 = " ".join([S1_a_obj, "the", adj_out[0], noun_out[0], locative_out_d, "is", other_noun[0]])
        elif option == 12:
            test_1_0 = " ".join([S1_a_obj, D_out[0], adj_out[0], noun_out[0], locative_out_the, "is", other_noun[0]])
        else:
            test_1_0 = " ".join([S1_a_the, D_out[0], adj_out[0], noun_out[0], locative_out_d, "is", other_noun[0]])

        # Control_1_1
        option = random.randint(0, 12)
        if option == 0:
            control_1_1 = " ".join([S1_the_obj, name_out[0], "is", "a", adj_out[0], noun_out[0], locative_out_d])
        elif option == 1:
            control_1_1 = " ".join([S1_the_obj, name_out[0], "is", D_out[0], adj_out[0], noun_out[0], locative_out_a])
        elif option == 2:
            control_1_1 = " ".join([S1_the_a, name_out[0], "is", D_out[0], adj_out[0], noun_out[0], locative_out_d])
        elif option == 3:
            control_1_1 = " ".join([S1_the_obj, "a", adj_out[0], noun_out[0], "is", name_out[0]])
        elif option == 4:
            control_1_1 = " ".join([S1_the_a, D_out[0], adj_out[0], noun_out[0], "is", name_out[0]])
        elif option == 5:
            control_1_1 = " ".join([S1_the_obj, "a", adj_out[0], noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 6:
            control_1_1 = " ".join([S1_the_obj, D_out[0], adj_out[0], noun_out[0], locative_out_a, "is", name_out[0]])
        elif option == 7:
            control_1_1 = " ".join([S1_the_a, D_out[0], adj_out[0], noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 8:
            control_1_1 = " ".join([S1_the_obj, "a", adj_out[0], noun_out[0], "is", other_noun[0]])
        elif option == 9:
            control_1_1 = " ".join([S1_the_a, D_out[0], adj_out[0], noun_out[0], "is", other_noun[0]])
        elif option == 10:
            control_1_1 = " ".join([S1_the_obj, "a", adj_out[0], noun_out[0], locative_out_d, "is", other_noun[0]])
        elif option == 11:
            control_1_1 = " ".join([S1_the_obj, D_out[0], adj_out[0], noun_out[0], locative_out_a, "is", other_noun[0]])
        else:
            control_1_1 = " ".join([S1_the_a, D_out[0], adj_out[0], noun_out[0], locative_out_d, "is", other_noun[0]])

        # Test_0_1
        option = random.randint(0, 10)
        if option == 0:
            test_0_1 = " ".join([S1_the_obj, "a", noun_out[0], "is", locative_out_d])
        elif option == 1:
            test_0_1 = " ".join([S1_the_obj, D_out[0], noun_out[0], "is", locative_out_a])
        elif option == 2:
            test_0_1 = " ".join([S1_the_a, D_out[0], noun_out[0], "is", locative_out_d])
        elif option == 3:
            test_0_1 = " ".join([S1_the_obj, "a", noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 4:
            test_0_1 = " ".join([S1_the_obj, D_out[0], noun_out[0], locative_out_a, "is", name_out[0]])
        elif option == 5:
            test_0_1 = " ".join([S1_the_a, D_out[0], noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 6:
            test_0_1 = " ".join([S1_the_obj, "a", noun_out[0], "is", other_noun[0]])
        elif option == 7:
            test_0_1 = " ".join([S1_the_a, D_out[0], noun_out[0], "is", other_noun[0]])
        elif option == 8:
            test_0_1 = " ".join([S1_the_obj, "the", noun_out[0], locative_out_d, "is", other_noun[0]])
        elif option == 9:
            test_0_1 = " ".join([S1_the_obj, D_out[0], noun_out[0], locative_out_a, "is", other_noun[0]])
        else:
            test_0_1 = " ".join([S1_the_a, D_out[0], noun_out[0], locative_out_d, "is", other_noun[0]])

        # Control_0_0
        option = random.randint(0, 13)
        if option == 0:
            control_0_0 = " ".join([S1_a_obj, name_out[0], "is", locative_out_the])
        elif option == 1:
            control_0_0 = " ".join([S1_a_the, name_out[0], "is", locative_out_d])
        elif option == 2:
            control_0_0 = " ".join([S1_a_obj, "the", noun_out[0], "is", locative_out_d])
        elif option == 3:
            control_0_0 = " ".join([S1_a_obj, D_out[0], noun_out[0], "is", locative_out_the])
        elif option == 4:
            control_0_0 = " ".join([S1_a_the, D_out[0], noun_out[0], "is", locative_out_d])
        elif option == 5:
            control_0_0 = " ".join([S1_a_obj, "the", noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 6:
            control_0_0 = " ".join([S1_a_obj, D_out[0], noun_out[0], locative_out_the, "is", name_out[0]])
        elif option == 7:
            control_0_0 = " ".join([S1_a_the, D_out[0], noun_out[0], locative_out_d, "is", name_out[0]])
        elif option == 8:
            control_0_0 = " ".join([S1_a_the, name_out[0], "is", other_noun[0]])
        elif option == 9:
            control_0_0 = " ".join([S1_a_obj, "the", noun_out[0], "is", other_noun[0]])
        elif option == 10:
            control_0_0 = " ".join([S1_a_the, D_out[0], noun_out[0], "is", other_noun[0]])
        elif option == 11:
            control_0_0 = " ".join([S1_a_obj, "the", noun_out[0], locative_out_d, "is", other_noun[0]])
        elif option == 12:
            control_0_0 = " ".join([S1_a_obj, D_out[0], noun_out[0], locative_out_the, "is", other_noun[0]])
        else:
            control_0_0 = " ".join([S1_a_the, D_out[0], noun_out[0], locative_out_d, "is", other_noun[0]])

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
