from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets_dynamic import *
import random

class MyGenerator(data_generator.StructureDependenceGenerator):
    def __init__(self):
        super().__init__(uid="main_verb",
                         linguistic_feature_description="Is the main verb in the progressive form?",
                         surface_feature_description="Is the first verb in the progressive form?")

        self.safe_nouns = np.intersect1d(get_all_frequent(), get_all_common_nouns())
        self.CP_nouns = get_all("category", "N/S", get_all_nominals())
        self.all_ing_verbs = get_all("ing", "1", get_all_verbs())
        all_possibly_ing_verbs = np.unique(np.array([item for sublist in [get_all("root", x["root"], get_all_verbs()) for x in self.all_ing_verbs] for item in sublist]))
        all_non_ing_verbs = np.setdiff1d(all_possibly_ing_verbs, self.all_ing_verbs)
        self.all_ing_transitive_verbs = np.intersect1d(self.all_ing_verbs, get_all_transitive_verbs())
        self.all_non_ing_transitive_verbs = np.intersect1d(all_non_ing_verbs, get_all_transitive_verbs())
        self.all_ing_intransitive_verbs = np.intersect1d(self.all_ing_verbs, get_all_intransitive_verbs())
        self.all_non_ing_intransitive_verbs = np.intersect1d(all_non_ing_verbs, get_all_intransitive_verbs())
        CP_verbs = get_all("category", "(S\\NP)/S")
        self.CP_verbs_ing = np.intersect1d(CP_verbs, self.all_ing_verbs)
        self.CP_verbs_non_ing = np.intersect1d(CP_verbs, all_non_ing_verbs)
        clause_embedding_verbs = np.union1d(CP_verbs, get_all_rogatives())
        self.all_non_CP_ing_verbs = np.setdiff1d(self.all_ing_verbs, clause_embedding_verbs)
        self.all_non_CP_non_ing_verbs = np.setdiff1d(all_non_ing_verbs, clause_embedding_verbs)


        # self.all_possibly_plural_transitive_verbs = np.intersect1d(self.all_transitive_verbs, all_possibly_plural_verbs)
        # self.plural_noun = choice(all_plural_nouns)



    def sample(self):

        track_sentence = []
        option = random.randint(0, 4)
        if option == 0:
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_nested_rc(ambiguous=True)
        elif option == 1:
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_verb_RC(ambiguous=True)
        elif option == 2:
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_1_RC(ambiguous=True)
        elif option == 3:
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_nested_CP_verb(ambiguous=True)
        else:
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_under_RC(ambiguous=True)
        track_sentence.extend(track_sentence_in)

        option = random.randint(0, 3)
        if option == 0:
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_2_RCs(ambiguous=False)
        elif option == 1:
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_noun(ambiguous=False)
        elif option == 2:
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_noun_RC(ambiguous=False)
        else:
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_nested_RC_2_RCs(ambiguous=False)
        track_sentence.extend(track_sentence_out)

        data_transform = self.build_paradigm(
            training_1_1=data_transform_in[0],
            training_0_0=data_transform_in[1],
            test_1_0=data_transform_out[0],
            test_0_1=data_transform_out[1],
            training_1_1_base=data_base_in[0],
            training_0_0_base=data_base_in[1],
            test_1_0_base=data_base_out[0],
            test_0_1_base=data_base_out[1],
            template_1_1=templates_in[0],
            template_0_0=templates_in[1],
            template_1_0=templates_out[0],
            template_0_1=templates_out[1]
        )

        return data_transform, track_sentence

    def get_ing_form(self, verb):
        return list(filter(lambda x: x["root"] == verb["root"], self.all_ing_verbs))[0]

    def subject_relative_clause(self, subj, bind=False):
        rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        V = choice(get_matched_by(subj, "arg_1", self.all_non_ing_transitive_verbs))
        V = conjugate(V, subj)
        V_ing = self.get_ing_form(V)
        V_ing = conjugate(V_ing, subj)
        obj = choice(get_matches_of(V, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(obj, "arg_1", get_all_very_common_dets()))
        if bind:
            RC = " ".join([rel[0], "{v}", D2[0], obj[0], "{rc}"])
        else:
            RC = " ".join([rel[0], "%s", D2[0], obj[0]])
        return RC, obj, V[0], V_ing[0]

    def subject_relative_clause_intransitive(self, subj):
        rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        try:
            V = choice(get_matched_by(subj, "arg_1", self.all_non_ing_intransitive_verbs))
        except IndexError:
            raise MatchNotFoundError("")
        V_ing = self.get_ing_form(V)
        V = conjugate(V, subj)
        V_ing = conjugate(V_ing, subj)
        RC = " ".join([rel[0], "%s"])
        return RC, V[0], V_ing[0]

    def object_relative_clause(self, obj, bind=False):
        rel = choice(get_matched_by(obj, "arg_1", get_all("category_2", "rel")))
        if bool(random.randint(0, 1)):
            rel[0] = ""
        V = choice(get_matched_by(obj, "arg_2", self.all_non_ing_transitive_verbs))
        V_ing = self.get_ing_form(V)
        subj = choice(get_matches_of(V, "arg_1", self.safe_nouns))
        V = conjugate(V, subj)
        V_ing = conjugate(V_ing, subj)
        D2 = choice(get_matched_by(subj, "arg_1", get_all_very_common_dets()))
        if bind:
            RC = " ".join([rel[0], D2[0], subj[0], "{rc}", "{v}"])
        else:
            RC = " ".join([rel[0], D2[0], subj[0], "%s"])
        return RC, subj, V[0], V_ing[0]

    def sample_2_RCs(self, ambiguous):

        if ambiguous:
            raise Exception("This paradigm can't be ambiguous")
        template = "2_RCs"
        V1 = choice(self.all_non_ing_transitive_verbs)
        V1_ing = self.get_ing_form(V1)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        V1 = conjugate(V1, NP1)
        try:
            V1_ing = conjugate(V1_ing, NP1)
        except Exception:
            pass
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
        S1 = " ".join([D1[0], NP1[0], "%s", D2[0], NP2[0]])

        option = random.randint(0, 1)
        template += ",RC1=%d" % option
        if option == 0:
            RC1, _, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1)
        else:
            RC1, _, V_RC1, V_RC1_ing = self.object_relative_clause(NP1)

        option = random.randint(0, 1)
        template += ",RC2=%d" % option
        if option == 0:
            RC2, _, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2)
        else:
            RC2, _, V_RC2, V_RC2_ing = self.object_relative_clause(NP2)

        track_sentence = [
            (S1, RC1, RC2, V_RC1, V_RC2),
            (S1, RC1, RC2, V_RC1, V_RC2),
        ]
        
        data_transform = []
        data_base = []
        templates = []
        # 1_0
        data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1_ing[0], D2[0], NP2[0], RC2 % V_RC2]))
        data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], D2[0], NP2[0], RC2 % V_RC2]))
        templates.append(template + ",1_0")

        # 0_1
        data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1_ing, V1[0], D2[0], NP2[0], RC2 % V_RC2]))
        data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], D2[0], NP2[0], RC2 % V_RC2]))
        templates.append(template + ",0_1")

        return data_transform, data_base, track_sentence, templates


    def sample_nested_rc(self, ambiguous):

        template = "nested_rc"
        V1 = choice(self.all_non_ing_transitive_verbs)
        V1_ing = self.get_ing_form(V1)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        V1 = conjugate(V1, NP1)
        V1_ing = conjugate(V1_ing, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
        S1 = " ".join([D1[0], NP1[0], "%s", D2[0], NP2[0]])

        option = random.randint(0, 2)
        template += ",RC1=%d" % option
        if option == 0:
            RC1, arg_RC1, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1, bind=True)
            RC1_b, _, V_RC1_b, V_RC1_ing_b = self.subject_relative_clause(arg_RC1, bind=False)
        elif option == 1:
            RC1, arg_RC1, V_RC1, V_RC1_ing = self.object_relative_clause(NP1, bind=True)
            RC1_b, _, V_RC1_b, V_RC1_ing_b = self.subject_relative_clause(arg_RC1, bind=False)
        else:
            RC1, arg_RC1, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1, bind=True)
            RC1_b, _, V_RC1_b, V_RC1_ing_b = self.object_relative_clause(arg_RC1, bind=False)


        option = random.randint(0, 2)
        template += ",RC2=%d" % option
        if option == 0:
            RC2, arg_RC2, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2, bind=True)
            RC2_b, _, V_RC2_b, V_RC2_ing_b = self.subject_relative_clause(arg_RC2, bind=False)
        elif option == 1:
            RC2, arg_RC2, V_RC2, V_RC2_ing = self.object_relative_clause(NP2, bind=True)
            RC2_b, _, V_RC2_b, V_RC2_ing_b = self.subject_relative_clause(arg_RC2, bind=False)
        else:
            RC2, arg_RC2, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2, bind=True)
            RC2_b, _, V_RC2_b, V_RC2_ing_b = self.object_relative_clause(arg_RC2, bind=False)

        track_sentence = [
            (S1, RC1, RC2),
            (S1, RC1, RC2)
        ]

        data_transform = []
        data_base = []
        templates = []
        if ambiguous:
            # 1_1
            data_transform.append(" ".join([D1[0], NP1[0], V1_ing[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
            data_base.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
            templates.append(template + ",1_1")

            # 0_0
            option = random.randint(0, 1)
            templates.append(template + ",0_0,option=%d" % option)
            if option == 0:
                data_transform.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2.format(v=V_RC2_ing, rc=(RC2_b % V_RC2_b))]))
                data_base.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
            else:
                data_transform.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_ing_b))]))
                data_base.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))

                # NOTE: This template can't be used because there is no 1_1 version of it.
                # data_transform.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_ing_b)), V1[0], D2[0], NP2[0]]))
                # data_base.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0]]))

        else:  # unambiguous
            # 1_0
            data_transform.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1_ing[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0]]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1_ing, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0]]))
            templates.append(template + ",0_1")

        return data_transform, data_base, track_sentence, templates


    def sample_CP_verb_RC(self, ambiguous):

        template = "CP_verb_RC"
        V1 = choice(self.CP_verbs_non_ing)
        V1_ing = self.get_ing_form(V1)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        V1 = conjugate(V1, NP1)
        V1_ing = conjugate(V1_ing, NP1)

        V2 = choice(self.all_non_ing_transitive_verbs)
        V2_ing = self.get_ing_form(V2)
        NP2 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        V2 = conjugate(V2, NP2)
        V2_ing = conjugate(V2_ing, NP2)
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
        NP3 = choice(get_matches_of(V2, "arg_2", self.safe_nouns))
        D3 = choice(get_matched_by(NP3, "arg_1", get_all_very_common_dets()))


        option = random.randint(0, 1)
        template += ",RC1=%d" % option
        if option == 0:
            RC1, _, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1)
        else:
            RC1, _, V_RC1, V_RC1_ing = self.object_relative_clause(NP1)

        option = random.randint(0, 1)
        template += ",RC2=%d" % option
        if option == 0:
            RC2, _, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2)
        else:
            RC2, _, V_RC2, V_RC2_ing = self.object_relative_clause(NP2)

        option = random.randint(0, 1)
        template += ",RC3=%d" % option
        if option == 0:
            RC3, _, V_RC3, V_RC3_ing = self.subject_relative_clause(NP3)
        else:
            RC3, _, V_RC3, V_RC3_ing = self.object_relative_clause(NP3)

        S1 = " ".join([D1[0], "%s", NP1[0], "%s", V1[0], "that", D2[0], "%s", NP2[0], V2[0], D3[0], "%s", NP3[0]])

        track_sentence = [
            (S1, RC1, RC2, RC3),
            (S1, RC1, RC2, RC3)
        ]

        data_transform = []
        data_base = []
        templates = []

        if ambiguous:
            # 1_1
            optionA = random.randint(0, 1)
            templates.append(template + ",1_1,optionA=%d" % optionA)
            optionB = random.randint(0, 1)
            templates.append(template + ",0_0,optionA=%d,optionB=%d" % (optionA, optionB))
            if optionA == 0:
                data_transform.append(" ".join([D1[0], NP1[0], V1_ing[0], "that", D2[0], NP2[0], RC2 % V_RC2, V2[0], D3[0], NP3[0]]))
                data_base.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], RC2 % V_RC2, V2[0], D3[0], NP3[0]]))
                # 0_0
                if optionB == 0:
                    data_transform.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], RC2 % V_RC2_ing, V2[0], D3[0], NP3[0]]))
                    data_base.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], RC2 % V_RC2, V2[0], D3[0], NP3[0]]))
                else:
                    data_transform.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], RC2 % V_RC2, V2_ing[0], D3[0], NP3[0]]))
                    data_base.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], RC2 % V_RC2, V2[0], D3[0], NP3[0]]))
            else:
                # 1_1
                data_transform.append(" ".join([D1[0], NP1[0], V1_ing[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0], RC3 % V_RC3]))
                data_base.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0], RC3 % V_RC3]))
                # 0_0
                if optionB == 0:
                    data_transform.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0], RC3 % V_RC3_ing]))
                    data_base.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0], RC3 % V_RC3]))
                else:
                    data_transform.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], V2_ing[0], D3[0], NP3[0], RC3 % V_RC3]))
                    data_base.append(" ".join([D1[0], NP1[0], V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0], RC3 % V_RC3]))

                # Note: This 0_0 template can't be used because it doesn't have a 1_1 pair
                # data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], "that", D2[0], NP2[0], V2_ing[0], D3[0], NP3[0]]))
                # data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0]]))

        else:  # unambiguous
            # 1_0
            data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1_ing[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0]]))
            data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0]]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1_ing, V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0]]))
            data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], "that", D2[0], NP2[0], V2[0], D3[0], NP3[0]]))
            templates.append(template + ",0_1")

        return data_transform, data_base, track_sentence, templates


    def sample_CP_noun(self, ambiguous):
        if ambiguous:
            raise Exception("This paradigm can't be ambiguous")

        template = "CP_noun"
        NP1 = choice(self.CP_nouns)
        V1 = choice(get_matched_by(NP1, "arg_1", self.all_non_ing_transitive_verbs))
        V1_ing = self.get_ing_form(V1)
        V1 = conjugate(V1, NP1)
        V1_ing = conjugate(V1_ing, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))

        V_emb = choice(self.all_non_ing_transitive_verbs)
        V_emb_ing = self.get_ing_form(V_emb)
        NP1_emb = choice(get_matches_of(V_emb, "arg_1", self.safe_nouns))
        V_emb = conjugate(V_emb, NP1_emb)
        V_emb_ing = conjugate(V_emb_ing, NP1_emb)
        D1_emb = choice(get_matched_by(NP1_emb, "arg_1", get_all_very_common_dets()))
        NP2_emb = choice(get_matches_of(V_emb, "arg_2", self.safe_nouns))
        D2_emb = choice(get_matched_by(NP2_emb, "arg_1", get_all_very_common_dets()))

        S1 = " ".join([D1[0], NP1[0], NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]])
        track_sentence = [S1, S1]

        data_transform = []
        data_base = []
        templates = []

        # 1_0
        data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], V1_ing[0], D2[0], NP2[0]]))
        data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]]))
        templates.append(template + ",1_0")

        # 0_1
        data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb_ing[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]]))
        data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]]))
        templates.append(template + ",0_1")

        return data_transform, data_base, track_sentence, templates


    def sample_CP_noun_RC(self, ambiguous):
        if ambiguous:
            raise Exception("This paradigm can't be ambiguous")

        template = "CP_noun_RC"
        NP1 = choice(self.CP_nouns)
        V1 = choice(get_matched_by(NP1, "arg_1", self.all_non_ing_transitive_verbs))
        V1_ing = self.get_ing_form(V1)
        V1 = conjugate(V1, NP1)
        V1_ing = conjugate(V1_ing, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))

        V_emb = choice(self.all_non_ing_transitive_verbs)
        V_emb_ing = self.get_ing_form(V_emb)
        NP1_emb = choice(get_matches_of(V_emb, "arg_1", self.safe_nouns))
        V_emb = conjugate(V_emb, NP1_emb)
        V_emb_ing = conjugate(V_emb_ing, NP1_emb)
        D1_emb = choice(get_matched_by(NP1_emb, "arg_1", get_all_very_common_dets()))
        NP2_emb = choice(get_matches_of(V_emb, "arg_2", self.safe_nouns))
        D2_emb = choice(get_matched_by(NP2_emb, "arg_1", get_all_very_common_dets()))

        RC2, V_RC2, V_RC2_ing = self.subject_relative_clause_intransitive(NP2)
        RC1_emb, V_RC1_emb, V_RC1_emb_ing = self.subject_relative_clause_intransitive(NP1_emb)
        RC2_emb, V_RC2_emb, V_RC2_emb_ing = self.subject_relative_clause_intransitive(NP2_emb)

        S1 = " ".join([D1[0], NP1[0], NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]])
        track_sentence = [
            (S1),
            (S1)
        ]

        data_transform = []
        data_base = []
        templates = []
        option = random.randint(0, 2)
        templates.append(template + ",1_0,option=%d" % option)
        templates.append(template + ",0_1,option=%d" % option)

        if option == 0:  # RC1_emb, 1_0
            data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], RC1_emb % V_RC1_emb, V_emb[0], D2_emb[0], NP2_emb[0], V1_ing[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], RC1_emb % V_RC1_emb, V_emb[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]]))
            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], RC1_emb % V_RC1_emb_ing, V_emb[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], RC1_emb % V_RC1_emb, V_emb[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0]]))

        elif option == 1:  # RC_2_emb, 1_0
            data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], RC2_emb % V_RC2_emb, V1_ing[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], RC2_emb % V_RC2_emb, V1[0], D2[0], NP2[0]]))
            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb_ing[0], D2_emb[0], NP2_emb[0], RC2_emb % V_RC2_emb, V1[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], RC2_emb % V_RC2_emb, V1[0], D2[0], NP2[0]]))

        else: # RC_2, 1_0
            data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], V1_ing[0], D2[0], NP2[0], RC2 % V_RC2]))
            data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0], RC2 % V_RC2]))
            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb_ing[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0], RC2 % V_RC2]))
            data_base.append(" ".join([D1[0], NP1[0], "that", D1_emb[0], NP1_emb[0], V_emb[0], D2_emb[0], NP2_emb[0], V1[0], D2[0], NP2[0], RC2 % V_RC2]))

        return data_transform, data_base, track_sentence, templates


    def sample_nested_RC_2_RCs(self, ambiguous):
        if ambiguous:
            raise Exception("This paradigm can't be ambiguous")

        template = "nested_RC_2_RCs"
        V1 = choice(self.all_non_ing_transitive_verbs)
        V1_ing = self.get_ing_form(V1)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        V1 = conjugate(V1, NP1)
        V1_ing = conjugate(V1_ing, NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
        S1 = " ".join([D1[0], NP1[0], "%s", D2[0], NP2[0]])

        option = random.randint(0, 2)
        template += ",RC1=%d" % option
        if option == 0:
            RC1, arg_RC1, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1, bind=True)
            RC1_b, _, V_RC1_b, V_RC1_ing_b = self.subject_relative_clause(arg_RC1, bind=False)
        elif option == 1:
            RC1, arg_RC1, V_RC1, V_RC1_ing = self.object_relative_clause(NP1, bind=True)
            RC1_b, _, V_RC1_b, V_RC1_ing_b = self.subject_relative_clause(arg_RC1, bind=False)
        else:
            RC1, arg_RC1, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1, bind=True)
            RC1_b, _, V_RC1_b, V_RC1_ing_b = self.object_relative_clause(arg_RC1, bind=False)


        option = random.randint(0, 2)
        template += ",RC2=%d" % option
        if option == 0:
            RC2, arg_RC2, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2, bind=True)
            RC2_b, _, V_RC2_b, V_RC2_ing_b = self.subject_relative_clause(arg_RC2, bind=False)
        elif option == 1:
            RC2, arg_RC2, V_RC2, V_RC2_ing = self.object_relative_clause(NP2, bind=True)
            RC2_b, _, V_RC2_b, V_RC2_ing_b = self.subject_relative_clause(arg_RC2, bind=False)
        else:
            RC2, arg_RC2, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2, bind=True)
            RC2_b, _, V_RC2_b, V_RC2_ing_b = self.object_relative_clause(arg_RC2, bind=False)


        RC1_iv, V_RC1_iv, V_RC1_iv_ing = self.subject_relative_clause_intransitive(NP1)
        RC2_iv, V_RC2_iv, V_RC2_iv_ing = self.subject_relative_clause_intransitive(NP2)

        track_sentence = [
            (S1, RC1, RC2),
            (S1, RC1, RC2)
        ]

        data_transform = []
        data_base = []
        templates = []
        option = random.randint(0, 1)
        templates.append(template + ",1_0,option=%d" % option)
        templates.append(template + ",0_1,option=%d" % option)
        if option == 0:  # RC_1_b, 1_0
            data_transform.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1_ing[0], D2[0], NP2[0], RC2_iv % V_RC2_iv]))
            data_base.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0], RC2_iv % V_RC2_iv]))
            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1_ing, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0], RC2_iv % V_RC2_iv]))
            data_base.append(" ".join([D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0], RC2_iv % V_RC2_iv]))
        else:  # RC_2_b, 1_0
            data_transform.append(" ".join([D1[0], NP1[0], RC1_iv % V_RC1_iv, V1_ing[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
            data_base.append(" ".join([D1[0], NP1[0], RC1_iv % V_RC1_iv, V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], RC1_iv % V_RC1_iv_ing, V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
            data_base.append(" ".join([D1[0], NP1[0], RC1_iv % V_RC1_iv, V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))

        return data_transform, data_base, track_sentence, templates


    def sample_1_RC(self, ambiguous):
        template = "1_RC"
        V1 = choice(self.all_non_ing_transitive_verbs)
        V1_ing = self.get_ing_form(V1)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        V1 = conjugate(V1, NP1)
        try:
            V1_ing = conjugate(V1_ing, NP1)
        except Exception:
            pass
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
        S1 = " ".join([D1[0], NP1[0], "%s", D2[0], NP2[0]])

        option = random.randint(0, 1)
        template += ",RC1=%d" % option
        if option == 0:
            RC1, _, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1)
        else:
            RC1, _, V_RC1, V_RC1_ing = self.object_relative_clause(NP1)

        option = random.randint(0, 1)
        template += ",RC2=%d" % option
        if option == 0:
            RC2, _, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2)
        else:
            RC2, _, V_RC2, V_RC2_ing = self.object_relative_clause(NP2)

        track_sentence = [
            (S1, RC1, RC2, V_RC1, V_RC2),
            (S1, RC1, RC2, V_RC1, V_RC2),
        ]

        data_transform = []
        data_base = []
        templates = []
        if ambiguous:
            # 1_1
            data_transform.append(" ".join([D1[0], NP1[0], V1_ing[0], D2[0], NP2[0], RC2 % V_RC2]))
            data_base.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2 % V_RC2]))
            templates.append(template + ",1_1")

            # 0_0
            data_transform.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2 % V_RC2_ing]))
            data_base.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2 % V_RC2]))
            templates.append(template + ",0_0")

        else:  # unambiguous
            # 1_0
            data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1_ing[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], D2[0], NP2[0]]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1_ing, V1[0], D2[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], D2[0], NP2[0]]))
            templates.append(template + ",0_1")

        return data_transform, data_base, track_sentence, templates

    def sample_nested_CP_verb(self, ambiguous):
        if not ambiguous:
            raise Exception("This paradigm must be ambiguous")
        template = "nested_CP_verb"
        V1 = choice(self.CP_verbs_non_ing)
        V1_ing = self.get_ing_form(V1)
        NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        V1 = conjugate(V1, NP1)
        V1_ing = conjugate(V1_ing, NP1)

        V2 = choice(self.CP_verbs_non_ing, avoid=V1)
        V2_ing = self.get_ing_form(V2)
        NP2 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
        V2 = conjugate(V2, NP2)
        V2_ing = conjugate(V2_ing, NP2)

        V3 = choice(self.all_non_CP_non_ing_verbs)
        V3_ing = self.get_ing_form(V3)
        V3_args = verb_args_from_verb(V3)
        that1 = "that" if random.choice([True, False]) else ""
        that2 = "that" if random.choice([True, False]) else ""
        S3 = make_sentence_from_args(V3_args)
        V3_args["aux"] = return_aux(V3_ing, V3_args["subj"])
        V3_args["verb"] = V3_ing
        S3_ing = make_sentence_from_args(V3_args)

        track_sentence = [
            (V1, NP1, V2, NP2, V3),
            (V1, NP1, V2, NP2, V3)
        ]

        data_transform = []
        data_base = []
        templates = []

        # 1_1
        data_transform.append(" ".join([D1[0], NP1[0], V1_ing[0], that1, D2[0], NP2[0], V2[0], that2, S3]))
        data_base.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3]))
        templates.append(template + ",1_1")

        # 0_0
        option = random.randint(0, 1)
        templates.append(template + ",0_0,option=%d" % option)
        if option == 0:
            data_transform.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2_ing[0], that2, S3]))
            data_base.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3]))
        else:
            data_transform.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3_ing]))
            data_base.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3]))

        return data_transform, data_base, track_sentence, templates


    def sample_CP_under_RC(self, ambiguous):
        template = "CP_under_RC"
        V_CP = choice(self.CP_verbs_non_ing)
        V_CP_ing = self.get_ing_form(V_CP)

        NP1 = choice(get_matches_of(V_CP, "arg_1", self.safe_nouns))
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        Rel = choice(get_matched_by(NP1, "arg_1", get_all_relativizers()))[0]
        V_CP = conjugate(V_CP, NP1)
        V_CP_ing = conjugate(V_CP_ing, NP1)
        V_emb = choice(self.all_non_ing_transitive_verbs)
        V_emb_ing = self.get_ing_form(V_emb)
        NP2 = choice(get_matches_of(V_emb, "arg_1", self.safe_nouns))
        D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
        NP3 = choice(get_matches_of(V_emb, "arg_2", self.safe_nouns))
        D3 = choice(get_matched_by(NP3, "arg_1", get_all_very_common_dets()))
        V_emb = conjugate(V_emb, NP2)
        V_emb_ing = conjugate(V_emb_ing, NP2)

        try:
            option = random.randint(0, 2)
            if option == 0:  # bind subject of V_CP
                that = "that"
                NP_RC = " ".join([D1[0], NP1[0], Rel, "{V_CP}", that, D2[0], NP2[0], "{V_emb}", D3[0], NP3[0]])
            elif option == 1:  # bind subject of CP
                Rel = Rel if random.choice([True, False]) else ""
                that = ""
                NP_RC = " ".join([D2[0], NP2[0], Rel, D1[0], NP1[0], "{V_CP}", that, "{V_emb}", D3[0], NP3[0]])
            else:  # bind object of CP
                Rel = Rel if random.choice([True, False]) else ""
                that = "that"
                NP_RC = " ".join([D3[0], NP3[0], Rel, D1[0], NP1[0], "{V_CP}", that, D2[0], NP2[0], "{V_emb}"])
        except Exception:
            pass

        if ambiguous:
            V_main = choice(get_matched_by(NP1, "arg_2", self.all_non_ing_transitive_verbs))
            V_main_ing = self.get_ing_form(V_main)
            NP4 = choice(get_matches_of(V_main, "arg_1", self.safe_nouns))
            D4 = choice(get_matched_by(NP4, "arg_1", get_all_very_common_dets()))
            V_main = conjugate(V_main, NP4)
            V_main_ing = conjugate(V_main_ing, NP4)

            data_transform = []
            data_base = []
            templates = []

            # 1_1
            data_transform.append(" ".join([D4[0], NP4[0], V_main_ing[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))
            data_base.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))
            templates.append(template + ",1_1")

            # 0_0
            option = random.randint(0, 1)
            templates.append(template + ",0_0,option=%d" % option)
            if option == 0:
                data_transform.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP_ing[0], V_emb=V_emb[0])]))
                data_base.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))
            else:
                data_transform.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb_ing[0])]))
                data_base.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))

        else:  # unambiguous
            V_main = choice(get_matched_by(NP1, "arg_1", self.all_non_CP_non_ing_verbs))
            V_main_ing = self.get_ing_form(V_main)
            V_main_args = verb_args_from_verb(verb=V_main, subj=NP1)
            V_main = conjugate(V_main, NP1)
            V_main_ing = conjugate(V_main_ing, NP1)

            data_transform = []
            data_base = []
            templates = []

            # 1_0
            data_transform.append(" ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main_ing[0], join_args(V_main_args["args"])]))
            data_base.append(" ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([NP_RC.format(V_CP=V_CP_ing[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))
            data_base.append(" ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))
            templates.append(template + ",0_1")

            # Note: The template can't be used because it cannot form a fully ambiguous or unambiguous minimal pair
            # data_transform.append(" ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb_ing[0]), V_main[0], join_args(V_main_args["args"])]))
            # data_base.append(" ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))

        track_sentence = [
            (V_CP, NP1, V_emb, NP2, NP3, V_main),
            (V_CP, NP1, V_emb, NP2, NP3, V_main)
        ]

        return data_transform, data_base, track_sentence, templates




generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/structure/" + generator.uid)