from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper

class MyGenerator(generation_projects.inductive_biases.person_helper.PersonGenerator):
    def __init__(self):
        super().__init__(uid="same_clause3_b_control",
                         linguistic_feature_type="syntactic",
                         linguistic_feature_description="Are the two adjectives ?",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)

        # simplify things by (1) using only finite verbs, (2) using only very frequent determiners, (3) using only "good" and "bad"
        self.safe_nouns = np.array(list(filter(lambda x: "public" not in x["expression"] 
                                                      and "Great" not in x["expression"] 
                                                      and "high" not in x["expression"], all_common_nouns)))
        self.safe_nouns = get_all("start_with_vowel", "0", self.safe_nouns)
        self.locales = get_all("locale", "1", self.safe_nouns)
        # self.safe_adjectives = np.array(list(filter(lambda x: "out in the open" != x["expression"], all_adjectives)))
        self.physical_nouns = get_all("physical", "1", self.safe_nouns)
        self.CP_verbs = get_all("category", "(S\\NP)/S", all_finite_verbs)
        self.CP_nouns = get_all("category", "N/S", all_nominals)
        self.all_transitive_verbs = np.intersect1d(all_finite_verbs, all_transitive_verbs)
        self.all_possibly_plural_transitive_verbs = np.intersect1d(self.all_transitive_verbs, all_possibly_plural_verbs)
        self.plural_noun = choice(all_plural_nouns)



    def sample(self):
        # Training 1
        # The boy might see the cat and the students bought the paper

        # Training 0
        # The boy might see the cat and the students shred the paper

        # Test 1
        # The boy might see the cat and the students found the book

        # Test 0
        # The boy might see the cat and the students understand the book

        track_sentence = []
        option = random.randint(0, 3)
        if option == 0:
            data_in, track_sentence_in = self.sample_rc_over_multiple_DPs()
        elif option == 1:
            data_in, track_sentence_in = self.sample_coordination_over_rc()
        elif option == 2:
            data_in, track_sentence_in = self.sample_nested_rc()
        else:
            data_in, track_sentence_in = self.sample_CP_noun()
        track_sentence.extend(track_sentence_in)

        option = random.randint(0, 2)
        if option == 0:
            data_out, track_sentence_out = self.sample_2_rcs()
        elif option == 1:
            data_out, track_sentence_out = self.sample_coordination()
        else:
            data_out, track_sentence_out = self.sample_CP_verb_RC()
        track_sentence.extend(track_sentence_out)

        data = self.build_paradigm(
            training_1_1=data_in[0],
            training_0_0=data_in[1],
            test_1_0=data_out[0],
            test_0_1=data_out[1]
        )

        return data, track_sentence



    def subject_relative_clause(self, subj):
        rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        V = choice(get_matched_by(subj, "arg_1", self.all_transitive_verbs))
        aux1 = return_aux(V, subj)
        obj = choice(get_matches_of(V, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(obj, "arg_1", all_very_common_dets))

        RC = " ".join([rel[0], aux1[0], V[0], D2[0], "%s", obj[0]])
        return RC, obj

    def object_relative_clause(self, obj):
        rel = choice(get_matched_by(obj, "arg_1", get_all("category_2", "rel")))
        V = choice(get_matched_by(obj, "arg_2", self.all_transitive_verbs))
        subj = choice(get_matches_of(V, "arg_1", self.safe_nouns))
        aux1 = return_aux(V, subj)
        D2 = choice(get_matched_by(subj, "arg_1", all_very_common_dets))
        RC = " ".join([rel[0], D2[0], "%s", subj[0], "%s", aux1[0], V[0]])
        return RC, subj

    def sample_coordination(self):

        V1 = choice(self.all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_very_common_dets))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", all_very_common_dets))
        S1 = " ".join([D1[0], "%s", NP1[0], aux1[0], V1[0], D2[0], "%s", NP2[0]])

        V2 = choice(self.all_transitive_verbs)
        NP3 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        aux2 = return_aux(V2, NP3)
        D3 = choice(get_matched_by(NP3, "arg_1", all_very_common_dets))
        NP4 = choice(get_matches_of(V2, "arg_2", self.safe_nouns))
        D4 = choice(get_matched_by(NP4, "arg_1", all_very_common_dets))
        S2 = " ".join([D3[0], "%s", NP3[0], aux2[0], V2[0], D4[0], "%s", NP4[0]])


        track_sentence = [
            (S1, S2),
            (S1, S2),
            ]

        data = []
        if bool(random.randint(0, 1)):
            data.append((S1 + " and " + S2) % ("good", "bad", "", ""))
        else:
            data.append((S1 + " and " + S2) % ("", "", "good", "bad"))

        option = random.randint(0, 3)
        if option == 0:
            data.append((S1 + " and " + S2) % ("good", "", "bad", ""))
        elif option == 1:
            data.append((S1 + " and " + S2) % ("good", "", "", "bad"))
        elif option == 2:
            data.append((S1 + " and " + S2) % ("", "good", "bad", ""))
        else:
            data.append((S1 + " and " + S2) % ("", "", "good", "bad"))

        return data, track_sentence

    def sample_coordination_over_rc(self):

        V1 = choice(self.all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_very_common_dets))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", all_very_common_dets))
        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])

        V2 = choice(self.all_transitive_verbs)
        NP3 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        aux2 = return_aux(V2, NP3)
        D3 = choice(get_matched_by(NP3, "arg_1", all_very_common_dets))
        NP4 = choice(get_matches_of(V2, "arg_2", self.safe_nouns))
        D4 = choice(get_matched_by(NP4, "arg_1", all_very_common_dets))
        S2 = " ".join([D3[0], "%s", NP3[0], "%s", aux2[0], V2[0], D4[0], "%s", NP4[0], "%s"])

        # def subject_relative_clause(subj):
        #     rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        #     V = choice(get_matched_by(subj, "arg_1", self.all_transitive_verbs))
        #     aux1 = return_aux(V, subj)
        #     obj = choice(get_matches_of(V, "arg_2", all_common_nouns))
        #     A = choice(get_matched_by(obj, "arg_1", self.safe_adjectives))
        #     D2 = choice(get_matched_by(obj, "arg_1", all_very_common_dets))
        #     RC = " ".join([rel[0], aux1[0], V[0], D2[0], "%s", obj[0]])
        #     return RC, A

        RC1, _ = self.subject_relative_clause(NP1)
        RC2, _ = self.subject_relative_clause(NP2)
        RC3, _ = self.subject_relative_clause(NP3)
        RC4, _ = self.subject_relative_clause(NP4)


        track_sentence = [
            (S1, S2),
            (S1, S2),
            ]

        data = []
        option = random.randint(0, 7)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % "", aux1[0], V1[0], D2[0], "bad", NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], RC1 % "", aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], "good", NP3[0], aux2[0], V2[0], D4[0], "bad", NP4[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], "bad", NP2[0], RC2 % "", "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % "", "and", D3[0], "good", NP3[0], aux2[0], V2[0], D4[0], "bad", NP4[0]]))
        elif option == 4:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], "bad", NP2[0], "and", D3[0], NP3[0], RC3 % "", aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], "good", NP3[0], RC3 % "", aux2[0], V2[0], D4[0], "bad", NP4[0]]))
        elif option == 6:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], "bad", NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % ""]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], "good", NP3[0], aux2[0], V2[0], D4[0], "bad", NP4[0], RC4 % ""]))


        option = random.randint(0, 1)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % "bad", aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], RC1 % "good", aux1[0], V1[0], D2[0], "bad", NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], NP1[0], RC1 % "good", aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], "bad", NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % "good", aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], "bad", NP4[0]]))

        elif option == 4:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % "bad", "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], "good", NP2[0], RC2 % "bad", "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 6:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % "good", "and", D3[0], "bad", NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 7:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % "good", "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], "bad", NP4[0]]))

        elif option == 8:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], RC3 % "bad", aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], "good", NP2[0], "and", D3[0], NP3[0], RC3 % "bad", aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 10:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], "good", NP3[0], RC3 % "bad", aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 11:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], RC3 % "good", aux2[0], V2[0], D4[0], "bad", NP4[0]]))

        elif option == 12:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % "bad"]))
        elif option == 13:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], "good", NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % "bad"]))
        elif option == 14:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], "good", NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % "bad"]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], "good", NP4[0], RC4 % "bad"]))

        return data, track_sentence

    def sample_2_rcs(self):

        V1 = choice(self.all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_very_common_dets))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", all_very_common_dets))
        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])

        RC1, _ = self.subject_relative_clause(NP1)
        RC2, _ = self.subject_relative_clause(NP2)

        track_sentence = [
            (S1, RC1, RC2),
            (S1, RC1, RC2)
        ]

        data = []
        data.append(" ".join([D1[0], "good", NP1[0], RC1 % "", aux1[0], V1[0], D2[0], "bad", NP2[0], RC2 % ""]))
        option = random.randint(0, 4)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % "bad", aux1[0], V1[0], D2[0], NP2[0], RC2 % ""]))
        elif option == 1:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % "", aux1[0], V1[0], D2[0], NP2[0], RC2 % "bad"]))
        elif option == 2:
            data.append(" ".join([D1[0], NP1[0], RC1 % "good", aux1[0], V1[0], D2[0], "bad", NP2[0], RC2 % ""]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % "good", aux1[0], V1[0], D2[0], NP2[0], RC2 % "bad"]))
        else:
            data.append(" ".join([D1[0], NP1[0], RC1 % "", aux1[0], V1[0], D2[0], "good", NP2[0], RC2 % "bad"]))

        return data, track_sentence

    def sample_rc_over_multiple_DPs(self):

        V1 = choice(self.all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_very_common_dets))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", all_very_common_dets))

        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])

        def object_relative_clause_coord(obj):
            rel = choice(get_matched_by(obj, "arg_1", get_all("category_2", "rel")))
            V = choice(get_matched_by(obj, "arg_2", self.all_possibly_plural_transitive_verbs))
            subj1 = choice(get_matches_of(V, "arg_1", self.safe_nouns))
            subj2 = choice(list(filter(lambda x: x["animate"] == subj1["animate"]
                                                 and x["sg"] == subj1["sg"]
                                                 and x["agent"] == subj1["agent"]
                                                 and x["physical"] == subj1["physical"]
                                                 and x["artifact"] == subj1["artifact"],
                                                 get_matches_of(V, "arg_1", self.safe_nouns))))
            aux = return_aux(V, self.plural_noun)
            D1 = choice(get_matched_by(subj1, "arg_1", all_very_common_dets))
            D2 = choice(get_matched_by(subj2, "arg_1", all_very_common_dets))
            RC = " ".join([rel[0], D1[0], "%s", subj1[0], "and", D2[0], "%s", subj2[0], aux[0], V[0]])
            return RC

        RC1 = object_relative_clause_coord(NP1)
        RC2 = object_relative_clause_coord(NP2)

        track_sentence = [
            (S1, RC1, RC2),
            (S1, RC1, RC2)
        ]

        data = []

        option = random.randint(0, 2)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], "bad", NP2[0], RC2 % ("", "")]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("good", "bad"), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "")]))
        else:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("good", "bad")]))


        option = random.randint(0, 11)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("bad", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "")]))
        elif option == 1:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("", "bad"), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "")]))
        elif option == 2:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("bad", "")]))
        elif option == 3:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "bad")]))

        elif option == 4:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("good", ""), aux1[0], V1[0], D2[0], "bad", NP2[0], RC2 % ("", "")]))
        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("good", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("bad", "")]))
        elif option == 6:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("good", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "bad")]))

        elif option == 7:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", "good"), aux1[0], V1[0], D2[0], "bad", NP2[0], RC2 % ("", "")]))
        elif option == 8:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", "good"), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("bad", "")]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", "good"), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "bad")]))

        elif option == 10:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], "good", NP2[0], RC2 % ("bad", "")]))
        else:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], "good", NP2[0], RC2 % ("", "bad")]))

        return data, track_sentence

    def sample_nested_rc(self):

        V1 = choice(self.all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_very_common_dets))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", all_very_common_dets))
        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])

        RC1, obj_RC1 = self.object_relative_clause(NP1)
        RC2, obj_RC2 = self.object_relative_clause(NP2)
        RC1_b, obj_RC1_b = self.subject_relative_clause(obj_RC1)
        RC2_b, obj_RC2_b = self.subject_relative_clause(obj_RC2)

        track_sentence = [
            (S1, RC1, RC2),
            (S1, RC1, RC2)
        ]

        data = []
        option = random.randint(0, 1)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("", (RC1_b % "")), aux1[0], V1[0], D2[0], "bad", NP2[0]]))
        else:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], "bad", NP2[0], RC2 % ("", (RC2_b % ""))]))


        option = random.randint(0, 10)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("bad", (RC1_b % "")), aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("", (RC1_b % "bad")), aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % ("", (RC1_b % "")), aux1[0], V1[0], D2[0], "bad", NP2[0]]))

        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("good", (RC1_b % "bad")), aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 4:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("good", (RC1_b % "")), aux1[0], V1[0], D2[0], "bad", NP2[0]]))

        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", (RC1_b % "good")), aux1[0], V1[0], D2[0], "bad", NP2[0]]))

        elif option == 6:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % ("bad", (RC2_b % ""))]))
        elif option == 7:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", (RC2_b % "bad"))]))

        elif option == 8:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], "good", NP2[0], RC2 % ("bad", (RC2_b % ""))]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], "good", NP2[0], RC2 % ("", (RC2_b % "bad"))]))

        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % ("good", (RC2_b % "bad"))]))

        return data, track_sentence

    def sample_CP_verb_RC(self):

        V1 = choice(self.cp_verb)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_very_common_dets))
        V2 = choice(self.all_transitive_verbs)
        NP2 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        aux2 = return_aux(V2, NP2)
        D2 = choice(get_matched_by(NP2, "arg_1", all_very_common_dets))
        NP3 = choice(get_matches_of(V2, "arg_2", self.safe_nouns))
        D3 = choice(get_matched_by(NP3, "arg_1", all_very_common_dets))

        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], "that", D2[0], "%s", NP2[0], aux2[0], V2[0], D3[0], "%s", NP3[0]])

        RC1, _ = self.subject_relative_clause(NP1)
        RC2, _ = self.subject_relative_clause(NP2)
        RC3, _ = self.subject_relative_clause(NP3)

        track_sentence = [
            (S1, RC1, RC2),
            (S1, RC1, RC2)
        ]

        data = []

        option = random.randint(0, 2)
        if option == 0:
            data.append(" ".join([D1[0], NP1[0], RC1 % "", aux1[0], V1[0], "that", D2[0], "good", NP2[0], aux2[0], V2[0], D3[0], "bad", NP3[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], "good", NP2[0], RC2 % "", aux2[0], V2[0], D3[0], "bad", NP3[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], "good", NP2[0], aux2[0], V2[0], D3[0], "bad", NP3[0], RC3 % ""]))


        option = random.randint(0, 14)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % "bad", aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % "", aux1[0], V1[0], "that", D2[0], "bad", NP2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], "good", NP1[0], RC1 % "", aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], "bad", NP3[0]]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % "good", aux1[0], V1[0], "that", D2[0], "bad", NP2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 4:
            data.append(" ".join([D1[0], NP1[0], RC1 % "good", aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], "bad", NP3[0]]))

        elif option == 5:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], "that", D2[0], "bad", NP2[0], RC2 % "", aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 6:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], RC2 % "bad", aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 7:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], RC2 % "", aux2[0], V2[0], D3[0], "bad", NP3[0]]))
        elif option == 8:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], "good", NP2[0], RC2 % "bad", aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], RC2 % "good", aux2[0], V2[0], D3[0], "bad", NP3[0]]))

        elif option == 10:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], "that", D2[0], "bad", NP2[0], aux2[0], V2[0], D3[0], NP3[0], RC3 % ""]))
        elif option == 11:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], "bad", NP3[0], RC3 % ""]))
        elif option == 12:
            data.append(" ".join([D1[0], "good", NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0], RC3 % "bad"]))
        elif option == 13:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], "good", NP2[0], aux2[0], V2[0], D3[0], NP3[0], RC3 % "bad"]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], "good", NP3[0], RC3 % "bad"]))

        return data, track_sentence

    def sample_CP_noun(self):

        NP1 = choice(self.CP_nouns)
        V1 = choice(get_matched_by(NP1, "arg_1", self.all_transitive_verbs))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_very_common_dets))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", all_very_common_dets))
        # S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])



        V_emb = choice(self.all_transitive_verbs)
        NP1_emb = choice(get_matches_of(V_emb, "arg_1", self.safe_nouns))
        aux_emb = return_aux(V_emb, NP1_emb)
        D1_emb = choice(get_matched_by(NP1_emb, "arg_1", all_very_common_dets))
        NP2_emb = choice(get_matches_of(V_emb, "arg_2", self.safe_nouns))
        D2_emb = choice(get_matched_by(NP2_emb, "arg_1", all_very_common_dets))

        S1 = " ".join([D1[0], NP1[0], NP1_emb[0], V_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]])
        track_sentence = [
            (S1),
            (S1)
        ]

        data = []
        option = random.randint(0, 1)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], "that", D1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], "bad", NP2[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], "good", NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], "bad", NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]]))


        option = random.randint(0, 4)
        if option == 0:
            data.append(" ".join([D1[0], "good", NP1[0], "that", D1_emb[0], "bad", NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], "good", NP1[0], "that", D1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], "bad", NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], "good", NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], "bad", NP2[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], "good", NP2_emb[0], aux1[0], V1[0], D2[0], "bad", NP2[0]]))
        return data, track_sentence



generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
