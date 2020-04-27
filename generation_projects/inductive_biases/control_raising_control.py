
from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random


# import generation_projects.inductive_biases.person_helper

class MyGenerator(data_generator.InductiveBiasesGenerator):
    def __init__(self):
        super().__init__(uid="control_raising_control",
                         linguistic_feature_type="syntactic construction",
                         linguistic_feature_description="Is the sentence an example of control or raising",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)

        def split_adjs(adjs):
            np.random.shuffle(adjs)
            in_domain = adjs[:int(len(adjs) / 2)]
            out_domain = adjs[int(len(adjs) / 2):]
            return in_domain, out_domain

        def split_verbs(verbs):
            verb_roots = list(set(verbs["root"]))
            np.random.shuffle(verb_roots)
            in_domain = list(filter(lambda x: x["root"] in verb_roots[:int(len(verb_roots) / 2)], verbs))
            out_domain = list(filter(lambda x: x["root"] in verb_roots[int(len(verb_roots) / 2):], verbs))
            return np.array(in_domain), np.array(out_domain)

        ambiguous_control_raising_roots = ["fail_(S\\NP)/(S[to]\\N)",
                                           "fail_S/S[to]",
                                           "look_S/S[to]",
                                           "threaten_S/S[to]",
                                           # "need_(S\NP)/(S[to]\N)",
                                           # "need_(S\NP)/S[to]",
                                           # "want_(S\NP)/(S[to]\N)",
                                           # "want_(S\NP)/S[to]",
                                           ]
        non_ambiguous_verbs = np.array(list(filter(lambda x: x["root"] not in ambiguous_control_raising_roots, all_verbs)))

        self.v_control_subj_in, self.v_control_subj_out = split_verbs(get_all("category_2", "V_control_subj", non_ambiguous_verbs))
        self.v_raising_subj_in, self.v_raising_subj_out = split_verbs(get_all("category_2", "V_raising_subj", non_ambiguous_verbs))
        self.v_control_obj_in, self.v_control_obj_out = split_verbs(get_all("category_2", "V_control_object", non_ambiguous_verbs))
        self.v_raising_obj_in, self.v_raising_obj_out = split_verbs(get_all("category_2", "V_raising_object", non_ambiguous_verbs))
        self.adj_control_subj_in, self.adj_control_subj_out = split_adjs(get_all("category_2", "Adj_control_subj"))
        self.adj_raising_subj_in, self.adj_raising_subj_out = split_adjs(get_all("category_2", "Adj_raising_subj"))
        self.safe_verbs = np.setdiff1d(non_ambiguous_verbs,
                                       np.array(list(reduce(lambda x, y: np.union1d(x, y),
                                                            [self.v_control_subj_in, self.v_control_subj_out,
                                                             self.v_raising_subj_in, self.v_raising_subj_out,
                                                             self.v_control_obj_in, self.v_control_obj_out,
                                                             self.v_raising_obj_in, self.v_raising_obj_out,
                                                             self.adj_control_subj_in, self.adj_control_subj_out,
                                                             self.adj_raising_subj_in, self.adj_raising_subj_out]))))


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
        option = random.choice([1, 2, 3])
        if option == 1:     # subject control/raising
            V_control_in = choice(self.v_control_subj_in)
            DP1 = N_to_DP_mutate(choice(get_matches_of(V_control_in, "arg_1")))
            Aux1 = return_aux(V_control_in, DP1)
            VP = V_to_VP_mutate(choice(get_matches_of(V_control_in, "arg_2", get_matched_by(DP1, "arg_1", all_bare_verbs))), aux=False)
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
            VP = V_to_VP_mutate(choice(get_matches_of(V_control_in, "arg_3", get_matched_by(DP2, "arg_1", all_bare_verbs))), aux=False)
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
            VP = V_to_VP_mutate(choice(get_matches_of(V_control_in, "arg_2", get_matched_by(DP1, "arg_1", all_bare_verbs))), aux=False)
            V_control_out = choice(get_matched_by(DP1, "arg_1",
                                                  get_matched_by(VP, "arg_2", self.adj_control_subj_out)))
            V_raising_in = choice(self.adj_raising_subj_in)
            V_raising_out = choice(self.adj_raising_subj_out)
            to = "to"


        data = self.build_paradigm(
            training_1_1=" ".join([DP1[0], Aux1[0], V_control_in[0], to, VP[0], "."]),
            training_0_0=" ".join([DP1[0], Aux1[0], V_raising_in[0], to, VP[0], "."]),
            test_1_0=" ".join([DP1[0], Aux1[0], V_control_out[0], to, VP[0], "."]),
            test_0_1=" ".join([DP1[0], Aux1[0], V_raising_out[0], to, VP[0], "."]),
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
