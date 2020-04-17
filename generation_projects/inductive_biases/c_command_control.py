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

        # self.universal_quantifiers = np.array(list(filter(lambda x: x["expression"] in ["every", "all", "each"], get_all("category_2", "D"))))
        self.embedding_verbs = np.intersect1d(all_possibly_singular_verbs,
                                              np.union1d(get_all("category_2", "V_raising_object"),
                                                         np.union1d(get_all("category_2", "V_control_object"),
                                                                    get_all("category_2", "V_embedding"))))
        self.all_possibly_singular_transitive_verbs = np.intersect1d(all_possibly_singular_verbs, all_transitive_verbs)
        self.singular_indefs = np.array(list(filter(lambda x: x["expression"] in ["a", "an"], get_all("category_2", "D"))))
        self.indefs = np.array(list(filter(lambda x: x["expression"] in ["a", "an", ""], get_all("category_2", "D"))))
        self.safe_dets = np.array(list(filter(lambda x: x["expression"] in ["a", "an", "the", "this", "these", "that", "those",
                                                                   "an", "the", ], get_all("category_2", "D"))))
        self.to = get_all("expression", "to")[0]
        self.all_bare_transitive_verbs = np.intersect1d(all_transitive_verbs, all_bare_verbs)
        self.all_singular_common_nouns = np.intersect1d(all_singular_count_nouns, all_common_nouns)
        ing = []
        for v in all_ing_verbs:
            verbs = get_all("root", v["root"], all_transitive_verbs)
            if len(verbs) > 0:
                ing.extend(verbs)
        self.possibly_ing_transitive_verbs = np.array(ing)
        # self.possibly_ing_transitive_verbs = reduce(lambda x, y: np.union1d(x, y), [get_all("root", v["root"], all_transitive_verbs) for v in self.all_bare_transitive_verbs])

    def sample(self):
        # Training 1
        # Every man who      read the  book      told a    boy to   see the  same  movie.
        # D1_1  NP1 rel Aux1 V1   D2_1 NP2  Aux2 V2   D3_1 NP3 Aux3 V3  D4_1 recip NP4

        # Training 0
        # The  man who      read every book      told a    boy to   see the  same  movie.
        # D2_2 NP1 rel Aux1 V1   D2_2  NP2  Aux2 V2   D3_2 NP3 Aux3 V3  D4_2 recip NP4

        # Test 1
        # The  man      told every boy  reading the  book to   see the  same  movie.
        # D1_3 NP1 Aux2 V2   D3_3  NP3  V1ing   D2_3 NP2  Aux3 V3  D4_3 recip NP4

        # Test 0
        # The  man      told that boy  reading every book to   see the  same  movie.
        # D1_4 NP1 Aux2 V2   D3_4 NP3  V1ing   D2_4  NP2  Aux3 V3  D4_4 recip NP4

        V2 = choice(self.embedding_verbs)
        NP1 = choice(get_matches_of(V2, "arg_1", self.all_singular_common_nouns))
        Aux2 = return_aux(V2, NP1)
        rel = choice(get_matched_by(NP1, "arg_1", all_relativizers))

        if V2["category_2"] == "V_control_object":
            NP3 = choice(get_matches_of(V2, "arg_2", self.all_singular_common_nouns))
            V3 = choice(get_matches_of(V2, "arg_3", self.all_bare_transitive_verbs))
            Aux3 = self.to

        elif V2["category_2"] == "V_raising_object":
            V3 = choice(self.all_bare_transitive_verbs)
            Aux3 = self.to
            NP3 = choice(get_matches_of(V3, "arg_1", self.all_singular_common_nouns))
        else:   # clause embedding verb
            V2[0] = V2[0] + " that"
            V3 = choice(self.all_possibly_singular_transitive_verbs)
            NP3 = choice(get_matches_of(V3, "arg_1", self.all_singular_common_nouns))
            Aux3 = return_aux(V3, NP3)

        try:
            NP4 = choice(get_matches_of(V3, "arg_2", self.all_singular_common_nouns))
        except Exception:
            pass

        V1 = choice(get_matched_by(NP1, "arg_1", get_matched_by(NP3, "arg_1", self.possibly_ing_transitive_verbs)))
        try:
            V1ing = choice(get_all("ing", "1", get_all("root", V1["root"])))
        except Exception:
            pass
        NP2 = choice(get_matches_of(V1, "arg_2", self.all_singular_common_nouns))
        Aux1 = return_aux(V1, NP1)

        recip = random.choice(["the same", "a different"])
        try:
            D1 = choice(get_matched_by(NP1, "arg_1", self.singular_indefs))
            D2 = choice(get_matched_by(NP2, "arg_1", self.singular_indefs))
            D3 = choice(get_matched_by(NP3, "arg_1", self.singular_indefs))
            D4 = choice(get_matched_by(NP4, "arg_1", self.singular_indefs))
        except Exception:
            pass

        # There are four possible patterns for training example with label 1
        Ds = []
        option = random.choice([1, 2, 3])
        if option == 1:
            Ds.append(["every", D2[0], recip, D4[0]])
        elif option == 2:
            Ds.append(["every", D2[0], D3[0], recip])
        elif option == 3:
            Ds.append([D1[0], D2[0], "every", recip])

        # There are two possible patterns for training example with label 0
        option = random.choice([1, 2])
        if option == 1:
            Ds.append([D1[0], "every", recip, D4[0]])
        elif option == 2:
            Ds.append([D1[0], "every", D3[0], recip])

        # There are four possible patterns for test example with label 1
        option = random.choice([1, 2, 3, 4])
        if option == 1:
            Ds.append(["every", recip, D2[0], D4[0]])
        elif option == 2:
            Ds.append(["every", D3[0], recip, D4[0]])
        elif option == 3:
            Ds.append(["every", D3[0], D2[0], recip])
        elif option == 4:
            Ds.append([D1[0], "every", D2[0], recip])

        # There's only one possible pattern for test example with label 0
        Ds.append([D1[0], D2[0], "every", recip])

        data = self.build_paradigm(
            training_1_1=" ".join([Ds[0][0], NP1[0], rel[0], Aux1[0], V1[0], Ds[0][1], NP2[0], Aux2[0], V2[0], Ds[0][2],
                                   NP3[0], Aux3[0], V3[0], Ds[0][3], NP4[0]]),
            training_0_0=" ".join([Ds[1][0], NP1[0], rel[0], Aux1[0], V1[0], Ds[1][1], NP2[0], Aux2[0], V2[0], Ds[1][2],
                                   NP3[0], Aux3[0], V3[0], Ds[1][3], NP4[0]]),
            test_1_0=" ".join([Ds[2][0], NP1[0], Aux2[0], V2[0], Ds[2][1], NP3[0], V1ing[0], Ds[2][2], NP2[0], Aux3[0],
                               V3[0], Ds[2][3], NP4[0]]),
            test_0_1=" ".join([Ds[3][0], NP1[0], Aux2[0], V2[0], Ds[3][1], NP3[0], V1ing[0], Ds[3][2], NP2[0], Aux3[0],
                               V3[0], Ds[3][3], NP4[0]])
        )

        track_sentence = [
            (NP1[0], V1[0], NP2[0], V2[0], NP3[0], V3[0], NP4[0], recip)
        ]

        return data, track_sentence


generator = MyGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)

# from utils import data_generator
# from utils.constituent_building import *
# from utils.conjugate import *
# from utils.randomize import choice
# import random
# # import generation_projects.inductive_biases.person_helper
#
# class MyGenerator(data_generator.InductiveBiasesGenerator):
#     def __init__(self):
#         super().__init__(uid="c_command_same_control",
#                          linguistic_feature_type="relative syntactic position / semantic reading",
#                          linguistic_feature_description="Does the universal quantifier c-command same/different? / Does an internal (bound) reading exist?",
#                          surface_feature_type=None,
#                          surface_feature_description=None,
#                          control_paradigm=True)
#
#         # self.universal_quantifiers = np.array(list(filter(lambda x: x["expression"] in ["every", "all", "each"], get_all("category_2", "D"))))
#         self.embedding_verbs = np.union1d(get_all("category_2", "V_raising_object"),
#                                           np.union1d(get_all("category_2", "V_control_object"),
#                                                      get_all("category_2", "V_embedding")))
#         self.singular_indefs = list(filter(lambda x: x["expression"] in ["a", "an"], get_all("category_2", "D")))
#         self.indefs = list(filter(lambda x: x["expression"] in ["a", "an", ""], get_all("category_2", "D")))
#         self.safe_dets = list(filter(lambda x: x["expression"] in ["a", "an", "the", "this", "these", "that", "those",
#                                                                    "an", "the",], get_all("category_2", "D")))
#         self.to = get_all("expression", "to")[0]
#         self.all_bare_transitive_verbs = np.intersect1d(all_transitive_verbs, all_transitive_verbs)
#         self.all_singular_common_nouns = np.intersect1d(all_singular_count_nouns, all_common_nouns)
#
#
#     def sample(self):
#         # Training 1
#         # Every man who      read the  book      told a    boy to   see the  same  movie.
#         # D1_1  NP1 rel Aux1 V1   D2_1 NP2  Aux2 V2   D3_1 NP3 Aux3 V3  D4_1 recip NP4
#
#         # Training 0
#         # The  man who      read every book      told a    boy to   see the  same  movie.
#         # D2_2 NP1 rel Aux1 V1   D2_2  NP2  Aux2 V2   D3_2 NP3 Aux3 V3  D4_2 recip NP4
#
#         # Test 1
#         # The  man      told every boy  reading the  book to   see the  same  movie.
#         # D1_3 NP1 Aux2 V2   D3_3  NP3  V1ing   D2_3 NP2  Aux3 V3  D4_3 recip NP4
#
#         # Test 0
#         # The  man      told that boy  reading every book to   see the  same  movie.
#         # D1_4 NP1 Aux2 V2   D3_4 NP3  V1ing   D2_4  NP2  Aux3 V3  D4_4 recip NP4
#
#
#         V2 = choice(self.embedding_verbs)
#         NP1 = choice(get_matches_of(V2, "arg_1", self.all_singular_common_nouns))
#         Aux2 = return_aux(V2, NP1)
#         rel = get_matches_of(NP1, "arg_1", all_relativizers)
#
#         if V2["category_2"] == "V_control_object":
#             NP3 = choice(get_matches_of(V2, "arg_2", self.all_singular_common_nouns))
#             V3 = choice(get_matches_of(V2, "arg_3", all_transitive_verbs))
#             Aux3 = self.to
#
#         elif V2["category_2"] == "V_raising_object":
#             V3 = choice(self.all_bare_transitive_verbs)
#             Aux3 = self.to
#             NP3 = choice(get_matches_of(V3, "arg_1", self.all_singular_common_nouns))
#         else:
#             V3 = choice(all_transitive_verbs)
#             NP3 = choice(get_matches_of(V3, "arg_1", self.all_singular_common_nouns))
#             Aux3 = return_aux(V3, NP3)
#
#         A = choice(get_matched_by(NP3, "arg_1", self.singular_indefs))
#         NP4 = choice(get_matches_of(V3, "arg_2"))
#         options = [1,2]
#         while len(options) > 0:
#             subj_or_obj = random.choice(options)
#             options.remove(subj_or_obj)
#             if subj_or_obj == 1:     #subj, subj
#                 V1 = choice(get_matched_by(NP1, "arg_1", get_matched_by(NP3, "arg_1", all_transitive_verbs)))
#                 V1ing = choice(get_all("ing", "1", get_all("root", V1["root"])))
#                 NP2 = choice(get_matches_of(V1, "arg_2", self.all_singular_common_nouns))
#                 Aux1 = return_aux(V1, NP1)
#                 RC = " ".join([rel[0], Aux1[0], V1[0], NP2[0]])
#                 Mod = " ".join([V1ing[0], NP2[0]])
#             else:   #obj, obj
#                 V1 = choice(get_matched_by(NP1, "arg_2", get_matched_by(NP3, "arg_2", all_transitive_verbs)))
#                 V1ing = choice(get_all("en", "1", get_all("root", V1["root"])))
#                 NP2 = choice(get_matches_of(V1, "arg_1", self.all_singular_common_nouns))
#                 Aux1 = return_aux(V1, NP2)
#                 RC = " ".join([rel[0], NP2[0], Aux1[0], V1[0]])
#                 Mod = " ".join([V1ing[0], "by", NP2[0]])
#
#         recip = random.choice(["the same", "a different"])
#         D1 = choice(get_matched_by(NP1, "arg_1", self.singular_indefs))
#         D2 = choice(get_matched_by(NP2, "arg_1", self.singular_indefs))
#         D3 = choice(get_matched_by(NP3, "arg_1", self.singular_indefs))
#         D4 = choice(get_matched_by(NP4, "arg_1", self.singular_indefs))
#
#         # There are four possible patterns for training example with label 1
#         option = random.choice([1,2,3,4])
#         if option == 1:
#             if subj_or_obj == 1:
#                 reconj1 = re_conjugate(V1, pluralize(NP1), Aux1)
#                 reconj2 = re_conjugate(V2, pluralize(NP1), Aux2)
#                 training_1_1 = " ".join(["three", NP1["pluralform"], ])
#             DPs.append(["three " + NP1["pluralform"], recip + " " + NP2[0], D3[0] + " " + NP3[0], D4[0] + " " + NP4[0]])
#         elif option == 2:
#             DPs.append(["three " + NP1["pluralform"], D2[0] + " " + NP2[0], recip + " " + NP3[0], D4[0] + " " + NP4[0]])
#         elif option == 3:
#             DPs.append(["three " + NP1["pluralform"], D2[0] + " " + NP2[0], D3[0] + " " + NP3[0], recip + " " + NP4[0]])
#         elif option == 4:
#             DPs.append([D1[0] + " " + NP1[0], D2[0] + " " + NP2[0], "three " + NP3["pluralform"], recip + " " + NP4[0]])
#
#         # There are two possible patterns for training example with label 0
#         option = random.choice([1, 2])
#         if option == 1:
#             DPs.append([D1[0] + " " + NP1[0], "three " + NP2["pluralform"], recip + " " + NP3[0], D4[0] + " " + NP4[0]])
#         elif option == 2:
#             DPs.append([D1[0] + " " + NP1[0], "three " + NP2["pluralform"], D3[0] + " " + NP3[0], recip + " " + NP4[0]])
#
#         # There are five possible patterns for test example with label 1
#         option = random.choice([1,2,3,4,5])
#         if option == 1:
#             DPs.append(["three " + NP1["pluralform"], recip + " " + NP3[0], D2[0] + " " + NP2[0], D4[0] + " " + NP4[0]])
#         elif option == 2:
#             DPs.append(["three " + NP1["pluralform"], D3[0] + " " + NP3[0], recip + " " + NP2[0], D4[0] + " " + NP4[0]])
#         elif option == 3:
#             DPs.append(["three " + NP1["pluralform"], D3[0] + " " + NP3[0], D2[0] + " " + NP2[0], recip + " " + NP4[0]])
#         elif option == 4:
#             DPs.append([D1[0] + " " + NP1[0], "three " + NP3["pluralform"], recip + " " + NP2[0], D4[0] + " " + NP4[0]])
#         elif option == 5:
#             DPs.append([D1[0] + " " + NP1[0], "three " + NP3["pluralform"], D2[0] + " " + NP2[0], recip + " " + NP4[0]])
#
#         # There's only one possible pattern for test example with label 0
#         DPs.append(
#             [D1[0] + " " + NP1[0], D2[0] + " " + NP2[0], "three " + NP3["pluralform"], recip + " " + NP4[0]])
#
#
#
#         if subj_or_obj == 1:
#             data = self.build_paradigm(
#                 training_1_1=" ".join([DPs[0][0], rel[0], Aux1[0], V1[0], DPs[0][1], Aux2[0], V2[0], DPs[0][2], Aux3[0], V3[0], DPs[0][3]]),
#                 training_0_0=" ".join([DPs[0][0], rel[0], Aux1[0], V1[0], DPs[0][1], Aux2[0], V2[0], DPs[0][2], Aux3[0], V3[0], DPs[0][3]]),
#                 test_1_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
#                 test_0_1="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
#             )
#
#         # Q = choice(get_matched_by(NP1, "arg_1", self.universal_quantifiers))
#         # D3 = choice(get_matched_by(NP3, "arg_1", self.safe_dets))
#         # if bool(random.getrandbits(1)):
#         #     D4, recip = "the", "same"
#         # else:
#         #     D4, recip = choice(get_matched_by(NP4, "arg_1", self.indefs)), "different"
#         # D2 = choice(get_matched_by(NP2, "arg_1", self.safe_dets))
#
#         track_sentence = " ".join([Q[0], NP1[0], rel[0], Aux1[0], V1[0], D2[0], NP2[0], Aux2[0], V2[0], A[0], NP3[0], Aux3[0], V3[0], D4[0], recip, NP4[0]])
#
#
#
#
#
#
#
#
#         # track_sentence = "%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0])
#         data = {}
#         #
#         # data = self.build_paradigm(
#         #     training_1_1="%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
#         #     training_0_0="%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
#         #     test_1_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
#         #     test_0_1="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
#         # )
#         return data, track_sentence
#
# generator = MyGenerator()
# generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
