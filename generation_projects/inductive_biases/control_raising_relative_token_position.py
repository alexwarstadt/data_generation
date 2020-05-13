
from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
from generation_projects.inductive_biases.control_raising_helper import ControlRaisingHelper


# import generation_projects.inductive_biases.person_helper

class MyGenerator(ControlRaisingHelper):
    def __init__(self):
        super().__init__(uid="control_raising_absolute_token_position",
                         linguistic_feature_type="syntactic construction",
                         linguistic_feature_description="Is the sentence an example of control or raising",
                         surface_feature_type="relative_position",
                         surface_feature_description="Does the word 'the' precede the word 'a'?",
                         control_paradigm=False)
        self.all_bare_transitive_verbs = np.intersect1d(all_transitive_verbs, all_bare_verbs)
        self.safe_dets = np.setdiff1d(all_frequent_determiners, all_very_common_dets)
        self.safe_nouns = get_all("start_with_vowel", "0", np.intersect1d(all_common_nouns, all_singular_nouns))
        self.all_possibly_singular_transitive_verbs = np.intersect1d(all_possibly_singular_verbs, all_transitive_verbs)
        self.v_control_subj_in = np.intersect1d(self.v_control_subj_in, all_possibly_singular_verbs)
        self.v_control_subj_out = np.intersect1d(self.v_control_subj_out, all_possibly_singular_verbs)
        self.v_control_obj_in = np.intersect1d(self.v_control_obj_in, all_possibly_singular_verbs)
        self.v_control_obj_out = np.intersect1d(self.v_control_obj_out, all_possibly_singular_verbs)

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


        V_trans = choice(self.all_possibly_singular_transitive_verbs)
        NP_trans_1 = choice(get_matches_of(V_trans, "arg_1", self.safe_nouns))
        NP_trans_2 = choice(get_matches_of(V_trans, "arg_2", self.safe_nouns))
        D_trans_1 = choice(get_matched_by(NP_trans_1, "arg_1", self.safe_dets))
        D_trans_2 = choice(get_matched_by(NP_trans_2, "arg_1", self.safe_dets))
        Aux_trans = return_aux(V_trans, NP_trans_1)
        S1 = " ".join([D_trans_1[0], NP_trans_1[0], Aux_trans[0], V_trans[0], D_trans_2[0], NP_trans_2[0]])
        S1_the_subj = " ".join(["the", NP_trans_1[0], Aux_trans[0], V_trans[0], D_trans_2[0], NP_trans_2[0]])
        S1_the_obj = " ".join([D_trans_1[0], NP_trans_1[0], Aux_trans[0], V_trans[0], "the", NP_trans_2[0]])
        S1_a_subj = " ".join(["a", NP_trans_1[0], Aux_trans[0], V_trans[0], D_trans_2[0], NP_trans_2[0]])
        S1_a_obj = " ".join([D_trans_1[0], NP_trans_1[0], Aux_trans[0], V_trans[0], "a", NP_trans_2[0]])
        S1_the_a = " ".join(["the", NP_trans_1[0], Aux_trans[0], V_trans[0], "a", NP_trans_2[0]])
        S1_a_the = " ".join(["a", NP_trans_1[0], Aux_trans[0], V_trans[0], "the", NP_trans_2[0]])
        S1_abs = " ".join(["%s", NP_trans_1[0], Aux_trans[0], V_trans[0], "%s", NP_trans_2[0]])

        option = random.choice([1, 2, 3])
        if option == 1:     # subject control/raising
            V_control_in = choice(self.v_control_subj_in)
            NP1 = choice(get_matches_of(V_control_in, "arg_1", self.safe_nouns))
            D1 = choice(get_matched_by(NP1, "arg_1", self.safe_dets))
            Aux1 = return_aux(V_control_in, NP1)
            V = choice(get_matches_of(V_control_in, "arg_2", get_matched_by(NP1, "arg_1", self.all_bare_transitive_verbs)))
            NP2 = choice(get_matches_of(V, "arg_2", self.safe_nouns))
            D2 = choice(get_matched_by(NP2, "arg_1", self.safe_dets))
            V_control_out = choice(get_matched_by(NP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(V, "arg_2", self.v_control_subj_out))))
            V_raising_in = choice(get_matched_by(NP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(V, "arg_2", self.v_raising_subj_in))))
            V_raising_out = choice(get_matched_by(NP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(V, "arg_2", self.v_raising_subj_out))))
            to = "to"
        elif option == 2:       # object control/raising
            V_control_in = choice(self.v_control_obj_in)
            NP1 = choice(get_matches_of(V_control_in, "arg_1", self.safe_nouns))
            D1 = choice(get_matched_by(NP1, "arg_1", self.safe_dets))
            Aux1 = return_aux(V_control_in, NP1)
            control_obj = N_to_DP_mutate(choice(get_matches_of(V_control_in, "arg_2")))
            V = choice(get_matches_of(V_control_in, "arg_3", get_matched_by(NP1, "arg_1", self.all_bare_transitive_verbs)))
            NP2 = choice(get_matches_of(V, "arg_2", self.safe_nouns))
            D2 = choice(get_matched_by(NP2, "arg_1", self.safe_dets))
            V_control_out = choice(get_matched_by(NP1, "arg_1",
                                                  get_matches_of(Aux1, "arg_2",
                                                                 get_matched_by(V, "arg_3",
                                                                                get_matched_by(NP2, "arg_2", self.v_control_obj_out)))))

            try:
                V_raising_in = choice(get_matched_by(NP1, "arg_1",
                                                 get_matches_of(Aux1, "arg_2", self.v_raising_obj_in)))
                V_raising_out = choice(get_matched_by(NP1, "arg_1",
                                                      get_matches_of(Aux1, "arg_2", self.v_raising_obj_out)))
            except Exception:
                pass
            to = control_obj[0] + " to"

        else:       # adjective control/raising
            V_control_in = choice(self.adj_control_subj_in)
            NP1 = choice(get_matches_of(V_control_in, "arg_1", all_common_nouns))
            D1 = choice(get_matched_by(NP1, "arg_1", self.safe_dets))
            Aux1 = return_copula(NP1)
            V = choice(get_matches_of(V_control_in, "arg_2", get_matched_by(NP1, "arg_1", self.all_bare_transitive_verbs)))
            NP2 = choice(get_matches_of(V, "arg_2", all_common_nouns))
            D2 = choice(get_matched_by(NP2, "arg_1", self.safe_dets))
            V_control_out = choice(get_matched_by(NP1, "arg_1",
                                                  get_matched_by(V, "arg_2", self.adj_control_subj_out)))
            V_raising_in = choice(self.adj_raising_subj_in)
            V_raising_out = choice(self.adj_raising_subj_out)
            to = "to"

        # option = random.randint(0, 1)
        # if option == 1:
        #     training_1_1 = " ".join([S1_the_subj, "and", "a", NP1[0], Aux1[0], V_control_in[0], to, V[0], D2[0], NP2[0], "."])
        #     control_1_0 = " ".join([S1_a_subj, "and", "the", NP1[0], Aux1[0], V_control_in[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     training_1_1 = " ".join(["the", NP1[0], Aux1[0], V_control_in[0], to, V[0], "the", NP2[0], "and", S1, "."])
        #
        # option = random.randint(0, 1)
        # if option == 1:
        #     test_0_1 = " ".join([S1_the_subj, "and", D1[0], NP1[0], Aux1[0], V_raising_out[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     test_0_1 = " ".join(["the", NP1[0], Aux1[0], V_raising_out[0], to, V[0], D2[0], NP2[0], "and", S1, "."])
        #
        # option = random.randint(0, 1)
        # if option == 1:
        #     control_1_1 = " ".join([S1_the_subj, "and", D1[0], NP1[0], Aux1[0], V_control_out[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     control_1_1 = " ".join(["the", NP1[0], Aux1[0], V_control_out[0], to, V[0], D2[0], NP2[0], "and", S1, "."])
        #
        # option = random.randint(0, 1)
        # if option == 1:
        #     control_0_1 = " ".join([S1_the_subj, "and", D1[0], NP1[0], Aux1[0], V_raising_in[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     control_0_1 = " ".join(["the", NP1[0], Aux1[0], V_raising_in[0], to, V[0], D2[0], NP2[0], "and", S1, "."])
        #
        #
        # option = random.randint(0, 1)
        # if option == 1:
        #     training_0_0 = " ".join([S1_the_obj, "and", D1[0], NP1[0], Aux1[0], V_raising_in[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     training_0_0 = " ".join([D1[0], NP1[0], Aux1[0], V_raising_in[0], to, V[0], "the", NP2[0], "and", S1, "."])
        #
        # option = random.randint(0, 1)
        # if option == 1:
        #     test_1_0 = " ".join([S1_the_obj, "and", D1[0], NP1[0], Aux1[0], V_control_out[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     test_1_0 = " ".join([D1[0], NP1[0], Aux1[0], V_control_out[0], to, V[0], "the", NP2[0], "and", S1, "."])
        #
        # option = random.randint(0, 1)
        # if option == 1:
        #     control_0_0 = " ".join([S1_the_obj, "and", D1[0], NP1[0], Aux1[0], V_raising_out[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     control_0_0 = " ".join([D1[0], NP1[0], Aux1[0], V_raising_out[0], to, V[0], "the", NP2[0], "and", S1, "."])
        #
        # option = random.randint(0, 1)
        # if option == 1:
        #     control_1_0 = " ".join([S1_the_obj, "and", D1[0], NP1[0], Aux1[0], V_control_in[0], to, V[0], D2[0], NP2[0], "."])
        # else:
        #     control_1_0 = " ".join([D1[0], NP1[0], Aux1[0], V_control_in[0], to, V[0], "the", NP2[0], "and", S1, "."])

        Ds = []
        option = random.choice([1, 2, 3])  # There are three in-domain configurations (arbitrarily chosen)
        if option == 1:
            Ds.append(("the", "a", D1[0], D2[0]))
            Ds.append(("a", "the", D1[0], D2[0]))
        elif option == 2:
            Ds.append(("the", D_trans_2[0], D1[0], "a"))
            Ds.append(("a", D_trans_2[0], D1[0], "the"))
        else:
            Ds.append((D_trans_1[0], "the", D1[0], "a"))
            Ds.append((D_trans_1[0], "a", D1[0], "the"))

        option = random.choice([1, 2, 3])  # There are three out-domain configurations (arbitrarily chosen)
        if option == 1:
            Ds.append(("the", D_trans_2[0], "a", D2[0]))
            Ds.append(("a", D_trans_2[0], "the", D2[0]))
        elif option == 2:
            Ds.append((D_trans_1[0], "the", "a", D2[0]))
            Ds.append((D_trans_1[0], "a", "the", D2[0]))
        else:
            Ds.append((D_trans_1[0], D_trans_2[0], "the", "a"))
            Ds.append((D_trans_1[0], D_trans_2[0], "a", "the"))

        data = self.build_paradigm(
            training_1_1=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_control_in[0], to, V[0], "%s", NP2[0], "."]) % Ds[0],
            training_0_0=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_raising_in[0], to, V[0], "%s", NP2[0], "."]) % Ds[1],
            control_1_0=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_control_in[0], to, V[0], "%s", NP2[0], "."]) % Ds[1],
            control_0_1=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_raising_in[0], to, V[0], "%s", NP2[0], "."]) % Ds[0],
            test_1_0=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_control_out[0], to, V[0], "%s", NP2[0], "."]) % Ds[3],
            test_0_1=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_raising_out[0], to, V[0], "%s", NP2[0], "."]) % Ds[2],
            control_1_1=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_control_out[0], to, V[0], "%s", NP2[0], "."]) % Ds[2],
            control_0_0=" ".join([S1_abs, "and", "%s", NP1[0], Aux1[0], V_raising_out[0], to, V[0], "%s", NP2[0], "."]) % Ds[3],
        )

        track_sentence = [
            (NP1[0], Aux1[0], V_control_in[0], to, V[0], NP2[0], "."),
            (NP1[0], Aux1[0], V_raising_in[0], to, V[0], NP2[0], "."),
            (NP1[0], Aux1[0], V_control_out[0], to, V[0], NP2[0], "."),
            (NP1[0], Aux1[0], V_raising_out[0], to, V[0], NP2[0], "."),
            (NP1[0], Aux1[0], V_control_out[0], to, V[0], NP2[0], "."),
            (NP1[0], Aux1[0], V_raising_out[0], to, V[0], NP2[0], ".")
        ]

        return data, track_sentence









generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
