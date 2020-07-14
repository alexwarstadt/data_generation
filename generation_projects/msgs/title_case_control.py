from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
from titlecase import titlecase
import generation_projects.msgs.person_helper

class MyGenerator(data_generator.InductiveBiasesGenerator):
    def __init__(self):
        super().__init__(uid="title_case_control",
                         linguistic_feature_type=None,
                         linguistic_feature_description=None,
                         surface_feature_type="orthography",
                         surface_feature_description="Does the sentence appear in title case?",
                         control_paradigm=True)

        # match_a = get_matches_of(get_all("expression", "a", all_very_common_dets)[0], "arg_1")
        # self.safe_animate_common_nouns = get_matches_of(get_all("expression", "a", all_very_common_dets)[0], "arg_1", all_common_nouns)
        # self.safe_dets = np.setdiff1d(np.setdiff1d(all_determiners, get_all("expression", "the")), get_all("expression", "none of the"))
        self.cp_verbs = get_all("category", "(S\\NP)/S")
        # self.possibly_singular_transitive_verbs = np.intersect1d(all_transitive_verbs, all_possibly_singular_verbs)
        # self.lower_words = []

    def sample(self):
        # Training 1/1
        # The man who helped a  girl thinks  that that guy found a  cat.
        # THE   NP1 rel V1   D2 NP2  cp_verb THAT D3   NP3 V2    D4 NP4

        # Training 0/0
        # This man who helped a  girl thinks  that that guy found the cat.
        # D1   NP1 rel V1     D2 NP2  cp_verb THAT D3   NP3 V2    THE NP4

        # Test 1/0
        # The  man thinks   that that guy  who helped a girl found a  cat.
        # THE  NP1  cp_verb THAT D3   NP3  rel V1     D2 NP2 V2    D4 NP4

        # Test 0/1
        # This man thinks  that that guy who helped the girl found the cat.
        # D1   NP1 cp_verb THAT D3  NP3  rel V1     THE NP2  V2    THE NP4


        cp_verb = choice(self.cp_verbs)
        try:
            NP1 = N_to_DP_mutate(choice(get_matches_of(cp_verb, "arg_1", all_common_nouns)))
        except Exception:
            pass
        # D1 = choice(get_matched_by(NP1, "arg_1", self.safe_dets))
        rel1 = choice(get_matched_by(NP1, "arg_1", all_relativizers))
        V1 = choice(get_matched_by(NP1, "arg_1", all_transitive_verbs))
        NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_common_nouns)))
        # D2 = choice(get_matched_by(NP2, "arg_1", self.safe_dets))
        rel2 = choice(get_matched_by(NP2, "arg_1", all_relativizers))
        Aux1 = return_aux(V1, NP1)
        NP3 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", get_matches_of(Aux1, "arg_1", all_common_nouns))))
        # D3 = choice(get_matched_by(NP3, "arg_1", self.safe_dets))
        V2 = choice(get_matched_by(NP3, "arg_1", all_transitive_verbs))
        NP4 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_2", all_common_nouns)))
        # D4 = choice(get_matched_by(NP4, "arg_1", self.safe_dets))
        Aux_cp = return_aux(cp_verb, NP1)
        Aux2 = return_aux(V2, NP3)


        track_sentence = [
                (NP1[0], V1[0], NP2[0], cp_verb[0], NP3[0], V2[0], NP4[0]),  #training 1/1
                (NP1[0], V1[0], NP2[0], cp_verb[0], NP3[0], V2[0], NP4[0]),  #training 0/0
                (NP1[0], V1[0], NP2[0], cp_verb[0], NP3[0], V2[0], NP4[0]),  #Test 1/0
                (NP1[0], V1[0], NP2[0], cp_verb[0], NP3[0], V2[0], NP4[0]),  #Test 0/1
            ]

        data = self.build_paradigm(
            training_1_1=titlecase(" ".join([NP1[0], rel1[0], Aux1[0], V1[0], NP2[0], Aux_cp[0], cp_verb[0],
                                   "that", NP3[0], Aux2[0], V2[0], NP4[0]])),
            training_0_0=" ".join([NP1[0], rel1[0], Aux1[0], V1[0], NP2[0], Aux_cp[0], cp_verb[0],
                                   "that", NP3[0], Aux2[0], V2[0], NP4[0]]),
            test_1_0=titlecase(" ".join([NP1[0], Aux_cp[0], cp_verb[0], "that", NP3[0],
                               rel2[0], Aux1[0], V1[0], NP2[0], Aux2[0], V2[0], NP4[0]])),
            test_0_1=" ".join([NP1[0], Aux_cp[0], cp_verb[0], "that", NP3[0],
                               rel2[0], Aux1[0], V1[0], NP2[0], Aux2[0], V2[0], NP4[0]]),
        )
        return data, track_sentence


generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/msgs/" + generator.uid)
