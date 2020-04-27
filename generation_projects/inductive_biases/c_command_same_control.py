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
        self.all_singular_intransitive_verbs = np.intersect1d(all_possibly_singular_verbs, all_intransitive_verbs)
        # self.possibly_ing_transitive_verbs = reduce(lambda x, y: np.union1d(x, y), [get_all("root", v["root"], all_transitive_verbs) for v in self.all_bare_transitive_verbs])

    def sample(self):
        if bool(random.choice([0, 1])):
            return self.sample_modified_NP()
        else:
            return self.sample_coordination()


    def sample_modified_NP(self):
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
        Aux2 = return_aux(V2, NP1, allow_negated=False)
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
            Aux3 = return_aux(V3, NP3, allow_negated=False)

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
        Aux1 = return_aux(V1, NP1, allow_negated=False)

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
                                   NP3[0], Aux3[0], V3[0], Ds[0][3], NP4[0], "."]),
            training_0_0=" ".join([Ds[1][0], NP1[0], rel[0], Aux1[0], V1[0], Ds[1][1], NP2[0], Aux2[0], V2[0], Ds[1][2],
                                   NP3[0], Aux3[0], V3[0], Ds[1][3], NP4[0], "."]),
            test_1_0=" ".join([Ds[2][0], NP1[0], Aux2[0], V2[0], Ds[2][1], NP3[0], V1ing[0], Ds[2][2], NP2[0], Aux3[0],
                               V3[0], Ds[2][3], NP4[0], "."]),
            test_0_1=" ".join([Ds[3][0], NP1[0], Aux2[0], V2[0], Ds[3][1], NP3[0], V1ing[0], Ds[3][2], NP2[0], Aux3[0],
                               V3[0], Ds[3][3], NP4[0], "."])
        )

        track_sentence = [
            (NP1[0], V1[0], NP2[0], V2[0], NP3[0], V3[0], NP4[0], recip)
        ]

        return data, track_sentence



    def sample_coordination(self):
        # Training 1
        # A    man      slept or every girl      helped the  same  dog.
        # D1_1 NP1 Aux1 IV    OR D2_1  NP2  Aux2 V2     D3_1       NP3

        # Training
        # Every man      slept or the  same girl      helped a     dog.
        # D1_2  NP1 Aux1 IV    OR D2_2      NP2  Aux2 V2     D3_2  NP3

        # Test 1
        # Every man      loved a    girl or      helped the same dog.
        # D1_3  NP1 Aux1 TV    D2_3 NP2  OR Aux2 V2     D3_3     NP3

        # Test 0
        # A    man      loved every girl or      helped the same dog.
        # D1_4 NP1 Aux1 TV    D2_4  NP2  OR Aux2 V2     D3_4     NP3

        IV = choice(self.all_singular_intransitive_verbs)
        try:
            NP1 = choice(get_matches_of(IV, "arg_1", self.all_singular_common_nouns))
        except Exception:
            pass
        Aux1 = return_aux(IV, NP1, allow_negated=False)
        TV = choice(get_matched_by(NP1, "arg_1", get_matches_of(Aux1, "arg_2", all_transitive_verbs)))
        NP2 = choice(get_matches_of(TV, "arg_2", self.all_singular_common_nouns))
        V2 = choice(get_matched_by(NP1, "arg_1", get_matched_by(NP2, "arg_1", all_transitive_verbs)))
        Aux2 = return_aux(V2, NP2, allow_negated=False)
        NP3 = choice(get_matches_of(V2, "arg_2", self.all_singular_common_nouns))

        recip = random.choice(["the same", "a different"])
        D1 = choice(get_matched_by(NP1, "arg_1", self.singular_indefs))
        D2 = choice(get_matched_by(NP2, "arg_1", self.singular_indefs))
        D3 = choice(get_matched_by(NP3, "arg_1", self.singular_indefs))

        reverse = bool(random.choice([0, 1]))

        Ds = []
        # There is one possible pattern for training example with label 1
        Ds.append([D1[0], "every", recip])

        # There are two possible patterns for training example with label 0
        if reverse:
            option = random.choice([1, 2])
            if option == 1:
                Ds.append(["every", recip, D3[0]])
            elif option == 2:
                Ds.append(["every", D2[0], recip])
        else:
            option = random.choice([1, 2])
            if option == 1:
                Ds.append([recip, "every", D3[0]])
            elif option == 2:
                Ds.append([recip, D2[0], "every"])

        # There are two possible patterns for test example with label 1
        option = random.choice([1, 2])
        if option == 1:
            Ds.append(["every", recip, D3[0]])
        elif option == 2:
            Ds.append(["every", D2[0], recip])

        # There's only one possible pattern for test example with label 0
        Ds.append([D1[0], "every", recip])

        # We can reverse the order of the clauses in the training example for variety
        clause_1_a = " ".join([Ds[0][0], NP1[0], Aux1[0], IV[0]])
        clause_1_b = " ".join([Ds[0][1], NP2[0], Aux2[0], V2[0], Ds[0][2], NP3[0]])
        clause_0_a = " ".join([Ds[1][0], NP1[0], Aux1[0], IV[0]])
        clause_0_b = " ".join([Ds[1][1], NP2[0], Aux2[0], V2[0], Ds[1][2], NP3[0]])

        if reverse:
            training_1_1 = "%s or %s." % (clause_1_a, clause_1_b)
            training_0_0 = "%s or %s." % (clause_0_a, clause_0_b)
        else:
            training_1_1 = "%s or %s." % (clause_1_b, clause_1_a)
            training_0_0 = "%s or %s." % (clause_0_b, clause_0_a)

        data = self.build_paradigm(
            training_1_1=training_1_1,
            training_0_0=training_0_0,
            test_1_0=" ".join([Ds[2][0], NP1[0], Aux1[0], TV[0], Ds[2][1], NP2[0], "or", Aux2[0], V2[0], Ds[2][2], NP3[0], "."]),
            test_0_1=" ".join([Ds[3][0], NP1[0], Aux1[0], TV[0], Ds[3][1], NP2[0], "or", Aux2[0], V2[0], Ds[3][2], NP3[0], "."])
        )

        track_sentence = [
            (NP1[0], NP2[0], NP3[0], IV[0], TV[0], V2[0], recip)
        ]

        return data, track_sentence


generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
