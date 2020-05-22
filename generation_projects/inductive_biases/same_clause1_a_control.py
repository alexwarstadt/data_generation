from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
import generation_projects.inductive_biases.person_helper

class MyGenerator(generation_projects.inductive_biases.person_helper.PersonGenerator):
    def __init__(self):
        super().__init__(uid="same_clause_control",
                         linguistic_feature_type="syntactic",
                         linguistic_feature_description="Are the two adjectives ?",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)
        self.safe_nouns = np.array(list(filter(lambda x: "public" not in x["expression"] 
                                                      and "Great" not in x["expression"] 
                                                      and "high" not in x["expression"], all_common_nouns)))
        self.locales = get_all("locale", "1", self.safe_nouns)
        self.safe_adjectives = np.array(list(filter(lambda x: "out in the open" != x["expression"], all_adjectives)))
        self.physical_nouns = get_all("physical", "1", self.safe_nouns)
        self.CP_verbs = get_all("category", "(S\\NP)/S", all_verbs)
        self.CP_nouns = get_all("category", "N/S", all_nominals)
        self.all_possibly_plural_transitive_verbs = np.intersect1d(all_transitive_verbs, all_possibly_plural_verbs)
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
        option = random.randint(0, 2)
        if option == 0:
            data_out, track_sentence_out = self.sample_coordination()
        elif option == 1:
            data_out, track_sentence_out = self.sample_coordination_over_rc()
        else:
            data_out, track_sentence_out = self.sample_CP_verb_RC()
        track_sentence.extend(track_sentence_out)

        option = random.randint(0, 3)
        if option == 0:
            data_in, track_sentence_in = self.sample_2_rcs()
        elif option == 1:
            data_in, track_sentence_in = self.sample_rc_over_multiple_DPs()
        elif option == 2:
            data_in, track_sentence_in = self.sample_nested_rc()
        else:
            data_in, track_sentence_in = self.sample_CP_noun()
        track_sentence.extend(track_sentence_in)

        data = self.build_paradigm(
            training_1_1=data_in[0],
            training_0_0=data_in[1],
            test_1_0=data_out[0],
            test_0_1=data_out[1]
        )

        return data, track_sentence



    def subject_relative_clause(self, subj):
        rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        V = choice(get_matched_by(subj, "arg_1", all_transitive_verbs))
        aux1 = return_aux(V, subj)
        obj = choice(get_matches_of(V, "arg_2", self.safe_nouns))
        A = choice(get_matched_by(obj, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(obj, "arg_1", all_frequent_determiners))

        RC = " ".join([rel[0], aux1[0], V[0], D2[0], "%s", obj[0]])
        return RC, A, obj

    def object_relative_clause(self, obj):
        rel = choice(get_matched_by(obj, "arg_1", get_all("category_2", "rel")))
        V = choice(get_matched_by(obj, "arg_2", all_transitive_verbs))
        subj = choice(get_matches_of(V, "arg_1", self.safe_nouns))
        aux1 = return_aux(V, subj)
        A = choice(get_matched_by(subj, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(subj, "arg_1", all_frequent_determiners))
        RC = " ".join([rel[0], D2[0], "%s", subj[0], "%s", aux1[0], V[0]])
        return RC, A, subj

    def sample_coordination(self):

        V1 = choice(all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        A1 = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_frequent_determiners))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        A2 = choice(get_matched_by(NP2, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(NP2, "arg_1", all_frequent_determiners))
        S1 = " ".join([D1[0], "%s", NP1[0], aux1[0], V1[0], D2[0], "%s", NP2[0]])

        V2 = choice(all_transitive_verbs)
        NP3 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        A3 = choice(get_matched_by(NP3, "arg_1", self.safe_adjectives))
        aux2 = return_aux(V2, NP3)
        D3 = choice(get_matched_by(NP3, "arg_1", all_frequent_determiners))
        NP4 = choice(get_matches_of(V2, "arg_2", self.safe_nouns))
        A4 = choice(get_matched_by(NP4, "arg_1", self.safe_adjectives))
        D4 = choice(get_matched_by(NP4, "arg_1", all_frequent_determiners))
        S2 = " ".join([D3[0], "%s", NP3[0], aux2[0], V2[0], D4[0], "%s", NP4[0]])


        track_sentence = [
            (S1, S2, A1[0], A2[0]),
            (S1, S2, A3[0], A4[0]),
            ]

        data = []
        if bool(random.randint(0, 1)):
            data.append((S1 + " and " + S2) % (A1[0], A2[0], "", ""))
        else:
            data.append((S1 + " and " + S2) % ("", "", A3[0], A4[0]))

        option = random.randint(0, 3)
        if option == 0:
            data.append((S1 + " and " + S2) % (A1[0], "", A3[0], ""))
        elif option == 1:
            data.append((S1 + " and " + S2) % (A1[0], "", "", A4[0]))
        elif option == 2:
            data.append((S1 + " and " + S2) % ("", A2[0], A3[0], ""))
        else:
            data.append((S1 + " and " + S2) % ("", "", A3[0], A4[0]))

        return data, track_sentence

    def sample_coordination_over_rc(self):

        V1 = choice(all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        A1 = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_frequent_determiners))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        A2 = choice(get_matched_by(NP2, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(NP2, "arg_1", all_frequent_determiners))
        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])

        V2 = choice(all_transitive_verbs)
        NP3 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        A3 = choice(get_matched_by(NP3, "arg_1", self.safe_adjectives))
        aux2 = return_aux(V2, NP3)
        D3 = choice(get_matched_by(NP3, "arg_1", all_frequent_determiners))
        NP4 = choice(get_matches_of(V2, "arg_2", self.safe_nouns))
        A4 = choice(get_matched_by(NP4, "arg_1", self.safe_adjectives))
        D4 = choice(get_matched_by(NP4, "arg_1", all_frequent_determiners))
        S2 = " ".join([D3[0], "%s", NP3[0], "%s", aux2[0], V2[0], D4[0], "%s", NP4[0], "%s"])

        # def subject_relative_clause(subj):
        #     rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        #     V = choice(get_matched_by(subj, "arg_1", all_transitive_verbs))
        #     aux1 = return_aux(V, subj)
        #     obj = choice(get_matches_of(V, "arg_2", all_common_nouns))
        #     A = choice(get_matched_by(obj, "arg_1", self.safe_adjectives))
        #     D2 = choice(get_matched_by(obj, "arg_1", all_frequent_determiners))
        #     RC = " ".join([rel[0], aux1[0], V[0], D2[0], "%s", obj[0]])
        #     return RC, A

        RC1, A_RC1, _ = self.subject_relative_clause(NP1)
        RC2, A_RC2, _ = self.subject_relative_clause(NP2)
        RC3, A_RC3, _ = self.subject_relative_clause(NP3)
        RC4, A_RC4, _ = self.subject_relative_clause(NP4)


        track_sentence = [
            (S1, S2, A1[0], A2[0]),
            (S1, S2, A1[0], A4[0]),
            ]

        data = []
        option = random.randint(0, 7)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % "", aux1[0], V1[0], D2[0], A2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], RC1 % "", aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], A3[0], NP3[0], aux2[0], V2[0], D4[0], A4[0], NP4[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % "", "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % "", "and", D3[0], A3[0], NP3[0], aux2[0], V2[0], D4[0], A4[0], NP4[0]]))
        elif option == 4:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], "and", D3[0], NP3[0], RC3 % "", aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], A3[0], NP3[0], RC3 % "", aux2[0], V2[0], D4[0], A4[0], NP4[0]]))
        elif option == 6:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % ""]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], A3[0], NP3[0], aux2[0], V2[0], D4[0], A4[0], NP4[0], RC4 % ""]))


        option = random.randint(0, 1)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], A3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], A4[0], NP4[0]]))

        elif option == 4:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % A_RC2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % A_RC2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 6:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % A_RC2[0], "and", D3[0], A3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 7:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % A_RC2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], A4[0], NP4[0]]))

        elif option == 8:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], RC3 % A_RC3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], "and", D3[0], NP3[0], RC3 % A_RC3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 10:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], A3[0], NP3[0], RC3 % A_RC3[0], aux2[0], V2[0], D4[0], NP4[0]]))
        elif option == 11:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], RC3 % A_RC3[0], aux2[0], V2[0], D4[0], A4[0], NP4[0]]))

        elif option == 12:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % A_RC4[0]]))
        elif option == 13:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % A_RC4[0]]))
        elif option == 14:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], A3[0], NP3[0], aux2[0], V2[0], D4[0], NP4[0], RC4 % A_RC4[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], "and", D3[0], NP3[0], aux2[0], V2[0], D4[0], A4[0], NP4[0], RC4 % A_RC4[0]]))

        return data, track_sentence

    def sample_2_rcs(self):

        V1 = choice(all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        A1 = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_frequent_determiners))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        A2 = choice(get_matched_by(NP2, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(NP2, "arg_1", all_frequent_determiners))
        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])

        RC1, A_RC1, _ = self.subject_relative_clause(NP1)
        RC2, A_RC2, _ = self.subject_relative_clause(NP2)

        track_sentence = [
            (S1, A1[0], A2[0], RC1, RC2, A_RC1[0], A_RC2[0]),
            (S1, A1[0], A2[0], RC1, RC2, A_RC1[0], A_RC2[0])
        ]

        data = []
        data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % "", aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ""]))
        option = random.randint(0, 4)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % ""]))
        elif option == 1:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % "", aux1[0], V1[0], D2[0], NP2[0], RC2 % A_RC2[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ""]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % A_RC2[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], RC1 % "", aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % A_RC2[0]]))

        return data, track_sentence

    def sample_rc_over_multiple_DPs(self):

        V1 = choice(all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        A1 = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_frequent_determiners))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        A2 = choice(get_matched_by(NP2, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(NP2, "arg_1", all_frequent_determiners))


        # NP2_b = choice(get_matches_of(V1, "arg_2", all_common_nouns))
        # A2_b = choice(get_matched_by(NP2_b, "arg_1", self.safe_adjectives))
        # D2_b= choice(get_matched_by(NP2_b, "arg_1", all_frequent_determiners))

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
            A1 = choice(get_matched_by(subj1, "arg_1", self.safe_adjectives))
            D1 = choice(get_matched_by(subj1, "arg_1", all_frequent_determiners))
            A2 = choice(get_matched_by(subj2, "arg_1", self.safe_adjectives))
            D2 = choice(get_matched_by(subj2, "arg_1", all_frequent_determiners))
            RC = " ".join([rel[0], D1[0], "%s", subj1[0], "and", D2[0], "%s", subj2[0], aux[0], V[0]])
            return RC, A1, A2

        RC1, A_RC1_a, A_RC1_b = object_relative_clause_coord(NP1)
        RC2, A_RC2_a, A_RC2_b = object_relative_clause_coord(NP2)

        track_sentence = [
            (S1, A1[0], A2[0], RC1, RC2, A_RC1_a[0], A_RC2_a[0], A_RC1_b[0], A_RC2_b[0]),
            (S1, A1[0], A2[0], RC1, RC2, A_RC1_a[0], A_RC2_a[0], A_RC1_b[0], A_RC2_b[0])
        ]

        data = []

        option = random.randint(0, 2)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ("", "")]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], RC1 % (A_RC1_a[0], A_RC1_b[0]), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "")]))
        else:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % (A_RC2_a[0], A_RC2_b[0])]))


        option = random.randint(0, 11)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % (A_RC1_a[0], ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "")]))
        elif option == 1:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % ("", A_RC1_b[0]), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", "")]))
        elif option == 2:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % (A_RC2_a[0], "")]))
        elif option == 3:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", A_RC2_b[0])]))

        elif option == 4:
            data.append(" ".join([D1[0], NP1[0], RC1 % (A_RC1_a[0], ""), aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ("", "")]))
        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], RC1 % (A_RC1_a[0], ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % (A_RC2_a[0], "")]))
        elif option == 6:
            data.append(" ".join([D1[0], NP1[0], RC1 % (A_RC1_a[0], ""), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", A_RC2_b[0])]))

        elif option == 7:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", A_RC1_b[0]), aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ("", "")]))
        elif option == 8:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", A_RC1_b[0]), aux1[0], V1[0], D2[0], NP2[0], RC2 % (A_RC2_a[0], "")]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", A_RC1_b[0]), aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", A_RC2_b[0])]))

        elif option == 10:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % (A_RC2_a[0], "")]))
        else:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", ""), aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ("", A_RC2_b[0])]))

        return data, track_sentence

    def sample_nested_rc(self):

        V1 = choice(all_transitive_verbs)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        A1 = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_frequent_determiners))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        A2 = choice(get_matched_by(NP2, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(NP2, "arg_1", all_frequent_determiners))
        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])

        RC1, A_RC1, obj_RC1 = self.object_relative_clause(NP1)
        RC2, A_RC2, obj_RC2 = self.object_relative_clause(NP2)
        RC1_b, A_RC1_b, obj_RC1_b = self.subject_relative_clause(obj_RC1)
        RC2_b, A_RC2_b, obj_RC2_b = self.subject_relative_clause(obj_RC2)

        track_sentence = [
            (S1, A1[0], A2[0], RC1, RC2, A_RC1[0], A_RC2[0]),
            (S1, A1[0], A2[0], RC1, RC2, A_RC1[0], A_RC2[0])
        ]

        data = []
        option = random.randint(0, 1)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % ("", (RC1_b % "")), aux1[0], V1[0], D2[0], A2[0], NP2[0]]))
        else:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ("", (RC2_b % ""))]))


        option = random.randint(0, 10)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % (A_RC1[0], (RC1_b % "")), aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % ("", (RC1_b % A_RC1_b[0])), aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % ("", (RC1_b % "")), aux1[0], V1[0], D2[0], A2[0], NP2[0]]))

        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % (A_RC1[0], (RC1_b % A_RC1_b[0])), aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 4:
            data.append(" ".join([D1[0], NP1[0], RC1 % (A_RC1[0], (RC1_b % "")), aux1[0], V1[0], D2[0], A2[0], NP2[0]]))

        elif option == 5:
            data.append(" ".join([D1[0], NP1[0], RC1 % ("", (RC1_b % A_RC1_b[0])), aux1[0], V1[0], D2[0], A2[0], NP2[0]]))

        elif option == 6:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % (A_RC2[0], (RC2_b % ""))]))
        elif option == 7:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % ("", (RC2_b % A_RC2_b[0]))]))

        elif option == 8:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % (A_RC2[0], (RC2_b % ""))]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], A2[0], NP2[0], RC2 % ("", (RC2_b % A_RC2_b[0]))]))

        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], D2[0], NP2[0], RC2 % (A_RC2[0], (RC2_b % A_RC2_b[0]))]))

        return data, track_sentence

    def sample_CP_verb_RC(self):

        V1 = choice(self.cp_verb)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        A1 = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_frequent_determiners))
        V2 = choice(all_transitive_verbs)
        NP2 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        aux2 = return_aux(V2, NP2)
        A2 = choice(get_matched_by(NP2, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(NP2, "arg_1", all_frequent_determiners))
        NP3 = choice(get_matches_of(V2, "arg_2", self.safe_nouns))
        A3 = choice(get_matched_by(NP3, "arg_1", self.safe_adjectives))
        D3 = choice(get_matched_by(NP3, "arg_1", all_frequent_determiners))

        S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], "that", D2[0], "%s", NP2[0], aux2[0], V2[0], D3[0], "%s", NP3[0]])

        RC1, A_RC1, _ = self.subject_relative_clause(NP1)
        RC2, A_RC2, _ = self.subject_relative_clause(NP2)
        RC3, A_RC3, _ = self.subject_relative_clause(NP3)

        track_sentence = [
            (S1, A1[0], A2[0], RC1, RC2, A_RC1[0], A_RC2[0], A_RC3[0]),
            (S1, A1[0], A2[0], RC1, RC2, A_RC1[0], A_RC2[0], A_RC3[0])
        ]

        data = []

        option = random.randint(0, 2)
        if option == 0:
            data.append(" ".join([D1[0], NP1[0], RC1 % "", aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], aux2[0], V2[0], D3[0], A3[0], NP3[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], RC2 % "", aux2[0], V2[0], D3[0], A3[0], NP3[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], aux2[0], V2[0], D3[0], A3[0], NP3[0], RC3 % ""]))


        option = random.randint(0, 14)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % "", aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], A1[0], NP1[0], RC1 % "", aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], A3[0], NP3[0]]))
        elif option == 3:
            data.append(" ".join([D1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 4:
            data.append(" ".join([D1[0], NP1[0], RC1 % A_RC1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], A3[0], NP3[0]]))

        elif option == 5:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], RC2 % "", aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 6:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], RC2 % A_RC2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 7:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], RC2 % "", aux2[0], V2[0], D3[0], A3[0], NP3[0]]))
        elif option == 8:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], RC2 % A_RC2[0], aux2[0], V2[0], D3[0], NP3[0]]))
        elif option == 9:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], RC2 % A_RC2[0], aux2[0], V2[0], D3[0], A3[0], NP3[0]]))

        elif option == 10:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0], RC3 % ""]))
        elif option == 11:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], A3[0], NP3[0], RC3 % ""]))
        elif option == 12:
            data.append(" ".join([D1[0], A1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0], RC3 % A_RC3[0]]))
        elif option == 13:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], A2[0], NP2[0], aux2[0], V2[0], D3[0], NP3[0], RC3 % A_RC3[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], aux1[0], V1[0], "that", D2[0], NP2[0], aux2[0], V2[0], D3[0], A3[0], NP3[0], RC3 % A_RC3[0]]))

        return data, track_sentence

    def sample_CP_noun(self):

        NP1 = choice(self.CP_nouns)
        V1 = choice(get_matched_by(NP1, "arg_1", all_transitive_verbs))
        A1 = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux1 = return_aux(V1, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", all_frequent_determiners))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        A2 = choice(get_matched_by(NP2, "arg_1", self.safe_adjectives))
        D2 = choice(get_matched_by(NP2, "arg_1", all_frequent_determiners))
        # S1 = " ".join([D1[0], "%s", NP1[0], "%s", aux1[0], V1[0], D2[0], "%s", NP2[0], "%s"])



        V_emb = choice(all_transitive_verbs)
        NP1_emb = choice(get_matches_of(V_emb, "arg_1", self.safe_nouns))
        A1_emb = choice(get_matched_by(NP1, "arg_1", self.safe_adjectives))
        aux_emb = return_aux(V_emb, NP1_emb)
        D1_emb = choice(get_matched_by(NP1_emb, "arg_1", all_frequent_determiners))
        NP2_emb = choice(get_matches_of(V_emb, "arg_2", self.safe_nouns))
        A2_emb = choice(get_matched_by(NP2_emb, "arg_1", self.safe_adjectives))
        D2_emb = choice(get_matched_by(NP2_emb, "arg_1", all_frequent_determiners))

        S1 = " ".join([D1[0], NP1[0], NP1_emb[0], V_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]])
        track_sentence = [
            (S1, A1[0], A2[0], A1_emb[0], A2_emb[0]),
            (S1, A1[0], A2[0], A1_emb[0], A2_emb[0])
        ]

        data = []
        option = random.randint(0, 1)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], A2[0], NP2[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], A1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], A2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]]))


        option = random.randint(0, 4)
        if option == 0:
            data.append(" ".join([D1[0], A1[0], NP1[0], "that", D1_emb[0], A1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 1:
            data.append(" ".join([D1[0], A1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], A2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], NP2[0]]))
        elif option == 2:
            data.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], A1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], A2[0], NP2[0]]))
        else:
            data.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], aux_emb[0], V_emb[0], D2_emb[0], A2_emb[0], NP2_emb[0], aux1[0], V1[0], D2[0], A2[0], NP2[0]]))
        return data, track_sentence



generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
