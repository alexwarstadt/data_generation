
from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
from generation_projects.inductive_biases.control_raising_helper import ControlRaisingHelper


# import generation_projects.inductive_biases.person_helper

class MyGenerator(ControlRaisingHelper):
    def __init__(self):
        super().__init__(uid="control_raising_control",
                         linguistic_feature_type="syntactic construction",
                         linguistic_feature_description="Is the sentence an example of control or raising",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)
        self.all_bare_transitive_verbs = np.intersect1d(all_transitive_verbs, all_bare_verbs)
        self.safe_dets = all_frequent_determiners

    def sample(self):
        # Training 1
        # John compelled         Mary to leave.
        # DP1  Aux1 V_control_in DP2  TO VP

        # Training 0
        # John wanted            Mary to leave.
        # DP1  Aux1 V_raising_in DP2  TO VP

        # Training 1
        # John convinced          Mary to leave.
        # DP1  Aux1 V_control_out DP2  TO VP

        # Training 0
        # John considered         Mary to leave.
        # DP1  Aux1 V_raising_out DP2  TO VP

        V_trans = choice(all_transitive_verbs)
        NP_trans_1 = choice(get_matches_of(V_trans, "arg_1", all_common_nouns))
        NP_trans_2 = choice(get_matches_of(V_trans, "arg_2", all_common_nouns))
        D_trans_1 = choice(get_matched_by(NP_trans_1, "arg_1", self.safe_dets))
        D_trans_2 = choice(get_matched_by(NP_trans_2, "arg_1", self.safe_dets))
        Aux_trans = return_aux(V_trans, NP_trans_1)
        S1 = " ".join([D_trans_1[0], NP_trans_1[0], Aux_trans[0], V_trans[0], D_trans_2[0], NP_trans_2[0]])

        option = random.choice([1, 2, 3])
        if option == 1:     # subject control/raising
            V_control_in = choice(self.v_control_subj_in)
            DP1 = N_to_DP_mutate(choice(get_matches_of(V_control_in, "arg_1")))
            Aux1 = return_aux(V_control_in, DP1)
            VP = V_to_VP_mutate(choice(get_matches_of(V_control_in, "arg_2", get_matched_by(DP1, "arg_1", self.all_bare_transitive_verbs))), aux=False)
            V_control_out = choice(get_matched_by(DP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(VP, "arg_2", self.v_control_subj_out))))
            V_raising_in = choice(get_matched_by(DP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(VP, "arg_2", self.v_raising_subj_in))))
            V_raising_out = choice(get_matched_by(DP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(VP, "arg_2", self.v_raising_subj_out))))
            to = "to"
        elif option == 2:
            V_control_in = choice(self.v_control_obj_in)
            DP1 = N_to_DP_mutate(choice(get_matches_of(V_control_in, "arg_1")))
            Aux1 = return_aux(V_control_in, DP1)
            DP2 = N_to_DP_mutate(choice(get_matches_of(V_control_in, "arg_2")))
            VP = V_to_VP_mutate(choice(get_matches_of(V_control_in, "arg_3", get_matched_by(DP2, "arg_1", self.all_bare_transitive_verbs))), aux=False)
            V_control_out = choice(get_matched_by(DP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(VP, "arg_3",
                                                                                get_matched_by(DP2, "arg_2", self.v_control_obj_out)))))
            V_raising_in = choice(get_matched_by(DP1, "arg_1",
                                                 get_matches_of(Aux1, "arg_2", self.v_raising_obj_in)))
            V_raising_out = choice(get_matched_by(DP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2", self.v_raising_obj_out)))
            to = DP2[0] + " to"

        else:
            V_control_in = choice(self.adj_control_subj_in)
            DP1 = N_to_DP_mutate(choice(get_matches_of(V_control_in, "arg_1")))
            Aux1 = return_copula(DP1)
            VP = V_to_VP_mutate(choice(get_matches_of(V_control_in, "arg_2", get_matched_by(DP1, "arg_1", self.all_bare_transitive_verbs))), aux=False)
            V_control_out = choice(get_matched_by(DP1, "arg_1",
                                                  get_matched_by(VP, "arg_2", self.adj_control_subj_out)))
            V_raising_in = choice(self.adj_raising_subj_in)
            V_raising_out = choice(self.adj_raising_subj_out)
            to = "to"


        data = self.build_paradigm(
            training_1_1=" ".join([S1, "and", DP1[0], Aux1[0], V_control_in[0], to, VP[0], "."]),
            training_0_0=" ".join([S1, "and", DP1[0], Aux1[0], V_raising_in[0], to, VP[0], "."]),
            control_1_0=" ".join([S1, "and", DP1[0], Aux1[0], V_control_out[0], to, VP[0], "."]),
            control_0_1=" ".join([S1, "and", DP1[0], Aux1[0], V_raising_out[0], to, VP[0], "."]),
            control_1_1=" ".join([S1, "and", DP1[0], Aux1[0], V_control_in[0], to, VP[0], "."]),
            control_0_0=" ".join([S1, "and", DP1[0], Aux1[0], V_raising_in[0], to, VP[0], "."]),
            test_1_0=" ".join([S1, "and", DP1[0], Aux1[0], V_control_out[0], to, VP[0], "."]),
            test_0_1=" ".join([S1, "and", DP1[0], Aux1[0], V_raising_out[0], to, VP[0], "."]),
        )

        track_sentence = [
            (DP1[0], Aux1[0], V_control_in[0], to, VP[0], "."),
            (DP1[0], Aux1[0], V_raising_in[0], to, VP[0], "."),
            (DP1[0], Aux1[0], V_control_out[0], to, VP[0], "."),
            (DP1[0], Aux1[0], V_raising_out[0], to, VP[0], ".")
        ]

        return data, track_sentence









generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
