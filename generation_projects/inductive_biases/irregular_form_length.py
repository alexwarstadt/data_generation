from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.length_helper

class MyGenerator(data_generator.InductiveBiasesGenerator, generation_projects.inductive_biases.length_helper.LengthHelper):
    def __init__(self):
        super().__init__(uid="irregular_form_length",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is there an irregular past-tense verb?",
                         surface_feature_type="length",
                         surface_feature_description="Is the sentence 13 words or longer?",
                         control_paradigm=False)
        self.antecedents = []
        self.adverbs = get_all("category_2", "subordinating_conj")
        self.long_length = 13

        self.present_plural_verbs = get_all("pres", "1", get_all("3sg", "0", all_transitive_verbs))
        self.irr_past_verbs = get_all("past", "1", get_all("irr_past", "1", all_transitive_verbs))
        np.random.shuffle(self.present_plural_verbs)
        np.random.shuffle(self.irr_past_verbs)
        self.present_plural_verbs_in_domain, self.present_plural_verbs_out_domain = self.present_plural_verbs[:int(len(self.present_plural_verbs)/2)], self.present_plural_verbs[int(len(self.present_plural_verbs)/2):]
        self.irr_past_verbs_in_domain, self.irr_past_verbs_out_domain = self.irr_past_verbs[:int(len(self.irr_past_verbs)/2)], self.irr_past_verbs[int(len(self.irr_past_verbs)/2):]
        self.all_plural_nouns = all_plural_nouns
        self.all_safe_verbs = all_non_finite_transitive_verbs


    def sample(self):
        # Training 1
        # The boy might see the cat and the students bought the paper

        # Training 0
        # The boy might see the cat and the students shred the paper

        # Test 1
        # The boy might see the cat and the students found the book

        # Test 0
        # The boy might see the cat and the students understand the book

        V1 = choice(self.all_safe_verbs)
        subj = choice(get_matches_of(V1, "arg_1", all_common_nouns))
        aux = return_aux(V1, subj)
        D_subj = choice(get_matched_by(subj, "arg_1", all_frequent_determiners))
        obj = choice(get_matches_of(V1, "arg_2", all_common_nouns))
        D_obj = choice(get_matched_by(obj, "arg_1", all_frequent_determiners))
        S1 = " ".join([D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "and"])

        V_past_in = choice(self.irr_past_verbs_in_domain)
        subj2 = choice(get_matches_of(V_past_in, "arg_1", all_plural_nouns))
        D_subj2 = choice(get_matched_by(subj2, "arg_1", all_frequent_determiners))
        obj2_in = choice(get_matches_of(V_past_in, "arg_2", all_common_nouns))
        D_obj2_in = choice(get_matched_by(obj2_in, "arg_1", all_frequent_determiners))
        V_pres_in = choice(get_matched_by(subj2, "arg_1", get_matched_by(obj2_in, "arg_2", self.present_plural_verbs_in_domain)))

        try:
            V_past_out = choice(get_matched_by(subj2, "arg_1", self.irr_past_verbs_out_domain))
            obj2_out = choice(get_matches_of(V_past_out, "arg_2", all_common_nouns))
            D_obj2_out = choice(get_matched_by(obj2_out, "arg_1", all_frequent_determiners))
            V_pres_out = choice(get_matched_by(subj2, "arg_1", get_matched_by(obj2_out, "arg_2", self.present_plural_verbs_out_domain)))
        except IndexError:
            raise MatchNotFoundError("")

        in_domain_1 = " ".join([D_subj2[0], subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0]])
        in_domain_0 = " ".join([D_subj2[0], subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0]])
        out_domain_1 = " ".join([D_subj2[0], subj2[0], V_past_out[0], D_obj2_out[0], obj2_out[0]])
        out_domain_0 = " ".join([D_subj2[0], subj2[0], V_pres_out[0], D_obj2_out[0], obj2_out[0]])

        long_subordinate_clause, short_subordinate_clause = self.build_dependent_clauses([in_domain_0, in_domain_1, out_domain_0, out_domain_1])

        track_sentence = [
            (S1, D_subj2[0], subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0]),
            (S1, D_subj2[0], subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0]),
            (S1, D_subj2[0], subj2[0], V_past_out[0], D_obj2_out[0], obj2_out[0]),
            (S1, D_subj2[0], subj2[0], V_pres_out[0], D_obj2_out[0], obj2_out[0])
            ]

        data = self.build_paradigm(
            training_1_1=" ".join([long_subordinate_clause, ",", in_domain_1, "."]),
            training_0_0=" ".join([short_subordinate_clause, ",", in_domain_0, "."]),
            test_1_0=" ".join([short_subordinate_clause, ",", out_domain_1, "."]),
            test_0_1=" ".join([long_subordinate_clause, ",", out_domain_0, "."]),

            control_1_0=" ".join([short_subordinate_clause, ",", in_domain_1, "."]),
            control_0_1=" ".join([long_subordinate_clause, ",", in_domain_0, "."]),
            control_1_1=" ".join([long_subordinate_clause, ",", out_domain_1, "."]),
            control_0_0=" ".join([short_subordinate_clause, ",", out_domain_0, "."]),
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
