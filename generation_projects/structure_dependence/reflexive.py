from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets_dynamic import *
import random


class MyGenerator(data_generator.StructureDependenceGenerator):
    def __init__(self):
        super().__init__(uid="reflexive",
                         linguistic_feature_description="Is the reflexive bound by a valid antecedent?",
                         surface_feature_description="Is the reflexive bound by its most recent predecessor?")

        self.safe_nouns = np.intersect1d(get_all_frequent(), get_all_common_nouns())
        self.CP_nouns = get_all("category", "N/S", get_all_nominals())
        CP_verbs = get_all("category", "(S\\NP)/S")
        self.all_CP_verbs = np.union1d(CP_verbs, get_all_rogatives())
        self.all_himself = get_all_conjunctive([("gender", "m"), ("sg", "1")], self.safe_nouns)
        self.all_herself = get_all_conjunctive([("gender", "f"), ("sg", "1")], self.safe_nouns)
        self.all_itself = get_all_conjunctive([("animate", "0"), ("sg", "1")], self.safe_nouns)
        self.all_themselves = np.intersect1d(get_all_plural_nouns(), self.safe_nouns)
        self.all_agreeing_nouns = np.union1d(self.all_himself, np.union1d(self.all_herself, np.union1d(self.all_itself, self.all_themselves)))
        self.all_not_himself = np.setdiff1d(self.safe_nouns, self.all_himself)
        self.all_not_herself = np.setdiff1d(self.safe_nouns, self.all_herself)
        self.all_not_itself = np.setdiff1d(self.safe_nouns, self.all_itself)
        self.all_not_themselves = np.setdiff1d(self.safe_nouns, self.all_themselves)
        # self.all_possibly_plural_transitive_verbs = np.intersect1d(self.all_transitive_verbs, all_possibly_plural_verbs)
        # self.plural_noun = choice(all_plural_nouns)

    def sample(self):

        data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_verb_RC(ambiguous=True)
        data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_verb_RC(ambiguous=False)

        track_sentence = []
        # option = random.randint(0, 4)
        # if option == 0:
        #     data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_nested_rc(ambiguous=True)
        # elif option == 1:
        #     data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_verb_RC(ambiguous=True)
        # elif option == 2:
        #     data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_1_RC(ambiguous=True)
        # elif option == 3:
        #     data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_nested_CP_verb(
        #         ambiguous=True)
        # else:
        #     data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_under_RC(ambiguous=True)
        track_sentence.extend(track_sentence_in)

        # option = random.randint(0, 3)
        # if option == 0:
        #     data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_2_RCs(ambiguous=False)
        # elif option == 1:
        #     data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_noun(ambiguous=False)
        # elif option == 2:
        #     data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_noun_RC(
        #         ambiguous=False)
        # else:
        #     data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_nested_RC_2_RCs(
        #         ambiguous=False)
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

    def return_reflexive(self, noun):
        if noun in self.all_himself:
            return "himself"
        if noun in self.all_herself:
            return "herself"
        if noun in self.all_itself:
            return "itself"
        if noun in self.all_themselves:
            return "themselves"

    def get_non_agreeing_nouns(self, noun):
        if noun in self.all_himself:
            return self.all_not_himself
        if noun in self.all_herself:
            return self.all_not_herself
        if noun in self.all_itself:
            return self.all_not_itself
        if noun in self.all_themselves:
            return self.all_not_themselves

    def subject_relative_clause(self, subj, reflexive=False, binder=False, coindexes=[], other_verbs=[], nested=False):
        """
        :param subj: The subject of the RC
        :param reflexive: Does the RC verb have to be reflexive?
        :param binder: Is the generated object a binder of a reflexive?
        :param coindexes: List of other nouns that will get put in the place of the generated object.
        :param other_verbs: List of other verbs + argument slots where the generated object will appear.
        :param nested: Is there a nested relative clause?
        :return:
        """
        rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        V_sample_space = get_all_refl_preds() if reflexive else get_all_transitive_verbs()
        for NP in coindexes:
            V_sample_space = get_matched_by(NP, "arg_2", V_sample_space)
        V = choice(get_matched_by(subj, "arg_1", V_sample_space))
        V = conjugate(V, subj)
        obj_sample_space = self.all_agreeing_nouns if binder else self.safe_nouns
        for verb in other_verbs:
            obj_sample_space = get_matches_of(verb[0], verb[1], obj_sample_space)
        obj = choice(obj_sample_space)
        obj_refl = self.return_reflexive(obj)
        obj = N_to_DP_mutate(obj, very_common_det=True)
        if nested:
            RC = " ".join([rel[0], V[0], "{n}", "{rc}"])
        else:
            try:
                RC = " ".join([rel[0], V[0], "{n}"])
            except Exception:
                pass
        return RC, obj, obj_refl, V

    def subject_relative_clause_intransitive(self, subj):
        rel = choice(get_matched_by(subj, "arg_1", get_all("category_2", "rel")))
        try:
            V = choice(get_matched_by(subj, "arg_1", get_all_intransitive_verbs()))
        except IndexError:
            raise MatchNotFoundError("")
        V = conjugate(V, subj)
        RC = " ".join([rel[0], V[0]])
        return RC

    def object_relative_clause(self, obj, reflexive=False, binder=False, coindexes=[], other_verbs=[], nested=False):
        """
        :param obj: The object of the RC
        :param reflexive: Does the RC verb have to be reflexive?
        :param binder: Is the generated object a binder of a reflexive?
        :param coindexes: List of other nouns that will get put in the place of the generated subject.
        :param other_verbs: List of other verbs + argument slots where the generated subject will appear.
        :param nested: Is there a nested relative clause?
        :return:
        """
        rel = choice(get_matched_by(obj, "arg_1", get_all("category_2", "rel")))
        if bool(random.randint(0, 1)):
            rel[0] = ""
        V_sample_space = get_all_refl_preds() if reflexive else get_all_transitive_verbs()
        for NP in coindexes:
            V_sample_space = get_matched_by(NP, "arg_1", V_sample_space)
        V = choice(get_matched_by(obj, "arg_2", V_sample_space))
        subj_sample_space = self.all_agreeing_nouns if binder else self.safe_nouns
        for verb in other_verbs:
            subj_sample_space = get_matches_of(verb[0], verb[1], subj_sample_space)
        subj = choice(subj_sample_space)
        subj_refl = self.return_reflexive(subj)
        subj = N_to_DP_mutate(subj, very_common_det=True)
        try:
            V = conjugate(V, subj)
        except Exception:
            pass
        if nested:
            RC = " ".join([rel[0], "{n}", "{rc}", V[0]])
        else:
            RC = " ".join([rel[0], "{n}", V[0]])
        return RC, subj, subj_refl, V

    def sample_2_RCs(self, ambiguous):

        if not ambiguous:
            raise Exception("This paradigm must be ambiguous")

        template = "2_RCs"

        V1_refl = False
        V_RC1_refl = False
        V_RC2_refl = False
        optionA = random.randint(0, 1)
        if optionA == 0:    # 0 binds 1
            coindex_good = (0, 1)
            V_RC1_refl = True
        else:
            coindex_good = (2, 3)
            V_RC2_refl = True

        optionB = random.randint(0, 1)
        if optionB == 0:
            coindex_bad = (0, 3)
            V_RC2_refl = True
        else:
            coindex_bad = (1, 3)
            V_RC2_refl = True

        if V1_refl:
            V1 = choice(get_all_refl_preds())
        else:
            V1 = choice(get_all_transitive_verbs())

        if 0 in coindex_bad or 0 in coindex_good:
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns))
        else:
            NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
        V1 = conjugate(V1, NP1)
        NP1_refl = self.return_reflexive(NP1)
        NP1 = N_to_DP_mutate(NP1, very_common_det=True)

        if 2 in coindex_bad or 2 in coindex_good:
            NP2 = choice(get_matches_of(V1, "arg_2", self.all_agreeing_nouns))
        else:
            NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
        NP2_refl = self.return_reflexive(NP2)
        NP2 = N_to_DP_mutate(NP2, very_common_det=True)


        S1 = " ".join([NP1[0], "%s", NP2[0]])

        option = random.randint(0, 1)
        template += ",RC1=%d" % option
        binder1 = 1==coindex_good[0] or 1==coindex_bad[0]
        bound1 = 1==coindex_good[1] or 1==coindex_bad[1]
        coindexes1 = [NP1] if coindex_good == (0,1) else []
        if option == 0 or bound1:
            RC1, NP_RC1, NP_RC1_refl, V_RC1 = self.subject_relative_clause(NP1, reflexive=V_RC1_refl, binder=binder1, coindexes=coindexes1, other_verbs=[])
        else:
            RC1, NP_RC1, NP_RC1_refl, V_RC1 = self.object_relative_clause(NP1, reflexive=V_RC1_refl, binder=binder1, coindexes=coindexes1, other_verbs=[])

        option = random.randint(0, 1)
        template += ",RC2=%d" % option
        binder3 = 3==coindex_good[0] or 3==coindex_bad[0]
        bound3 = 3==coindex_good[1] or 3==coindex_bad[1]
        coindexes3 = []
        if (2,3) in coindex_good:
            coindexes3.append(NP2)
        if (0,3) in coindex_bad:
            coindexes3.append(NP1)
        if (1,3) in coindex_bad:
            coindexes3.append(NP_RC1)
        if option == 0 or bound3:
            RC2, NP_RC2, NP_RC2_refl, _ = self.subject_relative_clause(NP2, reflexive=V_RC2_refl, binder=binder3, coindexes=coindexes3, other_verbs=[])
        else:
            RC2, NP_RC2, NP_RC2_refl, _ = self.object_relative_clause(NP2, reflexive=V_RC2_refl, binder=binder3, coindexes=coindexes3, other_verbs=[])

        track_sentence = [
            (S1, RC1, RC2, NP_RC1, NP_RC2),
            (S1, RC1, RC2, NP_RC1, NP_RC2),
        ]

        data_transform = []
        data_base = []
        templates = []
        # 1_1
        if optionA == 0:  # (0, 1)
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP1_refl), V1[0], NP2[0], RC2.format(n=NP_RC2[0])]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP1[0]), V1[0], NP2[0], RC2.format(n=NP_RC2[0])]))
        else:  # (2, 3)
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP2_refl)]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP2[0])]))
        templates.append(template + ",1_1,optionA=" + str(optionA))

        # 0_0
        if optionB == 0:  # (0, 3)
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP1_refl)]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP1[0])]))
        else:  # (1, 3)
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP_RC1_refl)]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP_RC1[0])]))
        templates.append(template + ",0_0,optionB=" + str(optionB))

        return data_transform, data_base, track_sentence, templates

    def sample_nested_rc(self, ambiguous):
        track_sentence = []  # TODO
        data_transform = []
        data_base = []
        templates = []
        template = "nested_rc"
        if ambiguous:
            # optionA = random.randint(0, 1)
            optionA = 0     # TODO implement more of these if time
            if optionA == 0:  # 1 binds 2: The girl that helped the boy who hurt himself ate the pie.
                optionB = random.randint(0, 1)
                if optionB == 0:
                    coindex_bad = (0, 2)
                else:
                    coindex_bad = (1, 3)
                if 3 in coindex_bad:
                    V1 = choice(get_all_refl_preds())
                else:
                    V1 = choice(get_all_transitive_verbs())
                if 0 in coindex_bad:
                    NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns))
                else:
                    NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
                V1 = conjugate(V1, NP1)
                NP1_refl = self.return_reflexive(NP1)
                NP1 = N_to_DP_mutate(NP1, very_common_det=True)
                NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
                NP2_refl = self.return_reflexive(NP2)
                NP2 = N_to_DP_mutate(NP2, very_common_det=True)
                option = random.randint(0, 1)
                template += ",RC1=%d" % option
                binder1 = coindex_bad[0] == 1
                coindexes_RCb = [NP1] if coindex_bad == (0, 2) else []
                other_verbs_RC = [(V1, "arg_2")] if coindex_bad == (1, 3) else []
                if option == 0:
                    RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, reflexive=False, binder=binder1, coindexes=[], other_verbs=other_verbs_RC, nested=True)
                else:
                    RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, reflexive=False, binder=binder1, coindexes=[], other_verbs=other_verbs_RC, nested=True)
                RCb, NP_RCb, NP_RCb_refl, V_RCb = self.subject_relative_clause(NP_RC, reflexive=True, binder=False, coindexes=coindexes_RCb + [NP_RC], other_verbs=[])
                data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RC_refl)), V1[0], NP2[0]]))
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RC[0])), V1[0], NP2[0]]))
                templates.append(template + ",1_1,optionA=%d" % optionA)
                if optionB == 0:  # 0 binds 2
                    data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP1_refl)), V1[0], NP2[0]]))
                    data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP1[0])), V1[0], NP2[0]]))
                else:  # 1 binds 3
                    data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP_RC_refl]))
                    data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP_RC[0]]))
                templates.append(template + ",0_0,optionB=%d" % optionB)

        else:  # 1 binds 4: The girl that ate the pie that shocked the boy hurt herself.
            coindex_bad = (2, 3)
            V1 = choice(get_all_refl_preds())
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns))
            V1 = conjugate(V1, NP1)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
            NP2 = N_to_DP_mutate(NP2, very_common_det=True)
            option = random.randint(0, 1)
            template += ",RC1=%d" % option
            if option == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, nested=True)
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, nested=True)
            RCb, NP_RCb, NP_RCb_refl, V_RCb = self.subject_relative_clause(NP_RC, binder=True, other_verbs=[V1])
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP1_refl]))
            data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP1[0]]))
            templates.append(template + ",1_0")

            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP_RCb_refl]))
            data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP_RCb[0]]))
            templates.append(template + ",0_1")

        return data_transform, data_base, track_sentence, templates

    def sample_CP_verb_RC(self, ambiguous):
        track_sentence = []  # TODO
        data_transform = []
        data_base = []
        templates = []
        # if not ambiguous:
        #     raise Exception("This paradigm must be ambiguous")
        template = "CP_verb_RC"

        optionA = 1 if not ambiguous else random.randint(0, 2)  # Relative clause attached to NP1, NP2, or NP3

        if optionA == 0:    # RC attached to NP1
            V1 = choice(self.all_CP_verbs)
            optionB = random.randint(0, 1)  # distractor is matrix subject (0) or RC argument (1)
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns)) if optionB == 1 else choice(get_matches_of(V1, "arg_1", self.safe_nouns))
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1)
            V1 = conjugate(V1, NP1)
            option = random.randint(0, 1)
            template += f",RC={option}"
            if option == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, binder=optionB)
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, binder=optionB)
            V2 = choice(get_matched_by(NP_RC, "arg_2", get_all_refl_preds())) if optionB else choice(get_matched_by(NP1, "arg_2", get_all_refl_preds()))
            NP2 = choice(get_matches_of(V2, "arg_1", get_matches_of(V2, "arg_2", self.all_agreeing_nouns)))
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)
            V2 = conjugate(V2, NP2)

            # 1_1
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP2_refl]))
            data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP2[0]]))
            templates.append(f"{template},1_1,optionA={optionA}")

            # 0_0
            if optionB:
                data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP1_refl]))
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP1[0]]))
            else:
                data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP_RC_refl]))
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP_RC[0]]))
            templates.append(f"{template},1_1,optionA={optionA},optionB={optionB}")

        elif optionA == 1:  # RC attached to NP2
            V1 = choice(self.all_CP_verbs)
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns)) if ambiguous == 1 else choice(get_matches_of(V1, "arg_1", get_all_nouns()))
            NP1 = N_to_DP_mutate(NP1)
            NP1_refl = self.return_reflexive(NP1)
            V1 = conjugate(V1, NP1)
            V2 = choice(get_all_transitive_verbs()) if ambiguous else choice(get_all_refl_preds())
            NP2 = choice(get_matches_of(V2, "arg_1", self.all_agreeing_nouns))
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)
            V2 = conjugate(V2, NP2)
            NP3 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_2", get_all_nouns())))
            if ambiguous:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2, reflexive=True, coindexes=[NP2, NP1])
                # 1_1
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP2_refl), V2[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP2[0]), V2[0], NP3[0]]))
                templates.append(f"{template},1_1,optionA={optionA}")

                # 0_0
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP1_refl), V2[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP1[0]), V2[0], NP3[0]]))
                templates.append(f"{template},0_0,optionA={optionA}")

            else:
                option = random.randint(0, 1)
                template += f",RC={option}"
                if option == 0:
                    RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2, binder=True, other_verbs=[(V2, "arg_2")])
                else:
                    RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP2, binder=True, other_verbs=[(V2, "arg_2")])
                # 1_0
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP2_refl]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP2[0]]))
                templates.append(f"{template},1_0")

                # 0_1
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP_RC_refl]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP_RC[0]]))
                templates.append(f"{template},0_1")

        else:   # RC attached to NP3
            optionB = random.randint(0, 1)  # distractor is matrix subject (0) or embedded subject argument (1)
            V1 = choice(self.all_CP_verbs)
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns)) if optionB == 1 else choice(get_matches_of(V1, "arg_1", self.safe_nouns))
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1)
            V1 = conjugate(V1, NP1)
            V2 = choice(get_all_transitive_verbs())
            NP2 = choice(get_matches_of(V2, "arg_1", self.all_agreeing_nouns)) if optionB == 0 else choice(get_matches_of(V1, "arg_1", self.safe_nouns))
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)
            V2 = conjugate(V2, NP2)
            NP3 = choice(get_matches_of(V2, "arg_2", self.all_agreeing_nouns))
            NP3_refl = self.return_reflexive(NP3)
            NP3 = N_to_DP_mutate(NP3)
            RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, reflexive=True, coindexes=[NP3])

            # 1_1
            data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP3_refl)]))
            data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP_RC[0])]))
            templates.append(f"{template},1_1,optionA={optionA}")

            # 0_0
            if optionB:
                data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP1_refl]))
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP1[0]]))
            else:
                try:
                    data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP2_refl]))
                except Exception:
                    pass
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP2[0]]))
            templates.append(f"{template},1_1,optionA={optionA},optionB={optionB}")

        return data_transform, data_base, track_sentence, templates


    def sample_CP_noun(self, ambiguous):
        if not ambiguous:
            raise Exception("This paradigm must be ambiguous")

        template = "CP_noun"
        NP1 = N_to_DP_mutate(choice(self.CP_nouns), very_common_det=True)
        V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
        V1 = conjugate(V1, NP1)
        NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", self.safe_nouns)), very_common_det=True)

        V_emb = choice(get_all_refl_preds())
        NP1_emb = choice(get_matches_of(V_emb, "arg_1", get_matches_of(V1, "arg_2", self.all_agreeing_nouns)))
        NP1_emb_refl = get_reflexive(NP1_emb)
        NP1_emb = N_to_DP_mutate(NP1_emb, very_common_det=True)
        V_emb = conjugate(V_emb, NP1_emb)
        NP2_emb = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_2", self.safe_nouns)))
        data_transform = []
        data_base = []
        templates = []
        track_sentence = []

        # 1_1
        data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP1_emb_refl, V1[0], NP2[0]]))
        data_base.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP1_emb[0], V1[0], NP2[0]]))
        templates.append(template + ",1_1")

        # 0_1
        data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP1_emb_refl]))
        data_base.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP1_emb[0]]))
        templates.append(template + ",1_1")

        return data_transform, data_base, track_sentence, templates

    def sample_CP_noun_RC(self, ambiguous):
        """
        The idea that the girl who hurt the boy chased herself/the man is shocking the actor/himself    (disambig)
        The idea that the girl chased a boy that hurt himself/the woman is shocking the actor/himself     (ambig)
        The idea that the girl chased a boy is shocking the actor that hurt himself/herself     (ambig)
        """

        template = "CP_noun_RC"
        data_transform = []
        data_base = []
        templates = []
        track_sentence = []

        if not ambiguous:   # RC must attach to embedded subject
            # coindexes: (NP1_emb, NP2_emb), (NP2_emb, NP2)
            NP1 = N_to_DP_mutate(choice(self.CP_nouns), very_common_det=True)
            V1 = choice(get_matched_by(NP1, "arg_1", get_all_refl_preds()))
            V1 = conjugate(V1, NP1)
            V_emb = choice(get_all_refl_preds())
            NP1_emb = choice(get_matches_of(V_emb, "arg_1", self.all_agreeing_nouns))
            NP1_emb_refl = get_reflexive(NP1_emb)
            NP1_emb = N_to_DP_mutate(NP1_emb, very_common_det=True)
            NP2_emb = choice(get_matches_of(V_emb, "arg_2", get_matches_of(V1, "arg_2", self.all_agreeing_nouns)))
            NP2_emb_refl = get_reflexive(NP2_emb)
            NP2_emb = N_to_DP_mutate(NP2_emb, very_common_det=True)
            NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", self.safe_nouns)), very_common_det=True)
            option_RC = random.randint(0, 1)
            template += f",RC={option_RC}"
            if option_RC == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1_emb)
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1_emb)

            # 1_0
            data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), NP1_emb_refl, V1[0], NP2[0]]))
            data_base.append(" ".join([NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), NP1_emb[0], V1[0], NP2[0]]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), NP2_emb[0], V1[0], NP2_emb_refl]))
            data_base.append(" ".join([NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), NP2_emb[0], V1[0], NP2_emb[0]]))
            templates.append(template + ",0_1")


        else:
            optionA = random.randint(0, 1)  # 0 = RC on embedded obj; 1 = RC on matrix object
            if optionA == 0:    # RC on embedded obj
                # coindexes: (NP2_emb, NP_RC), (NP2_emb, NP2)

                NP1 = N_to_DP_mutate(choice(self.CP_nouns), very_common_det=True)
                V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
                V1 = conjugate(V1, NP1)
                V_emb = choice(get_all_transitive_verbs())
                NP1_emb = choice(get_matches_of(V_emb, "arg_1", self.safe_nouns))
                NP1_emb = N_to_DP_mutate(NP1_emb, very_common_det=True)
                NP2_emb = choice(get_matches_of(V_emb, "arg_2", get_matches_of(V1, "arg_2", self.all_agreeing_nouns)))
                NP2_emb_refl = get_reflexive(NP2_emb)
                NP2_emb = N_to_DP_mutate(NP2_emb, very_common_det=True)
                NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", self.safe_nouns)), very_common_det=True)
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1_emb, reflexive=True)

                # 1_1
                data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP2_emb_refl), V1[0], NP2[0]]))
                data_base.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP2_emb[0]), V1[0], NP2[0]]))
                templates.append(template + f"optionA={optionA},1_1")

                # 0_0
                data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP_RC[0]), V1[0], NP2_emb_refl]))
                data_base.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP_RC[0]), V1[0], NP2_emb[0]]))
                templates.append(template + f"optionA={optionA},0_0")

            else:    # RC on embedded obj
                # coindexes: (NP2, NP_RC), (NP1_emb, NP_RC)
                NP1 = N_to_DP_mutate(choice(self.CP_nouns), very_common_det=True)
                V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
                V1 = conjugate(V1, NP1)
                V_emb = choice(get_all_transitive_verbs())
                NP1_emb = choice(get_matches_of(V_emb, "arg_1", get_matches_of(V1, "arg_2", self.all_agreeing_nouns)))
                NP1_emb_refl = get_reflexive(NP1_emb)
                NP1_emb = N_to_DP_mutate(NP1_emb, very_common_det=True)
                NP2_emb = choice(get_matches_of(V_emb, "arg_2", self.safe_nouns))
                NP2_emb = N_to_DP_mutate(NP2_emb, very_common_det=True)
                NP2 = choice(get_matches_of(V1, "arg_2", self.all_agreeing_nouns))
                NP2_refl = get_reflexive(NP2)
                NP2 = N_to_DP_mutate(NP2)
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2, reflexive=True)

                # 1_1
                data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP2_refl)]))
                data_base.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP2[0])]))
                templates.append(template + f"optionA={optionA},1_1")

                # 0_0
                data_transform.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP1_emb_refl)]))
                data_base.append(" ".join([NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP1_emb[0])]))
                templates.append(template + f"optionA={optionA},0_0")

        return data_transform, data_base, track_sentence, templates


    # def sample_nested_RC_2_RCs(self, ambiguous):
    #     if ambiguous:
    #         raise Exception("This paradigm can't be ambiguous")

    #     template = "nested_RC_2_RCs"
    #     V1 = choice(self.all_non_ing_transitive_verbs)
    #     V1_ing = self.get_ing_form(V1)
    #     NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
    #     V1 = conjugate(V1, NP1)
    #     V1_ing = conjugate(V1_ing, NP1)
    #     D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
    #     NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
    #     D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
    #     S1 = " ".join([D1[0], NP1[0], "%s", D2[0], NP2[0]])
    #
    #     option = random.randint(0, 2)
    #     template += ",RC1=%d" % option
    #     if option == 0:
    #         RC1, arg_RC1, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1, bind=True)
    #         RC1_b, _, V_RC1_b, V_RC1_ing_b = self.subject_relative_clause(arg_RC1, bind=False)
    #     elif option == 1:
    #         RC1, arg_RC1, V_RC1, V_RC1_ing = self.object_relative_clause(NP1, bind=True)
    #         RC1_b, _, V_RC1_b, V_RC1_ing_b = self.subject_relative_clause(arg_RC1, bind=False)
    #     else:
    #         RC1, arg_RC1, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1, bind=True)
    #         RC1_b, _, V_RC1_b, V_RC1_ing_b = self.object_relative_clause(arg_RC1, bind=False)
    #
    #     option = random.randint(0, 2)
    #     template += ",RC2=%d" % option
    #     if option == 0:
    #         RC2, arg_RC2, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2, bind=True)
    #         RC2_b, _, V_RC2_b, V_RC2_ing_b = self.subject_relative_clause(arg_RC2, bind=False)
    #     elif option == 1:
    #         RC2, arg_RC2, V_RC2, V_RC2_ing = self.object_relative_clause(NP2, bind=True)
    #         RC2_b, _, V_RC2_b, V_RC2_ing_b = self.subject_relative_clause(arg_RC2, bind=False)
    #     else:
    #         RC2, arg_RC2, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2, bind=True)
    #         RC2_b, _, V_RC2_b, V_RC2_ing_b = self.object_relative_clause(arg_RC2, bind=False)
    #
    #     RC1_iv, V_RC1_iv, V_RC1_iv_ing = self.subject_relative_clause_intransitive(NP1)
    #     RC2_iv, V_RC2_iv, V_RC2_iv_ing = self.subject_relative_clause_intransitive(NP2)
    #
    #     track_sentence = [
    #         (S1, RC1, RC2),
    #         (S1, RC1, RC2)
    #     ]
    #
    #     data_transform = []
    #     data_base = []
    #     templates = []
    #     option = random.randint(0, 1)
    #     templates.append(template + ",1_0,option=%d" % option)
    #     templates.append(template + ",0_1,option=%d" % option)
    #     if option == 0:  # RC_1_b, 1_0
    #         data_transform.append(" ".join(
    #             [D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1_ing[0], D2[0], NP2[0],
    #              RC2_iv % V_RC2_iv]))
    #         data_base.append(" ".join(
    #             [D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0], RC2_iv % V_RC2_iv]))
    #         # 0_1
    #         data_transform.append(" ".join(
    #             [D1[0], NP1[0], RC1.format(v=V_RC1_ing, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0],
    #              RC2_iv % V_RC2_iv]))
    #         data_base.append(" ".join(
    #             [D1[0], NP1[0], RC1.format(v=V_RC1, rc=(RC1_b % V_RC1_b)), V1[0], D2[0], NP2[0], RC2_iv % V_RC2_iv]))
    #     else:  # RC_2_b, 1_0
    #         data_transform.append(" ".join([D1[0], NP1[0], RC1_iv % V_RC1_iv, V1_ing[0], D2[0], NP2[0],
    #                                         RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
    #         data_base.append(" ".join(
    #             [D1[0], NP1[0], RC1_iv % V_RC1_iv, V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
    #         # 0_1
    #         data_transform.append(" ".join([D1[0], NP1[0], RC1_iv % V_RC1_iv_ing, V1[0], D2[0], NP2[0],
    #                                         RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
    #         data_base.append(" ".join(
    #             [D1[0], NP1[0], RC1_iv % V_RC1_iv, V1[0], D2[0], NP2[0], RC2.format(v=V_RC2, rc=(RC2_b % V_RC2_b))]))
    #
    #     return data_transform, data_base, track_sentence, templates

    def sample_1_RC(self, ambiguous):
        template = "1_RC"
        data_base = []
        data_transform = []
        track_sentence = []
        templates = []
        if ambiguous:
            # The girl helped the boy that hurt himself/herself
            # RC on object
            # coindexes: (NP2, NP_RC), (NP1, NP_RC)
            V1 = choice(get_all_transitive_verbs())
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns))
            NP1_refl = get_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = conjugate(V1, NP1)
            NP2 = choice(get_matches_of(V1, "arg_2", self.all_agreeing_nouns))
            NP2_refl = get_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)
            RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2, reflexive=True, coindexes=[NP1])

            # 1_1
            data_transform.append(" ".join([NP1[0], V1[0], NP2[0], RC.format(n=NP2_refl)]))
            data_base.append(" ".join([NP1[0], V1[0], NP2[0], RC.format(n=NP2[0])]))
            templates.append(template + ",1_1")

            # 0_0
            data_transform.append(" ".join([NP1[0], V1[0], NP2[0], RC.format(n=NP1_refl)]))
            data_base.append(" ".join([NP1[0], V1[0], NP2[0], RC.format(n=NP1[0])]))
            templates.append(template + ",0_0")
        else:
            # The girl that helped the boy hurt herself/himself.
            # RC on subject
            # coindexes: (NP1, NP2), (NP_RC, NP2)
            V1 = choice(get_all_refl_preds())
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_agreeing_nouns))
            NP1_refl = get_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = conjugate(V1, NP1)
            NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
            NP2_refl = get_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)
            option_RC = random.randint(0, 1)
            template += f",RC={option_RC}"
            if option_RC == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, binder=True, other_verbs=[(V1, "arg_2")])
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, binder=True, other_verbs=[(V1, "arg_2")])

            # 1_0
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP1_refl]))
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP1[0]]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP_RC_refl]))
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP_RC[0]]))
            templates.append(template + ",0_1")
            
        return data_transform, data_base, track_sentence, templates

    #     V1 = choice(self.all_non_ing_transitive_verbs)
    #     V1_ing = self.get_ing_form(V1)
    #     NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
    #     V1 = conjugate(V1, NP1)
    #     try:
    #         V1_ing = conjugate(V1_ing, NP1)
    #     except Exception:
    #         pass
    #     D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
    #     NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns))
    #     D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
    #     S1 = " ".join([D1[0], NP1[0], "%s", D2[0], NP2[0]])
    #
    #     option = random.randint(0, 1)
    #     template += ",RC1=%d" % option
    #     if option == 0:
    #         RC1, _, V_RC1, V_RC1_ing = self.subject_relative_clause(NP1)
    #     else:
    #         RC1, _, V_RC1, V_RC1_ing = self.object_relative_clause(NP1)
    #
    #     option = random.randint(0, 1)
    #     template += ",RC2=%d" % option
    #     if option == 0:
    #         RC2, _, V_RC2, V_RC2_ing = self.subject_relative_clause(NP2)
    #     else:
    #         RC2, _, V_RC2, V_RC2_ing = self.object_relative_clause(NP2)
    #
    #     track_sentence = [
    #         (S1, RC1, RC2, V_RC1, V_RC2),
    #         (S1, RC1, RC2, V_RC1, V_RC2),
    #     ]
    #
    #     data_transform = []
    #     data_base = []
    #     templates = []
    #     if ambiguous:
    #         # 1_1
    #         data_transform.append(" ".join([D1[0], NP1[0], V1_ing[0], D2[0], NP2[0], RC2 % V_RC2]))
    #         data_base.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2 % V_RC2]))
    #         templates.append(template + ",1_1")
    #
    #         # 0_0
    #         data_transform.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2 % V_RC2_ing]))
    #         data_base.append(" ".join([D1[0], NP1[0], V1[0], D2[0], NP2[0], RC2 % V_RC2]))
    #         templates.append(template + ",0_0")
    #
    #     else:  # unambiguous
    #         # 1_0
    #         data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1_ing[0], D2[0], NP2[0]]))
    #         data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], D2[0], NP2[0]]))
    #         templates.append(template + ",1_0")
    #
    #         # 0_1
    #         data_transform.append(" ".join([D1[0], NP1[0], RC1 % V_RC1_ing, V1[0], D2[0], NP2[0]]))
    #         data_base.append(" ".join([D1[0], NP1[0], RC1 % V_RC1, V1[0], D2[0], NP2[0]]))
    #         templates.append(template + ",0_1")
    #
    #     return data_transform, data_base, track_sentence, templates
    #
    # def sample_nested_CP_verb(self, ambiguous):
    #     if not ambiguous:
    #         raise Exception("This paradigm must be ambiguous")
    #     template = "nested_CP_verb"
    #     V1 = choice(self.CP_verbs_non_ing)
    #     V1_ing = self.get_ing_form(V1)
    #     NP1 = choice(get_matches_of(V1, "arg_1", self.safe_nouns))
    #     D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
    #     V1 = conjugate(V1, NP1)
    #     V1_ing = conjugate(V1_ing, NP1)
    #
    #     V2 = choice(self.CP_verbs_non_ing, avoid=V1)
    #     V2_ing = self.get_ing_form(V2)
    #     NP2 = choice(get_matches_of(V2, "arg_1", self.safe_nouns))
    #     D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
    #     V2 = conjugate(V2, NP2)
    #     V2_ing = conjugate(V2_ing, NP2)
    #
    #     V3 = choice(self.all_non_CP_non_ing_verbs)
    #     V3_ing = self.get_ing_form(V3)
    #     V3_args = verb_args_from_verb(V3)
    #     that1 = "that" if random.choice([True, False]) else ""
    #     that2 = "that" if random.choice([True, False]) else ""
    #     S3 = make_sentence_from_args(V3_args)
    #     V3_args["aux"] = return_aux(V3_ing, V3_args["subj"])
    #     V3_args["verb"] = V3_ing
    #     S3_ing = make_sentence_from_args(V3_args)
    #
    #     track_sentence = [
    #         (V1, NP1, V2, NP2, V3),
    #         (V1, NP1, V2, NP2, V3)
    #     ]
    #
    #     data_transform = []
    #     data_base = []
    #     templates = []
    #
    #     # 1_1
    #     data_transform.append(" ".join([D1[0], NP1[0], V1_ing[0], that1, D2[0], NP2[0], V2[0], that2, S3]))
    #     data_base.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3]))
    #     templates.append(template + ",1_1")
    #
    #     # 0_0
    #     option = random.randint(0, 1)
    #     templates.append(template + ",0_0,option=%d" % option)
    #     if option == 0:
    #         data_transform.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2_ing[0], that2, S3]))
    #         data_base.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3]))
    #     else:
    #         data_transform.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3_ing]))
    #         data_base.append(" ".join([D1[0], NP1[0], V1[0], that1, D2[0], NP2[0], V2[0], that2, S3]))
    #
    #     return data_transform, data_base, track_sentence, templates
    #
    # def sample_CP_under_RC(self, ambiguous):
    #     template = "CP_under_RC"
    #     V_CP = choice(self.CP_verbs_non_ing)
    #     V_CP_ing = self.get_ing_form(V_CP)
    #
    #     NP1 = choice(get_matches_of(V_CP, "arg_1", self.safe_nouns))
    #     D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
    #     Rel = choice(get_matched_by(NP1, "arg_1", get_all_relativizers()))[0]
    #     V_CP = conjugate(V_CP, NP1)
    #     V_CP_ing = conjugate(V_CP_ing, NP1)
    #     V_emb = choice(self.all_non_ing_transitive_verbs)
    #     V_emb_ing = self.get_ing_form(V_emb)
    #     NP2 = choice(get_matches_of(V_emb, "arg_1", self.safe_nouns))
    #     D2 = choice(get_matched_by(NP2, "arg_1", get_all_very_common_dets()))
    #     NP3 = choice(get_matches_of(V_emb, "arg_2", self.safe_nouns))
    #     D3 = choice(get_matched_by(NP3, "arg_1", get_all_very_common_dets()))
    #     V_emb = conjugate(V_emb, NP2)
    #     V_emb_ing = conjugate(V_emb_ing, NP2)
    #
    #     try:
    #         option = random.randint(0, 2)
    #         if option == 0:  # bind subject of V_CP
    #             that = "that"
    #             NP_RC = " ".join([D1[0], NP1[0], Rel, "{V_CP}", that, D2[0], NP2[0], "{V_emb}", D3[0], NP3[0]])
    #         elif option == 1:  # bind subject of CP
    #             Rel = Rel if random.choice([True, False]) else ""
    #             that = ""
    #             NP_RC = " ".join([D2[0], NP2[0], Rel, D1[0], NP1[0], "{V_CP}", that, "{V_emb}", D3[0], NP3[0]])
    #         else:  # bind object of CP
    #             Rel = Rel if random.choice([True, False]) else ""
    #             that = "that"
    #             NP_RC = " ".join([D3[0], NP3[0], Rel, D1[0], NP1[0], "{V_CP}", that, D2[0], NP2[0], "{V_emb}"])
    #     except Exception:
    #         pass
    #
    #     if ambiguous:
    #         V_main = choice(get_matched_by(NP1, "arg_2", self.all_non_ing_transitive_verbs))
    #         V_main_ing = self.get_ing_form(V_main)
    #         NP4 = choice(get_matches_of(V_main, "arg_1", self.safe_nouns))
    #         D4 = choice(get_matched_by(NP4, "arg_1", get_all_very_common_dets()))
    #         V_main = conjugate(V_main, NP4)
    #         V_main_ing = conjugate(V_main_ing, NP4)
    #
    #         data_transform = []
    #         data_base = []
    #         templates = []
    #
    #         # 1_1
    #         data_transform.append(" ".join([D4[0], NP4[0], V_main_ing[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))
    #         data_base.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))
    #         templates.append(template + ",1_1")
    #
    #         # 0_0
    #         option = random.randint(0, 1)
    #         templates.append(template + ",0_0,option=%d" % option)
    #         if option == 0:
    #             data_transform.append(
    #                 " ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP_ing[0], V_emb=V_emb[0])]))
    #             data_base.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))
    #         else:
    #             data_transform.append(
    #                 " ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb_ing[0])]))
    #             data_base.append(" ".join([D4[0], NP4[0], V_main[0], NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0])]))
    #
    #     else:  # unambiguous
    #         V_main = choice(get_matched_by(NP1, "arg_1", self.all_non_CP_non_ing_verbs))
    #         V_main_ing = self.get_ing_form(V_main)
    #         V_main_args = verb_args_from_verb(verb=V_main, subj=NP1)
    #         V_main = conjugate(V_main, NP1)
    #         V_main_ing = conjugate(V_main_ing, NP1)
    #
    #         data_transform = []
    #         data_base = []
    #         templates = []
    #
    #         # 1_0
    #         data_transform.append(
    #             " ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main_ing[0], join_args(V_main_args["args"])]))
    #         data_base.append(
    #             " ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))
    #         templates.append(template + ",1_0")
    #
    #         # 0_1
    #         data_transform.append(
    #             " ".join([NP_RC.format(V_CP=V_CP_ing[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))
    #         data_base.append(
    #             " ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))
    #         templates.append(template + ",0_1")
    #
    #         # Note: The template can't be used because it cannot form a fully ambiguous or unambiguous minimal pair
    #         # data_transform.append(" ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb_ing[0]), V_main[0], join_args(V_main_args["args"])]))
    #         # data_base.append(" ".join([NP_RC.format(V_CP=V_CP[0], V_emb=V_emb[0]), V_main[0], join_args(V_main_args["args"])]))
    #
    #     track_sentence = [
    #         (V_CP, NP1, V_emb, NP2, NP3, V_main),
    #         (V_CP, NP1, V_emb, NP2, NP3, V_main)
    #     ]
    #
    #     return data_transform, data_base, track_sentence, templates


generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/structure/" + generator.uid)