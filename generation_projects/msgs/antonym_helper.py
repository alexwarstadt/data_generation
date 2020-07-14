
from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
# import generation_projects.msgs.person_helper
from utils.exceptions import *

class AntonymHelper(data_generator.InductiveBiasesGenerator):
    def __init__(self,
                 uid: str,
                 linguistic_feature_type: str,
                 linguistic_feature_description: str,
                 surface_feature_type: str,
                 surface_feature_description: str,
                 control_paradigm: bool):
        super().__init__(uid,
                         linguistic_feature_type,
                         linguistic_feature_description,
                         surface_feature_type,
                         surface_feature_description,
                         control_paradigm)

        def split_verbs(verbs):
            sets = []
            for v in verbs:
                matching_sets = list(filter(lambda s: v["root"] in s or v["antonym"] in s or v["synonym_hypernym_hyponym"] in s, sets))
                if len(matching_sets) == 0:
                    sets.append(frozenset({v["root"], v["antonym"], v["synonym_hypernym_hyponym"]}))
                elif len(matching_sets) == 1:
                    sets[sets.index(matching_sets[0])] |= frozenset({v["root"], v["antonym"], v["synonym_hypernym_hyponym"]})
                else:
                    print(v[0], " has multiple matches!")
            random.shuffle(sets)
            in_domain_sets = sets[:int(len(sets)/2)]
            out_domain_sets = sets[int(len(sets)/2):]
            in_domain = []
            out_domain = []
            for s in in_domain_sets:
                for root in s:
                    in_domain.extend(list(get_all("root", root)))
            for s in out_domain_sets:
                for root in s:
                    out_domain.extend(list(get_all("root", root)))
            return np.unique(np.array(in_domain)), np.unique(np.array(out_domain))

        def split_adjs(adjs):
            all_adjectives = get_all("category", "N\\N")
            sets = []
            for a in adjs:
                matching_sets = list(filter(lambda s: a["expression"] in s, sets))
                if len(matching_sets) == 0:
                    sets.append(frozenset({a["expression"],
                                           get_all("expression", a["antonym"], all_adjectives)[0]["expression"],
                                           get_all("expression", a["synonym_hypernym_hyponym"], all_adjectives)[0][
                                               "expression"]}))
                elif len(matching_sets) == 1:
                    try:
                        sets[sets.index(matching_sets[0])] |= \
                            frozenset({a["expression"],
                                       get_all("expression", a["antonym"], all_adjectives)[0]["expression"],
                                       get_all("expression", a["synonym_hypernym_hyponym"], all_adjectives)[0][
                                           "expression"]})
                    except Exception:
                        pass
                else:
                    print(a[0], " has multiple matches!")
            random.shuffle(sets)
            in_domain = np.unique(
                np.array([get_all("expression", item, all_adjectives)[0] for s in sets[:int(len(sets) / 2)] for item in s]))
            out_domain = np.unique(
                np.array([get_all("expression", item, all_adjectives)[0] for s in sets[int(len(sets) / 2):] for item in s]))
            return in_domain, out_domain

        ant_verbs = np.array(list(filter(lambda v: v["antonym"] != "" and v["synonym_hypernym_hyponym"] != "", all_verbs)))
        ant_adjs = np.array(list(filter(lambda v: v["antonym"] != "" and v["synonym_hypernym_hyponym"] != "", get_all("category", "N\\N"))))
        self.in_domain_verbs, self.out_domain_verbs = split_verbs(ant_verbs)
        self.in_domain_adjs, self.out_domain_adjs = split_adjs(ant_adjs)
        self.in_domain_verbs_main = np.intersect1d(self.in_domain_verbs, ant_verbs)
        self.out_domain_verbs_main = np.intersect1d(self.out_domain_verbs, ant_verbs)
        self.in_domain_adjs_main = np.intersect1d(self.in_domain_adjs, ant_adjs)
        self.out_domain_adjs_main = np.intersect1d(self.out_domain_adjs, ant_adjs)
        self.out_domain_transitive_verbs_main = np.intersect1d(all_transitive_verbs, self.out_domain_verbs_main)
        self.out_domain_intransitive_verbs_main = np.intersect1d(all_intransitive_verbs, self.out_domain_verbs_main)
        self.empty = get_all("expression", "")[0]

    def args_matching_3_verbs(self, v1, v2, v3, frequent=True, subj=None, aux=None, allow_negated=True, allow_modal=True,
                            allow_recursion=False, allow_quantifiers=True):
        """
        :param verb: a vocab entry for a verb
        :param frequent: should only frequent vocab be generated?
        :param subj: if supplied, the value of the subject in the returned dict. If None, a subject will be generated.
        :param aux: if supplied, the value of the auxiliary in the returned dict. If None, an auxiliary will be generated.
        :param allow_negated: should negated auxiliaries (e.g. has't) be generated?
        :param allow_modal: should modal auxiliaries (e.g. might) be generated?
        :param allow_recursion: for verbs that select for a clause or VP, should other clause/VP embedding verbs be generated in the embedded position?
        :param allow_quantifiers: should quantifiers (e.g. most, every) be generated as determiners for DPs?
        :return: dict of all arguments of verb: {subject:x1, auxiliary:x2, verb:x3, args:[arg_1, arg_2, ..., arg_n]}
        """
        args = {}
        if frequent:
            freq_vocab = get_all("frequent", "1")
        else:
            freq_vocab = vocab

        # all verbs have a subject
        if subj is None:
            args["subj"] = N_to_DP_mutate(choice(get_matches_of(v1, "arg_1",
                                                                get_matches_of(v2, "arg_1",
                                                                               get_matches_of(v3, "arg_1", (get_all("category", "N", freq_vocab)))))),
                                          allow_quantifiers=allow_quantifiers)
        else:
            args["subj"] = subj

        # all verbs have an auxiliary (or null)
        if aux is None:
            args["aux"] = return_aux(v1, args["subj"], allow_negated=allow_negated, allow_modal=allow_modal)
        else:
            args["aux"] = aux

        # INTRANSITIVE
        if v1["category"] == "S\\NP":
            args["args"] = []

        # TRANSITIVE
        if v1["category"] == "(S\\NP)/NP":
            args["args"] = [N_to_DP_mutate(choice(get_matches_of(v1, "arg_2",
                                                                 get_matches_of(v2, "arg_2",
                                                                                get_matches_of(v3, "arg_2",
                                                                                               get_all("category", "N", freq_vocab))))),
                                           allow_quantifiers=allow_quantifiers)]

        # # FROM-ING EMBEDDING
        # if v1["category"] == "(S\\NP)/(S[from]\\NP)":
        #     obj = N_to_DP_mutate(choice(get_matches_of(v1, "arg_2",
        #                                                get_matches_of(v2, "arg_2",
        #                                                               get_matches_of(v3, "arg_2", freq_vocab)))), allow_quantifiers=allow_quantifiers)
        #     if allow_recursion:
        #         VP = V_to_VP_mutate(choice(get_matched_by(obj, "arg_1", all_ing_verbs)), frequent=frequent, aux=False)
        #     else:
        #         safe_verbs = np.intersect1d(all_ing_verbs, all_non_recursive_verbs)
        #         VP = V_to_VP_mutate(choice(get_matched_by(obj, "arg_1", safe_verbs)), frequent=frequent, aux=False)
        #     VP[0] = "from " + VP[0]
        #     args["args"] = [obj, VP]
        #
        # # RAISING TO OBJECT
        # if v1["category_2"] == "V_raising_object":
        #     if allow_recursion:
        #         v_emb = choice(all_bare_verbs)
        #     else:
        #         safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
        #         v_emb = choice(safe_verbs)
        #     args_emb = verb_args_from_verb(v_emb, frequent)
        #     VP = V_to_VP_mutate(v_emb, frequent=frequent, args=args_emb, aux=False)
        #     VP[0] = "to " + VP[0]
        #     args["args"] = [args_emb["subj"], VP]
        #
        # # OBJECT CONTROL
        # if v1["category_2"] == "V_control_object":
        #     obj = N_to_DP_mutate(choice(get_matches_of(v1, "arg_2",
        #                                                get_matches_of(v2, "arg_2",
        #                                                               get_matches_of(v3, "arg_2")), allow_quantifiers=allow_quantifiers)))
        #     if allow_recursion:
        #         v_emb = choice(get_matched_by(obj, "arg_1", all_bare_verbs))
        #     else:
        #         safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
        #         v_emb = choice(get_matched_by(obj, "arg_1", safe_verbs))
        #     VP = V_to_VP_mutate(v_emb, frequent=frequent, aux=False)
        #     VP[0] = "to " + VP[0]
        #     args["args"] = [obj, VP]

        # CLAUSE EMBEDDING
        if v1["category"] == "(S\\NP)/S":
            emb_clause = make_sentence(frequent)
            if v1["arg_2"] == "expression_that":
                emb_clause[0] = "that " + emb_clause
            if v1["arg_2"] == "expression_wh":
                emb_clause[0] = "whether " + emb_clause
            args["args"] = [emb_clause]

        # # QUESTION EMBEDDING
        # if v1["category"] == "(S\\NP)/Q":
        #     args["args"] = [make_emb_subj_question(frequent)]
        #     # TODO: implement other kinds of questions
        #
        # # SUBJECT CONTROL
        # if v1["category"] == "(S\\NP)/(S[to]\\NP)":
        #     if allow_recursion:
        #         v_emb = choice(get_matched_by(args["subj"], "arg_1", all_bare_verbs))
        #     else:
        #         safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
        #         v_emb = choice(get_matched_by(args["subj"], "arg_1", safe_verbs))
        #     VP = V_to_VP_mutate(v_emb, frequent=frequent, aux=False)
        #     VP[0] = "to " + VP[0]
        #     args["args"] = [VP]
        #
        # # RAISING TO SUBJECT
        # if verb["category_2"] == "V_raising_subj":
        #     if allow_recursion:
        #         v_emb = choice(all_bare_verbs)
        #     else:
        #         safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
        #         v_emb = choice(safe_verbs)
        #     args_emb = verb_args_from_verb(v_emb, frequent, subj=False)
        #     VP = V_to_VP_mutate(v_emb, frequent=frequent, args=args_emb, aux=False)
        #     VP[0] = "to " + VP[0]
        #     args["args"] = [VP]

        return args
