from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets_dynamic import *
import random
import argparse

# TODO: prevent repeated nouns
# TODO: sample non-binders from all nouns


class MyGenerator(data_generator.StructureDependenceGenerator):
    def __init__(self):
        super().__init__(uid="reflexive",
                         linguistic_feature_description="Is the reflexive bound by a valid antecedent?",
                         surface_feature_description="Is the reflexive bound by its most recent predecessor?")

        self.safe_nouns = np.intersect1d(get_all_frequent(), get_all_common_nouns())
        self.CP_nouns = get_all("category", "N/S", get_all_nominals())
        self.all_CP_verbs = get_all("category", "(S\\NP)/S")
        self.all_himself = get_all_conjunctive([("gender", "m"), ("sg", "1")], self.safe_nouns)
        self.all_herself = get_all_conjunctive([("gender", "f"), ("sg", "1")], self.safe_nouns)
        self.all_itself = get_all_conjunctive([("animate", "0"), ("sg", "1")], self.safe_nouns)
        self.all_themselves = np.intersect1d(get_all_plural_nouns(), self.safe_nouns)
        self.all_agreeing_nouns = np.union1d(self.all_himself, np.union1d(self.all_herself, np.union1d(self.all_itself, self.all_themselves)))
        self.all_reflexive_nouns = np.array([n for n in self.all_agreeing_nouns if len(get_matched_by(n, "arg_1", get_matched_by(n, "arg_2", get_all_refl_preds()))) > 0])
        self.all_not_himself = np.setdiff1d(self.safe_nouns, self.all_himself)
        self.all_not_herself = np.setdiff1d(self.safe_nouns, self.all_herself)
        self.all_not_itself = np.setdiff1d(self.safe_nouns, self.all_itself)
        self.all_not_themselves = np.setdiff1d(self.safe_nouns, self.all_themselves)
        # self.all_possibly_plural_transitive_verbs = np.intersect1d(self.all_transitive_verbs, all_possibly_plural_verbs)
        # self.plural_noun = choice(all_plural_nouns)

    def sample(self, ambiguous=None, one_template=None):
        """
        Sample sentences from this set of sub-templates.
        The one_template option makes it possible to generate data from only a single sub-template.
        """

        if one_template is not None:
            assert(ambiguous is not None)
            data_transform, data_base, track_sentence, templates = getattr(self, one_template)(ambiguous=ambiguous)
            data = self.build_pair(transform_1=data_transform[0],
                                   transform_0=data_transform[1],
                                   base_1=data_base[0],
                                   base_0=data_base[1],
                                   template_1=templates[0],
                                   template_0=templates[1],
                                   ambiguous=ambiguous)
            return data, track_sentence

        track_sentence = []
        option = random.randint(0, 7)
        if option == 0:
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_2_RCs(ambiguous=True)
        elif option == 1:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_nested_rc(ambiguous=True)
        elif option == 2:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_verb_RC(ambiguous=True)
        elif option == 3:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_noun(ambiguous=True)
        elif option == 4:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_noun_RC(ambiguous=True)
        elif option == 5:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_nested_RC_2_RCs(ambiguous=True)
        elif option == 6:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_1_RC(ambiguous=True)
        elif option == 7:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_nested_CP_verb(ambiguous=True)
        else:    
            data_transform_in, data_base_in, track_sentence_in, templates_in = self.sample_CP_under_RC(ambiguous=True)
            
        track_sentence.extend(track_sentence_in)

        option = random.randint(0, 3)
        if option == 0:
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_nested_rc(ambiguous=False)
        elif option == 1:    
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_verb_RC(ambiguous=False)
        elif option == 2:    
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_noun_RC(ambiguous=False)
        elif option == 3:    
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_1_RC(ambiguous=False)
        else:    
            data_transform_out, data_base_out, track_sentence_out, templates_out = self.sample_CP_under_RC(ambiguous=False)
        track_sentence.extend(track_sentence_out)

        try:
            data = self.build_paradigm(
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
        except Exception:
            pass

        return data, track_sentence

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

    def subject_relative_clause(self, subj, reflexive=False, binder=False, coindexes=[], other_verbs=[], nested=False, avoid=[]):
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
        obj_sample_space = self.all_reflexive_nouns if binder else self.safe_nouns
        for verb in other_verbs:
            try:
                obj_sample_space = get_matches_of(verb[0], verb[1], obj_sample_space)
            except IndexError:
                raise MatchNotFoundError("")
        try:
            if binder:
                obj = choice(obj_sample_space, avoid_add=avoid)
                V = choice(get_matched_by(subj, "arg_1", get_matched_by(obj, "arg_2", V_sample_space)))
            else:
                V = choice(get_matched_by(subj, "arg_1", V_sample_space))
                obj = choice(get_matches_of(V, "arg_2", obj_sample_space), avoid_add=avoid)
        except IndexError:
            raise MatchNotFoundError("")
        V = conjugate(V, subj)
        obj_refl = self.return_reflexive(obj)
        obj = N_to_DP_mutate(obj, very_common_det=True)
        if nested:
            RC = " ".join([rel[0], V[0], "{n}", "{rc}"])
        else:
            RC = " ".join([rel[0], V[0], "{n}"])
        return RC, obj, obj_refl, V


    def object_relative_clause(self, obj, reflexive=False, binder=False, coindexes=[], other_verbs=[], nested=False, avoid=[]):
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
        subj_sample_space = self.all_reflexive_nouns if binder else self.safe_nouns
        for verb in other_verbs:
            try:
                subj_sample_space = get_matches_of(verb[0], verb[1], subj_sample_space)
            except IndexError:
                raise MatchNotFoundError("")
        try:
            if binder:
                subj = choice(subj_sample_space, avoid_add=avoid)
                V = choice(get_matched_by(subj, "arg_1", get_matched_by(obj, "arg_2", V_sample_space)))
            else:
                V = choice(get_matched_by(obj, "arg_2", V_sample_space))
                subj = choice(get_matches_of(V, "arg_2", subj_sample_space), avoid_add=avoid)
        except IndexError:
            raise MatchNotFoundError("")
        V = conjugate(V, subj)
        subj_refl = self.return_reflexive(subj)
        if subj_refl is None and binder:
            pass
        subj = N_to_DP_mutate(subj, very_common_det=True)
        if nested:
            RC = " ".join([rel[0], "{n}", "{rc}", V[0]])
        else:
            RC = " ".join([rel[0], "{n}", V[0]])
        return RC, subj, subj_refl, V

    def sample_2_RCs(self, ambiguous):
        # The boy who saw the child helped the girl who knew the actor.
        # NP1     RC1     NP_RC1    V1     NP2      RC2      NP_RC2

        if not ambiguous:
            raise Exception("This paradigm must be ambiguous")
        template = "2_RCs"

        optionA = random.randint(0, 1)
        # optionA = 0: 0 binds 1
        # The girl who saw herself  helped the boy who knew the actor.
        # NP1      RC1     NP1_refl V1     NP2     RC2      NP_RC2

        # optionA = 1: 2 binds 3
        # The boy who saw the child helped the girl who knew herself.
        # NP1     RC1     NP_RC1    V1     NP2      RC2      NP2_refl

        optionB = random.randint(0, 1)
        # optionB = 0: 0 binds 3 (*)
        # The boy who saw the child helped the girl who knew himself.
        # NP1     RC1     NP_RC1    V1     NP2      RC2      NP1_refl

        # optionB = 1: 1 binds 3 (*)
        # The child who saw the boy helped the girl who knew himself.
        # NP1       RC1     NP_RC1  V1     NP2      RC2      NP_RC1_refl

        avoid = []
        if optionA == 0:
            NP1 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            RC1, NP_RC1, NP_RC1_refl, V_RC1 = self.subject_relative_clause(NP1, reflexive=True, binder=optionB==1, coindexes=[NP1], avoid=avoid)
            V1 = conjugate(choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs())), NP1)
            NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", get_all_common_nouns()), avoid_add=avoid))
            coindexes = [NP1] if optionB == 0 else [NP_RC1]
            RC2, NP_RC2, NP_RC2_refl, V_RC2 = self.subject_relative_clause(NP2, reflexive=True, coindexes=coindexes, avoid=avoid)

        else:
            NP2 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2, very_common_det=True)
            if optionB == 0:
                NP1 = choice(self.all_reflexive_nouns, avoid_add=avoid)
                NP1_refl = self.return_reflexive(NP1)
                NP1 = N_to_DP_mutate(NP1, very_common_det=True)
                try:
                    V1 = choice(get_matched_by(NP1, "arg_1", get_matched_by(NP2, "arg_2", get_all_transitive_verbs())))
                except Exception:
                    pass
            else:
                V1 = choice(get_matched_by(NP2, "arg_2", get_all_transitive_verbs()))
                NP1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", get_all_common_nouns()), avoid_add=avoid), very_common_det=True)
            V1 = conjugate(V1, NP1)
            RC1, NP_RC1, NP_RC1_refl, V_RC1 = self.subject_relative_clause(NP1, binder=optionB==1, avoid=avoid)
            coindexes = [NP1, NP2] if optionB == 0 else [NP_RC1, NP2]
            RC2, NP_RC2, NP_RC2_refl, V_RC2 = self.subject_relative_clause(NP2, reflexive=True, coindexes=coindexes, avoid=avoid)

        data_transform = []
        data_base = []
        templates = []
        track_sentence = []
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
        avoid = []
        template = "nested_rc"
        if ambiguous:
            # optionA = random.randint(0, 1)
            optionA = 0     # TODO implement more of these if time
            if optionA == 0:
                optionB = random.randint(0, 1)  # 0 = 0 binds 2; 1 = 1 binds 3
                if optionB == 0:  # 0 = 0 binds 2
                    # The boy that helped the girl who hurt herself/himself     ate the pie.
                    # NP1     RC          NP_RC    RCb      NP_RC_refl/NP1_refl V1  NP2
                    NP1 = choice(self.all_reflexive_nouns, avoid_add=avoid)
                    NP1_refl = self.return_reflexive(NP1)
                    NP1 = N_to_DP_mutate(NP1, very_common_det=True)
                    V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
                    V1 = conjugate(V1, NP1)
                    NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                    option_RC = random.randint(0, 1)
                    template += ",RC1=%d" % option_RC
                    if option_RC == 0:
                        RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, binder=True, nested=True, avoid=avoid)
                    else:
                        RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, binder=True, nested=True, avoid=avoid)
                    RCb, NP_RCb, NP_RCb_refl, V_RCb = self.subject_relative_clause(NP_RC, reflexive=True, coindexes=[NP1, NP_RC], avoid=avoid)

                    # 1_1
                    data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RC_refl)), V1[0], NP2[0]]))
                    data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RC[0])), V1[0], NP2[0]]))
                    templates.append(template + ",1_1,optionA=%d" % optionA)

                    # 0_0
                    data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP1_refl)), V1[0], NP2[0]]))
                    data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP1[0])), V1[0], NP2[0]]))
                    templates.append(template + ",0_0,optionB=%d" % optionB)

                else:  # 1 binds 3
                    # The boy that found the girl who hurt herself/the child helped the child/*herself.
                    # NP1     RC         NP_RC    RCb      NP_RC_refl/NP_RCb V1     NP2/NP_RC_refl
                    V1 = choice(get_all_refl_preds())
                    NP1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", get_all_common_nouns()), avoid_add=avoid), very_common_det=True)
                    V1 = conjugate(V1, NP1)
                    NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                    option_RC = random.randint(0, 1)
                    template += ",RC1=%d" % option_RC
                    if option_RC == 0:
                        RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, binder=True, nested=True, other_verbs=[(V1, "arg_2")], avoid=avoid)
                    else:
                        RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, binder=True, nested=True, other_verbs=[(V1, "arg_2")], avoid=avoid)
                    RCb, NP_RCb, NP_RCb_refl, V_RCb = self.subject_relative_clause(NP_RC, reflexive=True, coindexes=[NP1, NP_RC], avoid=avoid)

                    # 1_1
                    data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RC_refl)), V1[0], NP2[0]]))
                    data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RC[0])), V1[0], NP2[0]]))
                    templates.append(template + ",1_1,optionA=%d" % optionA)

                    # 0_0
                    data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP_RC_refl]))
                    data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0], rc=RCb.format(n=NP_RCb[0])), V1[0], NP_RC[0]]))
                    templates.append(template + ",0_0,optionB=%d" % optionB)

        else:  # 1 binds 4:
            # The girl that ate the pie that shocked the boy hurt herself/himself.
            # NP1      RC       NP_RC   RCb          NP_RCb  V1   NP1_ref/NP_RCb_refl
            V1 = choice(get_all_refl_preds())
            NP1 = choice(get_matches_of(V1, "arg_2", get_matches_of(V1, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
            V1 = conjugate(V1, NP1)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            option = random.randint(0, 1)
            template += ",RC1=%d" % option
            if option == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, nested=True, avoid=avoid)
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, nested=True, avoid=avoid)
            RCb, NP_RCb, NP_RCb_refl, V_RCb = self.subject_relative_clause(NP_RC, binder=True, other_verbs=[(V1, "arg_1")], avoid=avoid)
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
        template = "CP_verb_RC"
        avoid = []

        optionA = 1 if not ambiguous else random.randint(0, 2)  # Relative clause attached to NP1, NP2, or NP3

        if optionA == 0:    # RC attached to NP1
            # The boy that played a game is saying that the girl hurt herself/*himself.
            # NP1     RC          NP_RC  V1        that NP2      V2   NP2_refl/NP1_refl
            V1 = choice(self.all_CP_verbs)
            optionB = random.randint(0, 1)  # distractor is matrix subject (0) or RC argument (1)
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_reflexive_nouns), avoid_add=avoid) if optionB == 0 else choice(get_matches_of(V1, "arg_1", self.safe_nouns), avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = conjugate(V1, NP1)
            option = random.randint(0, 1)
            template += f",RC={option}"
            if option == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, binder=optionB == 1, avoid=avoid)
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, binder=optionB == 1, avoid=avoid)
            V2 = choice(get_matched_by(NP_RC, "arg_2", get_all_refl_preds())) if optionB == 1 else choice(get_matched_by(NP1, "arg_2", get_all_refl_preds()))
            try:
                NP2 = choice(get_matches_of(V2, "arg_1", get_matches_of(V2, "arg_2", self.all_reflexive_nouns)), avoid_add=avoid)
            except Exception:
                pass
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2, very_common_det=True)
            V2 = conjugate(V2, NP2)

            # 1_1
            try:
                data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP2_refl]))
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP2[0]]))
                templates.append(f"{template},1_1,optionA={optionA}")
            except Exception:
                pass

            # 0_0
            if optionB == 0:
                data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP1_refl]))
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP1[0]]))
            else:
                data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP_RC_refl]))
                data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], "that", NP2[0], V2[0], NP_RC[0]]))
            templates.append(f"{template},1_1,optionA={optionA},optionB={optionB}")

        elif optionA == 1:  # RC attached to NP2
            V1 = choice(self.all_CP_verbs)
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_reflexive_nouns), avoid_add=avoid) if ambiguous == 1 else choice(get_matches_of(V1, "arg_1", get_all_nouns()), avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1)
            if NP1_refl is None:
                pass
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = conjugate(V1, NP1)
            NP2 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            V2 = choice(get_matched_by(NP2, "arg_1", get_all_transitive_verbs())) if ambiguous \
                else choice(get_matched_by(NP2, "arg_2", get_matched_by(NP2, "arg_1", get_all_refl_preds())))
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2, very_common_det=True)
            V2 = conjugate(V2, NP2)
            NP3 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_2", get_all_nouns()), avoid_add=avoid), very_common_det=True)
            if ambiguous:
                # The boy is saying that the girl that hurt herself/*himself  played a game.
                # NP1     V1        that NP2      RC        NP2_refl/NP1_refl V2   NP3
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2, reflexive=True, coindexes=[NP2, NP1], avoid=avoid)
                # 1_1
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP2_refl), V2[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP2[0]), V2[0], NP3[0]]))
                templates.append(f"{template},1_1,optionA={optionA}")

                # 0_0
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP1_refl), V2[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP1[0]), V2[0], NP3[0]]))
                templates.append(f"{template},0_0,optionA={optionA}")

            else:  # unambiguous
                # The child is saying that the girl that helped a boy hurt herself/*himself.
                # NP1       V1        that NP2      RC          NP_RC V2   NP2_refl/NP_RC_refl
                option = random.randint(0, 1)
                template += f",RC={option}"
                if option == 0:
                    RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2, binder=True, other_verbs=[(V2, "arg_2")], avoid=avoid)
                else:
                    RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP2, binder=True, other_verbs=[(V2, "arg_2")], avoid=avoid)
                # 1_0
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP2_refl]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP2[0]]))
                templates.append(f"{template},1_0")

                # 0_1
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP_RC_refl]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], RC.format(n=NP_RC[0]), V2[0], NP_RC[0]]))
                templates.append(f"{template},0_1")

        else:   # RC attached to NP3
            # The child is saying that the boy helped a girl that hurt herself/*himself.
            # NP1       V1        that NP2     V2     NP3    RC        NP3_refl/NP2_refl
            optionB = random.randint(0, 1)  # distractor is matrix subject (0) or embedded subject argument (1)
            V1 = choice(self.all_CP_verbs)
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_reflexive_nouns), avoid_add=avoid) if optionB == 0 else choice(get_matches_of(V1, "arg_1", get_all_nouns()), avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1) if optionB == 0 else None
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = conjugate(V1, NP1)

            NP2 = choice(self.all_reflexive_nouns, avoid_add=avoid) if optionB == 1 else choice(get_all_nouns(), avoid_add=avoid)
            NP2_refl = self.return_reflexive(NP2) if optionB == 1 else None
            NP2 = N_to_DP_mutate(NP2, very_common_det=True)

            NP3 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            NP3_refl = self.return_reflexive(NP3)
            NP3 = N_to_DP_mutate(NP3, very_common_det=True)
            try:
                V2 = conjugate(choice(get_matched_by(NP2, "arg_1", get_matched_by(NP3, "arg_2", get_all_transitive_verbs()))), NP2)
            except IndexError:
                raise MatchNotFoundError("")
            coindexes = [NP3, NP1] if optionB == 0 else [NP3, NP2]
            RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP3, reflexive=True, coindexes=coindexes, avoid=avoid)

            # 1_1
            data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP3_refl)]))
            data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP3[0])]))
            templates.append(f"{template},1_1,optionA={optionA}")

            # 0_0
            if optionB == 0:  # distractor is NP1
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP1_refl)]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP1[0])]))
            else:  # distractor is NP2
                data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP2_refl)]))
                data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], NP3[0], RC.format(n=NP2[0])]))
            templates.append(f"{template},1_1,optionA={optionA},optionB={optionB}")

        return data_transform, data_base, track_sentence, templates

    def sample_CP_noun(self, ambiguous):
        # The idea that the boy hurt  himself/the girl     is shocking the child/*himself
        # NP1      that NP1_emb V_emb NP1_emb_refl/NP2_emb V1          NP2/NP1_emb_refl
        if not ambiguous:
            raise Exception("This paradigm must be ambiguous")
        avoid = []

        template = "CP_noun"
        NP1 = choice(self.CP_nouns, avoid_add=avoid)
        D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
        V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
        V1 = conjugate(V1, NP1)
        NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", self.safe_nouns), avoid_add=avoid), very_common_det=True)

        V_emb = choice(get_all_refl_preds())
        NP1_emb = choice(get_matches_of(V_emb, "arg_1", get_matches_of(V1, "arg_2", self.all_reflexive_nouns)), avoid_add=avoid)
        NP1_emb_refl = self.return_reflexive(NP1_emb)
        NP1_emb = N_to_DP_mutate(NP1_emb, very_common_det=True)
        V_emb = conjugate(V_emb, NP1_emb)
        NP2_emb = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_2", self.safe_nouns), avoid_add=avoid))
        data_transform = []
        data_base = []
        templates = []
        track_sentence = []

        # 1_1
        try:
            data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP1_emb_refl, V1[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP1_emb[0], V1[0], NP2[0]]))
            templates.append(template + ",1_1")
        except Exception:
            pass

        # 0_0
        data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP1_emb_refl]))
        data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP1_emb[0]]))
        templates.append(template + ",0_0")

        return data_transform, data_base, track_sentence, templates

    def sample_CP_noun_RC(self, ambiguous):
        """
        The idea that the girl who hurt the boy chased herself/the man is shocking the actor/himself    (unambig)
        The idea that the girl chased a boy that hurt himself/the woman is shocking the actor/himself     (ambig)
        The idea that the girl chased a boy is shocking the actor that hurt himself/herself     (ambig)
        """

        template = "CP_noun_RC"
        data_transform = []
        data_base = []
        templates = []
        track_sentence = []
        avoid = []

        if not ambiguous:   # RC must attach to embedded subject
            # The idea that the girl who hurt the boy chased herself/the man     is shocking the actor/*himself
            # NP1      that NP1_emb  RC       NP_RC   V_emb  NP_emb_refl/NP2_emb V1          NP2/NP2_emb_refl
            NP1 = choice(self.CP_nouns, avoid_add=avoid)
            D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
            V1 = choice(get_matched_by(NP1, "arg_1", get_all_refl_preds()))
            V1 = conjugate(V1, NP1)
            NP1_emb = choice(self.all_reflexive_nouns, avoid_add=avoid)
            V_emb = conjugate(choice(get_matched_by(NP1_emb, "arg_1", get_matched_by(NP1_emb, "arg_2", get_all_refl_preds()))), NP1_emb)
            NP1_emb_refl = self.return_reflexive(NP1_emb)
            NP1_emb = N_to_DP_mutate(NP1_emb, very_common_det=True)
            NP2_emb = choice(get_matches_of(V_emb, "arg_2", get_matches_of(V1, "arg_2", self.all_reflexive_nouns)), avoid_add=avoid)
            NP2_emb_refl = self.return_reflexive(NP2_emb)
            NP2_emb = N_to_DP_mutate(NP2_emb, very_common_det=True)
            NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", self.safe_nouns), avoid_add=avoid), very_common_det=True)
            option_RC = random.randint(0, 1)
            template += f",RC={option_RC}"
            if option_RC == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1_emb, avoid=avoid)
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1_emb, avoid=avoid)

            # 1_0
            data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), V_emb[0], NP1_emb_refl, V1[0], NP2[0]]))
            data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), V_emb[0], NP1_emb[0], V1[0], NP2[0]]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), V_emb[0], NP2_emb[0], V1[0], NP2_emb_refl]))
            data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], RC.format(n=NP_RC[0]), V_emb[0], NP2_emb[0], V1[0], NP2_emb[0]]))
            templates.append(template + ",0_1")


        else:
            optionA = random.randint(0, 1)  # 0 = RC on embedded obj; 1 = RC on matrix object
            if optionA == 0:    # RC on embedded obj
                # The idea that the girl chased a boy   that hurt himself/the woman  is shocking the actor/*himself
                # NP1      that NP1_emb  V_emb  NP2_emb RC        NP2_emb_refl/NP_RC V1          NP2/*NP2_emb_refl

                NP1 = choice(self.CP_nouns, avoid_add=avoid)
                D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
                V1 = conjugate(choice(get_matched_by(NP1, "arg_1", get_all_refl_preds())), NP1)
                NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", get_all_nouns()), avoid_add=avoid))
                NP2_emb = choice(get_matches_of(V1, "arg_2", self.all_reflexive_nouns), avoid_add=avoid)
                NP2_emb_refl = self.return_reflexive(NP2_emb)
                NP2_emb = N_to_DP_mutate(NP2_emb, very_common_det=True)
                V_emb = choice(get_matched_by(NP2_emb, "arg_2", get_all_transitive_verbs()))
                NP1_emb = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_1", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                V_emb = conjugate(V_emb, NP1_emb)
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2_emb, reflexive=True, coindexes=[NP2_emb], avoid=avoid)


                # 1_1
                data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP2_emb_refl), V1[0], NP2[0]]))
                data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP2_emb[0]), V1[0], NP2[0]]))
                templates.append(template + f",optionA={optionA},1_1")

                # 0_0
                data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP_RC[0]), V1[0], NP2_emb_refl]))
                data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], RC.format(n=NP_RC[0]), V1[0], NP2_emb[0]]))
                templates.append(template + f",optionA={optionA},0_0")

            else:    # RC on matrix obj
                # The idea that the girl chased an actor is shocking the boy that hurt himself/*herself
                # NP1      that NP1_emb  V_emb  NP2_emb  V1          NP2     RC        NP2_refl/*NP1_emb_refl
                NP1 = choice(self.CP_nouns, avoid_add=avoid)
                D1 = choice(get_matched_by(NP1, "arg_1", get_all_very_common_dets()))
                V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
                V1 = conjugate(V1, NP1)
                NP1_emb = choice(self.all_reflexive_nouns, avoid_add=avoid)
                NP1_emb_refl = self.return_reflexive(NP1_emb)
                NP1_emb = N_to_DP_mutate(NP1_emb, very_common_det=True)
                NP2 = choice(get_matches_of(V1, "arg_2", self.all_reflexive_nouns), avoid_add=avoid)
                NP2_refl = self.return_reflexive(NP2)
                NP2 = N_to_DP_mutate(NP2)
                V_emb = conjugate(choice(get_matched_by(NP1_emb, "arg_1", get_all_transitive_verbs())), NP1_emb)
                NP2_emb = N_to_DP_mutate(choice(get_matched_by(V_emb, "arg_2", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                RC, _, _, _ = self.subject_relative_clause(NP2, reflexive=True, coindexes=[NP2, NP1_emb], avoid=avoid)

                # 1_1
                data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP2_refl)]))
                data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP2[0])]))
                templates.append(template + f",optionA={optionA},1_1")

                # 0_0
                data_transform.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP1_emb_refl)]))
                data_base.append(" ".join([D1[0], NP1[0], "that", NP1_emb[0], V_emb[0], NP2_emb[0], V1[0], NP2[0], RC.format(n=NP1_emb[0])]))
                templates.append(template + f",optionA={optionA},0_0")

        return data_transform, data_base, track_sentence, templates

    def sample_nested_RC_2_RCs(self, ambiguous):
        if not ambiguous:
            raise Exception("This paradigm must be ambiguous")

        template = "nested_RC_2_RCs"
        data_transform = []
        data_base = []
        templates = []
        track_sentence = []
        avoid = []
        option = random.randint(0, 2)
        if option == 0:
            # The boy that ate the pie the actor baked  is chasing a girl that hurt herself/*himself.
            # NP1          RC1 NP_RC1  RC_emb NP_RC_emb V1         NP2    RC2      NP2_refl/NP1_refl
            NP1 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
            V1 = conjugate(V1, NP1)
            RC1, NP_RC1, _, _ = self.subject_relative_clause(NP1, nested=True, avoid=avoid)
            option_RC = random.randint(0, 1)
            template += f",RC={option_RC}"
            if option_RC == 0:  # subject RC
                RC_emb, NP_RC_emb, _, _ = self.subject_relative_clause(NP_RC1, binder=True, avoid=avoid)
            else:  # object RC
                RC_emb, NP_RC_emb, _, _ = self.object_relative_clause(NP_RC1, binder=True, avoid=avoid)
            try:
                NP2 = choice(get_matches_of(V1, "arg_2", self.all_reflexive_nouns), avoid_add=avoid)
            except Exception:
                raise MatchNotFoundError("")
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2, very_common_det=True)
            RC2, NP_RC2, _, _ = self.subject_relative_clause(NP2, reflexive=True, coindexes=[NP1, NP2], avoid=avoid)

            # 1_1
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP_RC_emb[0])), V1[0], NP2[0], RC2.format(n=NP2_refl)]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP_RC_emb[0])), V1[0], NP2[0], RC2.format(n=NP2[0])]))
            templates.append(template + f",option={option},1_1")

            # 0_0
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP_RC_emb[0])), V1[0], NP2[0], RC2.format(n=NP1_refl)]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP_RC_emb[0])), V1[0], NP2[0], RC2.format(n=NP1[0])]))
            templates.append(template + f",option={option},0_0")

        elif option == 1:
            # The boy that chased the girl that hurt   herself/*himself     ate a pie that the actor baked.
            # NP1     RC1         NP_RC1   RC_emb      NP_RC1_refl/NP1_refl V1  NP2   RC2 NP_RC2
            NP1 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
            V1 = conjugate(V1, NP1)
            option_RC = random.randint(0, 1)
            template += f",RC={option_RC}"
            if option_RC == 0:  # subject RC
                RC1, NP_RC1, NP_RC1_refl, _ = self.subject_relative_clause(NP1, binder=True, nested=True, avoid=avoid)
            else:  # object RC
                RC1, NP_RC1, NP_RC1_refl, _ = self.object_relative_clause(NP1, binder=True, nested=True, avoid=avoid)
            RC_emb, _, _, _ = self.subject_relative_clause(NP_RC1, reflexive=True, coindexes=[NP1, NP_RC1], avoid=avoid)
            try:
                NP2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", self.safe_nouns), avoid_add=avoid), very_common_det=True)
            except Exception:
                raise MatchNotFoundError("")
            RC2, NP_RC2, _, _ = self.subject_relative_clause(NP2, avoid=avoid)

            # 1_1
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP_RC1_refl)), V1[0], NP2[0], RC2.format(n=NP_RC2[0])]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP_RC1[0])), V1[0], NP2[0], RC2.format(n=NP_RC2[0])]))
            templates.append(template + f",option={option},1_1")

            # 0_0
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP1_refl)), V1[0], NP2[0], RC2.format(n=NP_RC2[0])]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0], rc=RC_emb.format(n=NP1[0])), V1[0], NP2[0], RC2.format(n=NP_RC2[0])]))
            templates.append(template + f",option={option},0_0")

        else:
            # The child that ate the pie chased the boy that helped the girl that hurt   herself/*himself.
            # NP1       RC1      NP_RC1  V1     NP2     RC2         NP_RC2   RC_emb      NP_RC2_refl/NP2_refl
            NP2 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2, very_common_det=True)
            V1 = choice(get_matched_by(NP2, "arg_2", get_all_transitive_verbs()))
            option_RC = random.randint(0, 1)
            template += f",RC={option_RC}"
            if option_RC == 0:  # subject RC
                RC2, NP_RC2, NP_RC2_refl, _ = self.subject_relative_clause(NP2, binder=True, nested=True, avoid=avoid)
            else:  # object RC
                RC2, NP_RC2, NP_RC2_refl, _ = self.object_relative_clause(NP2, binder=True, nested=True, avoid=avoid)
            RC_emb, _, _, _ = self.subject_relative_clause(NP_RC2, reflexive=True, coindexes=[NP2, NP_RC2], avoid=avoid)
            NP1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.safe_nouns), avoid_add=avoid), very_common_det=True)
            RC1, NP_RC1, _, _ = self.subject_relative_clause(NP1, avoid=avoid)
            V1 = conjugate(V1, NP1)

            # 1_1
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP_RC2[0], rc=RC_emb.format(n=NP_RC2_refl))]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP_RC2[0], rc=RC_emb.format(n=NP_RC2[0]))]))
            templates.append(template + f",option={option},1_1")

            # 0_0
            data_transform.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP_RC2[0], rc=RC_emb.format(n=NP2_refl))]))
            data_base.append(" ".join([NP1[0], RC1.format(n=NP_RC1[0]), V1[0], NP2[0], RC2.format(n=NP_RC2[0], rc=RC_emb.format(n=NP2[0]))]))
            templates.append(template + f",option={option},0_0")
            
        return data_transform, data_base, track_sentence, templates

    def sample_1_RC(self, ambiguous):
        template = "1_RC"
        data_base = []
        data_transform = []
        track_sentence = []
        templates = []
        avoid = []
        if ambiguous:
            # The boy helped the girl that hurt herself/*himself
            # NP1      V1    NP2      RC        NP2_refl/NP1_refl
            # RC on object
            # coindexes: (NP2, NP_RC), (NP1, NP_RC)
            NP2 = choice(self.all_reflexive_nouns, avoid_add=avoid)
            RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP2, reflexive=True, coindexes=[NP2], avoid=avoid)
            V1 = choice(get_matched_by(NP2, "arg_2", get_all_transitive_verbs()))
            NP1 = choice(get_matches_of(V1, "arg_1", get_matches_of(V_RC, "arg_2", self.all_reflexive_nouns)), avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = conjugate(V1, NP1)
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)

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
            # NP1      RC          NP_RC   V1   NP1_refl/NP_RC_refl
            # RC on subject
            # coindexes: (NP1, NP2), (NP_RC, NP2)
            NP1 = choice(self.all_reflexive_nouns)
            V1 = choice(get_matched_by(NP1, "arg_1", get_matched_by(NP1, "arg_2", get_all_refl_preds())))
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1, very_common_det=True)
            V1 = conjugate(V1, NP1)
            NP2 = choice(get_matches_of(V1, "arg_2", self.safe_nouns), avoid_add=avoid)
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)
            option_RC = random.randint(0, 1)
            template += f",RC={option_RC}"
            if option_RC == 0:
                RC, NP_RC, NP_RC_refl, V_RC = self.subject_relative_clause(NP1, binder=True, other_verbs=[(V1, "arg_2")], avoid=avoid)
            else:
                RC, NP_RC, NP_RC_refl, V_RC = self.object_relative_clause(NP1, binder=True, other_verbs=[(V1, "arg_2")], avoid=avoid)

            # 1_0
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP1_refl]))
            data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP1[0]]))
            templates.append(template + ",1_0")

            # 0_1
            data_transform.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP_RC_refl]))
            data_base.append(" ".join([NP1[0], RC.format(n=NP_RC[0]), V1[0], NP_RC[0]]))
            templates.append(template + ",0_1")
            
        return data_transform, data_base, track_sentence, templates

    def sample_nested_CP_verb(self, ambiguous):
        if not ambiguous:
            raise Exception("This paradigm must be ambiguous")
        template = "nested_CP_verb"
        data_base = []
        data_transform = []
        track_sentence = []
        templates = []
        avoid = []
        V1 = choice(self.all_CP_verbs)
        V2 = choice(self.all_CP_verbs, avoid=[V1])
        option = random.randint(0, 1)
        if option == 0:  # (NP3, NP4), (NP1, NP4)
            # The boy is saying that the actor thought that the girl hurt herself/*himself.
            # NP1     V1        that NP2       V2      that NP3      V3   NP3_refl/NP1_refl
            NP1 = choice(get_matches_of(V1, "arg_1", self.all_reflexive_nouns), avoid_add=avoid)
            NP1_refl = self.return_reflexive(NP1)
            NP1 = N_to_DP_mutate(NP1)
            V1 = conjugate(V1, NP1)
            NP2 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_1", get_all_nouns()), avoid_add=avoid))
            V2 = conjugate(V2, NP2)
            V3 = choice(get_matched_by(NP1, "arg_2", get_all_refl_preds()))
            NP3 = choice(get_matches_of(V3, "arg_2", get_matches_of(V3, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
            NP3_refl = self.return_reflexive(NP3)
            NP3 = N_to_DP_mutate(NP3)
            V3 = conjugate(V3, NP3)
            refl = NP1_refl
            binder = NP1[0]

        else:  # (NP3, NP4), (NP2, NP4)
            # The actor is saying that the boy thought that the girl hurt herself/*himself.
            # NP1       V1        that NP2     V2      that NP3      V3   NP3_refl/NP2_refl
            NP1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", get_all_nouns()), avoid_add=avoid))
            V1 = conjugate(V1, NP1)
            NP2 = choice(get_matches_of(V2, "arg_1", self.all_reflexive_nouns), avoid_add=avoid)
            NP2_refl = self.return_reflexive(NP2)
            NP2 = N_to_DP_mutate(NP2)
            V2 = conjugate(V2, NP2)
            V3 = choice(get_matched_by(NP2, "arg_2", get_all_refl_preds()))
            NP3 = choice(get_matches_of(V3, "arg_2", get_matches_of(V3, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
            NP3_refl = self.return_reflexive(NP3)
            NP3 = N_to_DP_mutate(NP3)
            V3 = conjugate(V3, NP3)
            refl = NP2_refl
            binder = NP2[0]

        # 1_1
        try:
            data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], "that", NP3[0], V3[0], NP3_refl]))
            data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], "that", NP3[0], V3[0], NP3[0]]))
            templates.append(template + f",option={option},1_1")

            # 0_0
            data_transform.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], "that", NP3[0], V3[0], refl]))
            data_base.append(" ".join([NP1[0], V1[0], "that", NP2[0], V2[0], "that", NP3[0], V3[0], binder]))
            templates.append(template + f",option={option},0_0")

        except Exception:
            pass

        return data_transform, data_base, track_sentence, templates

    def sample_CP_under_RC(self, ambiguous):
        template = "CP_under_RC"
        data_base = []
        data_transform = []
        track_sentence = []
        templates = []
        avoid = []
        if ambiguous:
            option = random.randint(0, 1)
            if option == 0:
                # The boy that said that the girl hurt  herself/*himself   is eating a pie.
                # NP1     THAT V_CP THAT NP2      V_emb NP2_refl/NP1_refl V_mat     NP3
                V_CP = choice(self.all_CP_verbs)
                NP1 = choice(get_matches_of(V_CP, "arg_1", self.all_reflexive_nouns), avoid_add=avoid)
                NP1_refl = self.return_reflexive(NP1)
                NP1 = N_to_DP_mutate(NP1, very_common_det=True)
                V_CP = conjugate(V_CP, NP1)
                V_emb = choice(get_matched_by(NP1, "arg_2", get_all_refl_preds()))
                NP2 = choice(get_matches_of(V_emb, "arg_2", get_matches_of(V_emb, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
                NP2_refl = self.return_reflexive(NP2)
                NP2 = N_to_DP_mutate(NP2, very_common_det=True)
                V_emb = conjugate(V_emb, NP2)
                V_mat = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
                V_mat = conjugate(V_mat, NP1)
                NP3 = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_2", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                # 1_1
                data_transform.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP2_refl, V_mat[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP2[0], V_mat[0], NP3[0]]))
                templates.append(template + f",option={option},1_1")
                # 0_0
                data_transform.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP1_refl, V_mat[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP1[0], V_mat[0], NP3[0]]))
                templates.append(template + f",option={option},0_0")

            else:
                # The child helped the boy that said that the girl hurt  herself/*himself
                # NP1       V_mat  NP2     that V_CP that NP3      V_emb NP3_refl/NP2_refl
                V_CP = choice(self.all_CP_verbs)
                NP2 = choice(get_matches_of(V_CP, "arg_1", self.all_reflexive_nouns), avoid_add=avoid)
                NP2_refl = self.return_reflexive(NP2)
                NP2 = N_to_DP_mutate(NP2, very_common_det=True)
                V_CP = conjugate(V_CP, NP2)
                V_emb = choice(get_matched_by(NP2, "arg_2", get_all_refl_preds()))
                NP3 = choice(get_matches_of(V_emb, "arg_2", get_matches_of(V_emb, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
                NP3_refl = self.return_reflexive(NP3)
                NP3 = N_to_DP_mutate(NP3, very_common_det=True)
                V_emb = conjugate(V_emb, NP3)
                V_mat = choice(get_matched_by(NP2, "arg_2", get_all_transitive_verbs()))
                NP1 = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_1", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                V_mat = conjugate(V_mat, NP1)
                # 1_1
                data_transform.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", V_CP[0], "that", NP3[0], V_emb[0], NP3_refl]))
                data_base.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", V_CP[0], "that", NP3[0], V_emb[0], NP3[0]]))
                templates.append(template + f",option={option},1_1")
                # 0_0
                data_transform.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", V_CP[0], "that", NP3[0], V_emb[0], NP2_refl]))
                data_base.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", V_CP[0], "that", NP3[0], V_emb[0], NP2[0]]))
                templates.append(template + f",option={option},0_0")


        else:  # Not ambiguous
            option = random.randint(0, 2)
            if option == 0:
                # The girl that the boy said hurt  herself/*himself  is eating a pie.
                # NP1      that NP2     V_CP V_emb NP1_refl/NP2_refl V_mat     NP3
                V_CP = choice(self.all_CP_verbs)
                NP2 = choice(get_matches_of(V_CP, "arg_1", self.all_reflexive_nouns), avoid_add=avoid)
                NP2_refl = self.return_reflexive(NP2)
                NP2 = N_to_DP_mutate(NP2, very_common_det=True)
                V_CP = conjugate(V_CP, NP2)
                V_emb = choice(get_matched_by(NP2, "arg_2", get_all_refl_preds()))
                NP1 = choice(get_matches_of(V_emb, "arg_2", get_matches_of(V_emb, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
                NP1_refl = self.return_reflexive(NP1)
                NP1 = N_to_DP_mutate(NP1, very_common_det=True)
                V_emb = conjugate(V_emb, NP1)
                V_mat = choice(get_matched_by(NP1, "arg_1", get_all_transitive_verbs()))
                NP3 = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_2", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                V_mat = conjugate(V_mat, NP1)
                # 1_0
                data_transform.append(" ".join([NP1[0], "that", NP2[0], V_CP[0], V_emb[0], NP1_refl, V_mat[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], "that", NP2[0], V_CP[0], V_emb[0], NP1[0], V_mat[0], NP3[0]]))
                templates.append(template + f",option={option},1_0")
                # 0_1
                data_transform.append(" ".join([NP1[0], "that", NP2[0], V_CP[0], V_emb[0], NP2_refl, V_mat[0], NP3[0]]))
                data_base.append(" ".join([NP1[0], "that", NP2[0], V_CP[0], V_emb[0], NP2[0], V_mat[0], NP3[0]]))
                templates.append(template + f",option={option},0_1")

            elif option == 1:
                # The girl that said that the child helped the boy hurt  herself/*himself
                # NP1      that V_CP that NP2       V_emb  NP3     V_mat NP1_refl/NP3_refl
                V_CP = choice(self.all_CP_verbs)
                NP1 = choice(get_matches_of(V_CP, "arg_1", self.all_reflexive_nouns), avoid_add=avoid)
                NP1_refl = self.return_reflexive(NP1)
                NP1 = N_to_DP_mutate(NP1, very_common_det=True)
                V_CP = conjugate(V_CP, NP1)
                V_mat = choice(get_matched_by(NP1, "arg_1", get_matched_by(NP1, "arg_2", get_all_refl_preds())))
                NP3 = choice(get_matches_of(V_mat, "arg_2", get_matches_of(V_mat, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
                NP3_refl = self.return_reflexive(NP3)
                NP3 = N_to_DP_mutate(NP3, very_common_det=True)
                V_mat = conjugate(V_mat, NP1)
                V_emb = choice(get_matched_by(NP3, "arg_2", get_all_transitive_verbs()))
                NP2 = N_to_DP_mutate(choice(get_matches_of(V_emb, "arg_1", get_all_nouns()), avoid_add=avoid), very_common_det=True)
                V_emb = conjugate(V_emb, NP2)
                # 1_0
                data_transform.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP3[0], V_mat[0], NP1_refl]))
                data_base.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP3[0], V_mat[0], NP1[0]]))
                templates.append(template + f",option={option},1_0")
                # 0_1
                data_transform.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP3[0], V_mat[0], NP3_refl]))
                data_base.append(" ".join([NP1[0], "that", V_CP[0], "that", NP2[0], V_emb[0], NP3[0], V_mat[0], NP3[0]]))
                templates.append(template + f",option={option},0_1")

            else:
                # The child helped the girl that the boy said hurt  herself/*himself
                # NP1       V_mat  NP2      THAT NP3     V_CP V_emb NP2_refl/NP3_refl
                V_CP = choice(self.all_CP_verbs)
                NP3 = choice(get_matches_of(V_CP, "arg_1", self.all_reflexive_nouns), avoid_add=avoid)
                NP3_refl = self.return_reflexive(NP3)
                NP3 = N_to_DP_mutate(NP3, very_common_det=True)
                V_CP = conjugate(V_CP, NP3)
                V_emb = choice(get_matched_by(NP3, "arg_2", get_all_refl_preds()))
                NP2 = choice(get_matches_of(V_emb, "arg_2", get_matches_of(V_emb, "arg_1", self.all_reflexive_nouns)), avoid_add=avoid)
                NP2_refl = self.return_reflexive(NP2)
                NP2 = N_to_DP_mutate(NP2, very_common_det=True)
                V_emb = conjugate(V_emb, NP2)
                V_mat = choice(get_matched_by(NP2, "arg_2", get_all_transitive_verbs()))
                NP1 = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_1", get_all_nouns())), very_common_det=True)
                V_mat = conjugate(V_mat, NP1)
                # 1_0
                data_transform.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", NP3[0], V_CP[0], V_emb[0], NP2_refl]))
                data_base.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", NP3[0], V_CP[0], V_emb[0], NP2[0]]))
                templates.append(template + f",option={option},1_0")
                # 0_1
                data_transform.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", NP3[0], V_CP[0], V_emb[0], NP3_refl]))
                data_base.append(" ".join([NP1[0], V_mat[0], NP2[0], "that", NP3[0], V_CP[0], V_emb[0], NP3[0]]))
                templates.append(template + f",option={option},0_1")


        return data_transform, data_base, track_sentence, templates


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract re verbs.')
    parser.add_argument("--number_to_generate", "-n", default=5000, type=int, help="Number of pairs/quadruples to generate")
    parser.add_argument("--output_path", "-o", type=str, help="Relative path to output directory")
    parser.add_argument("--one_template", "-t", type=str, help="If provided, the name of template to generate data from")
    parser.add_argument('--ambiguous', dest='ambiguous', action='store_true')
    parser.add_argument('--unambiguous', dest='ambiguous', action='store_false')
    args = parser.parse_args()
    generator = MyGenerator()
    generator.generate_paradigm(number_to_generate=args.number_to_generate,
                                rel_output_path=args.output_path + generator.uid,
                                one_template=args.one_template,
                                ambiguous=args.ambiguous)

# x sample_2_RCs(ambiguous=True)
# x sample_nested_rc(ambiguous=True)
# x sample_CP_verb_RC(ambiguous=True)
# x sample_CP_noun(ambiguous=True)
# x sample_CP_noun_RC(ambiguous=True)
# ? sample_nested_RC_2_RCs(ambiguous=True)  This has tons of errors, but hard to fix
# ? sample_1_RC(ambiguous=True)  This has a few errors, but hard to fix
# x sample_nested_CP_verb(ambiguous=True)
# x sample_CP_under_RC(ambiguous=True)
# x sample_nested_rc(ambiguous=False)
# x sample_CP_verb_RC(ambiguous=False)
# x sample_CP_noun_RC(ambiguous=False)
# x sample_1_RC(ambiguous=False)  Some errors, but not too many
# x sample_CP_under_RC(ambiguous=False)