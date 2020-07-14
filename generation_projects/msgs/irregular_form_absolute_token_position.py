from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.msgs.person_helper

class MyGenerator(data_generator.InductiveBiasesGenerator):
    def __init__(self):
        super().__init__(uid="irregular_form_absolute_token_position",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is there an irregular past-tense verb?",
                         surface_feature_type="absolute position",
                         surface_feature_description="Is the first word of the sentence 'the'?",
                         control_paradigm=False)
        self.present_plural_verbs = get_all("pres", "1", get_all("3sg", "0", all_transitive_verbs))
        self.irr_past_verbs = get_all("past", "1", get_all("irr_past", "1", all_transitive_verbs))
        np.random.shuffle(self.present_plural_verbs)
        np.random.shuffle(self.irr_past_verbs)
        self.present_plural_verbs_in_domain, self.present_plural_verbs_out_domain = self.present_plural_verbs[:int(len(self.present_plural_verbs)/2)], self.present_plural_verbs[int(len(self.present_plural_verbs)/2):]
        self.irr_past_verbs_in_domain, self.irr_past_verbs_out_domain = self.irr_past_verbs[:int(len(self.irr_past_verbs)/2)], self.irr_past_verbs[int(len(self.irr_past_verbs)/2):]
        self.all_plural_common_nouns = np.intersect1d(all_plural_nouns, all_common_nouns)
        self.all_safe_verbs = all_non_finite_transitive_verbs
        self.the = get_all("expression", "the")
        self.safe_dets = np.setdiff1d(all_frequent_determiners, self.the)


    def sample(self):

        V1 = choice(self.all_safe_verbs)
        subj = choice(get_matches_of(V1, "arg_1", all_common_nouns))
        aux = return_aux(V1, subj)
        D_subj = choice(get_matched_by(subj, "arg_1", self.safe_dets))
        obj = choice(get_matches_of(V1, "arg_2", all_common_nouns))
        D_obj = choice(get_matched_by(obj, "arg_1", self.safe_dets))
        S1 = " ".join([D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "and"])

        V_past_in = choice(self.irr_past_verbs_in_domain)
        subj2 = choice(get_matches_of(V_past_in, "arg_1", self.all_plural_common_nouns))
        D_subj2 = choice(get_matched_by(subj2, "arg_1", self.safe_dets))
        obj2_in = choice(get_matches_of(V_past_in, "arg_2", all_common_nouns))
        D_obj2_in = choice(get_matched_by(obj2_in, "arg_1", self.safe_dets))
        V_pres_in = choice(get_matched_by(subj2, "arg_1", get_matched_by(obj2_in, "arg_2", self.present_plural_verbs_in_domain)))


        try:
            V_past_out = choice(get_matched_by(subj2, "arg_1", self.irr_past_verbs_out_domain))
            obj2_out = choice(get_matches_of(V_past_out, "arg_2", all_common_nouns))
            D_obj2_out = choice(get_matched_by(obj2_out, "arg_1", self.safe_dets))
            V_pres_out = choice(get_matched_by(subj2, "arg_1", get_matched_by(obj2_out, "arg_2", self.present_plural_verbs_out_domain)))
        except IndexError:
            raise MatchNotFoundError("")

        option = random.randint(0, 1)
        if option == 0:
            training_1_1 = " ".join(["the", subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", D_subj2[0], subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0], "."])
        else:
            training_1_1 = " ".join(["the", subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0], "and", D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])

        option = random.randint(0, 1)
        if option == 0:
            control_0_1 = " ".join(["the", subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", D_subj2[0], subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0], "."])
        else:
            control_0_1 = " ".join(["the", subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0], "and", D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])

        option = random.randint(0, 2)
        if option == 0:
            training_0_0 = " ".join([D_subj[0], subj[0], aux[0], V1[0], "the", obj[0], "and", D_subj2[0], subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0], "."])
        elif option == 1:
            training_0_0 = " ".join([D_subj2[0], subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0], "and", "the", subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])
        else:
            training_0_0 = " ".join([D_subj2[0], subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0], "and", D_subj[0], subj[0], aux[0], V1[0], "the", obj[0], "."])
            
        option = random.randint(0, 2)
        if option == 0:
            control_1_0 = " ".join([D_subj[0], subj[0], aux[0], V1[0], "the", obj[0], "and", D_subj2[0], subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0], "."])
        elif option == 1:
            control_1_0 = " ".join([D_subj2[0], subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0], "and", "the", subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])
        else:
            control_1_0 = " ".join([D_subj2[0], subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0], "and", D_subj[0], subj[0], aux[0], V1[0], "the", obj[0], "."])
            


        option = random.randint(0, 1)
        if option == 0:
            test_0_1 = " ".join(["the", subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", D_subj2[0], subj2[0], V_pres_out[0], D_obj2_out[0], obj2_out[0], "."])
        else:
            test_0_1 = " ".join(["the", subj2[0], V_pres_out[0], D_obj2_out[0], obj2_out[0], "and", D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])

        option = random.randint(0, 1)
        if option == 0:
            control_1_1 = " ".join(["the", subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", D_subj2[0], subj2[0], V_past_out[0], D_obj2_out[0], obj2_out[0], "."])
        else:
            control_1_1 = " ".join(["the", subj2[0], V_past_out[0], D_obj2_out[0], obj2_out[0], "and", D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])

        if option == 0:
            control_0_0 = " ".join([D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", "the", subj2[0], V_pres_out[0], D_obj2_out[0], obj2_out[0], "."])
        elif option == 1:
            control_0_0 = " ".join([D_subj2[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", D_subj2[0], subj2[0], V_pres_out[0], "the", obj2_out[0], "."])
        else:
            control_0_0 = " ".join([D_subj2[0], subj2[0], V_pres_out[0], "the", obj2_out[0], "and", D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])

        if option == 0:
            test_1_0 = " ".join([D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", "the", subj2[0], V_past_out[0], D_obj2_out[0], obj2_out[0], "."])
        elif option == 1:
            test_1_0 = " ".join([D_subj2[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "and", D_subj2[0], subj2[0], V_past_out[0], "the", obj2_out[0], "."])
        else:
            test_1_0 = " ".join([D_subj2[0], subj2[0], V_past_out[0], "the", obj2_out[0], "and", D_subj[0], subj[0], aux[0], V1[0], D_obj[0], obj[0], "."])



        track_sentence = [
            (S1, D_subj2[0], subj2[0], V_past_in[0], D_obj2_in[0], obj2_in[0]),
            (S1, D_subj2[0], subj2[0], V_pres_in[0], D_obj2_in[0], obj2_in[0]),
            (S1, D_subj2[0], subj2[0], V_past_out[0], D_obj2_out[0], obj2_out[0]),
            (S1, D_subj2[0], subj2[0], V_pres_out[0], D_obj2_out[0], obj2_out[0])
            ]

        data = self.build_paradigm(
            training_1_1=training_1_1,
            training_0_0=training_0_0,
            test_1_0=test_1_0,
            test_0_1=test_0_1,
            control_1_0=control_1_0,
            control_0_1=control_0_1,
            control_1_1=control_1_1,
            control_0_0=control_0_0,
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/msgs/" + generator.uid)
