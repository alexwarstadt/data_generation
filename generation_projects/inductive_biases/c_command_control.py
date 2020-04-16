from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
# import generation_projects.inductive_biases.person_helper

class MyGenerator(data_generator.InductiveBiasesGenerator):
    def __init__(self):
        super().__init__(uid="c_command_same_control",
                         linguistic_feature_type="relative syntactic position / semantic reading",
                         linguistic_feature_description="Does the universal quantifier c-command same/different? / Does an internal (bound) reading exist?",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)

        self.universal_quantifiers = np.array(list(filter(lambda x: x["expression"] in ["every", "all", "each"], get_all("category_2", "D"))))
        self.embedding_verbs = np.union1d(get_all("category_2", "V_raising_object"),
                                          np.union1d(get_all("category_2", "V_control_object"),
                                                     get_all("category_2", "V_embedding")))
        self.singular_indefs = list(filter(lambda x: x["expression"] in ["a", "an"], get_all("category_2", "D")))
        self.indefs = list(filter(lambda x: x["expression"] in ["a", "an", ""], get_all("category_2", "D")))
        self.safe_dets = list(filter(lambda x: x["expression"] in ["a", "an", "the", "this", "these", "that", "those",
                                                                   "an", "the",], get_all("category_2", "D")))
        self.to = get_all("expression", "to")[0]
        self.all_bare_transitive_verbs = np.intersect1d(all_transitive_verbs, all_transitive_verbs)


    def sample(self):
        # Training 1
        # Every man who      read the book      told a boy to   see the same  movie.
        # Q     NP1 rel Aux1 V1   D2  NP2  Aux2 V2   A NP3 Aux3 V3  D4  recip NP4

        # Training 0
        # The man who      read every book      told a  boy to   see the same  movie.
        # D2  NP1 rel Aux1 V1   Q     NP2  Aux2 V2   A  NP3 Aux3 V3  D4  recip NP4

        # Test 1
        # The man      told every boy  reading the book to   see the same  movie.
        # D1  NP1 Aux2 V2   Q     NP3  V1ing   D2  NP2  Aux3 V3  D4  recip NP4

        # Test 0
        # The man      told that boy  reading every book to   see the same  movie.
        # D1  NP1 Aux2 V2   D3   NP3  V1ing   Q     NP2  Aux3 V3  D4  recip NP4


        V2 = choice(self.embedding_verbs)
        NP1 = choice(get_matches_of(V2, "arg_1", all_common_nouns))
        Q = choice(get_matched_by(NP1, "arg_1", self.universal_quantifiers))
        Aux2 = return_aux(V2, NP1)
        rel = get_matches_of(NP1, "arg_1", all_relativizers)

        if V2["category_2"] == "V_control_object":
            NP3 = choice(get_matches_of(V2, "arg_2", get_matches_of(Q, "arg_1", all_singular_nouns)))
            V3 = choice(get_matches_of(V2, "arg_3", all_transitive_verbs))
            Aux3 = self.to

        elif V2["category_2"] == "V_raising_object":
            V3 = choice(self.all_bare_transitive_verbs)
            Aux3 = self.to
            NP3 = choice(get_matches_of(V3, "arg_1"))
        else:
            V3 = choice(all_transitive_verbs)
            NP3 = choice(get_matches_of(V3, "arg_1"))
            Aux3 = return_aux(V3, NP3)

        A = choice(get_matched_by(NP3, "arg_1", self.singular_indefs))
        D3 = choice(get_matched_by(NP3, "arg_1", self.safe_dets))
        NP4 = choice(get_matches_of(V3, "arg_2"))
        if bool(random.getrandbits(1)):
            D4, recip = "the", "same"
        else:
            D4, recip = choice(get_matched_by(NP4, "arg_1", self.indefs)), "different"
        options = [1,2]
        while len(options) > 0:
            option = random.choice(options)
            options.remove(option)
            if option == 1:     #subj, subj
                V1 = choice(get_matched_by(NP1, "arg_1", get_matched_by(NP3, "arg_1", all_transitive_verbs)))
                V1ing = choice(get_all("ing", "1", get_all("root", V1["root"])))
                NP2 = choice(get_matches_of(V1, "arg_2"))
                Aux1 = return_aux(V1, NP1)
            else:   #obj, obj
                V1 = choice(get_matched_by(NP1, "arg_2", get_matched_by(NP3, "arg_2", all_transitive_verbs)))
                V1ing = choice(get_all("en", "1", get_all("root", V1["root"])))
                NP2 = choice(get_matches_of(V1, "arg_1"))
                Aux1 = return_aux(V1, NP2)
        D2 = choice(get_matched_by(NP2, "arg_1", self.safe_dets))

        track_sentence = " ".join([Q[0], NP1[0], rel[0], Aux1[0], V1[0], D2[0], NP2[0], Aux2[0], V2[0], A[0], NP3[0], Aux3[0], V3[0], D4[0], recip, NP4[0]])






        

        # track_sentence = "%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0])
        data = {}
        #
        # data = self.build_paradigm(
        #     training_1_1="%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
        #     training_0_0="%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
        #     test_1_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
        #     test_0_1="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
        # )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
