
from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
# import generation_projects.msgs.person_helper

class ControlRaisingHelper(data_generator.InductiveBiasesGenerator):
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

        def split_adjs(adjs):
            np.random.shuffle(adjs)
            in_domain = adjs[:int(len(adjs) / 2)]
            out_domain = adjs[int(len(adjs) / 2):]
            return in_domain, out_domain

        def split_verbs(verbs):
            verb_roots = list(set(verbs["root"]))
            np.random.shuffle(verb_roots)
            in_domain = list(filter(lambda x: x["root"] in verb_roots[:int(len(verb_roots) / 2)], verbs))
            out_domain = list(filter(lambda x: x["root"] in verb_roots[int(len(verb_roots) / 2):], verbs))
            return np.array(in_domain), np.array(out_domain)

        ambiguous_control_raising_roots = ["fail_(S\\NP)/(S[to]\\N)",
                                           "fail_S/S[to]",
                                           "look_S/S[to]",
                                           "threaten_S/S[to]",
                                           # "need_(S\NP)/(S[to]\N)",
                                           # "need_(S\NP)/S[to]",
                                           # "want_(S\NP)/(S[to]\N)",
                                           # "want_(S\NP)/S[to]",
                                           ]
        non_ambiguous_verbs = np.array(list(filter(lambda x: x["root"] not in ambiguous_control_raising_roots, all_verbs)))

        self.v_control_subj_in, self.v_control_subj_out = split_verbs(get_all("category_2", "V_control_subj", non_ambiguous_verbs))
        self.v_raising_subj_in, self.v_raising_subj_out = split_verbs(get_all("category_2", "V_raising_subj", non_ambiguous_verbs))
        self.v_control_obj_in, self.v_control_obj_out = split_verbs(get_all("category_2", "V_control_object", non_ambiguous_verbs))
        self.v_raising_obj_in, self.v_raising_obj_out = split_verbs(get_all("category_2", "V_raising_object", non_ambiguous_verbs))
        self.adj_control_subj_in, self.adj_control_subj_out = split_adjs(get_all("category_2", "Adj_control_subj"))
        self.adj_raising_subj_in, self.adj_raising_subj_out = split_adjs(get_all("category_2", "Adj_raising_subj"))
        self.safe_verbs = np.setdiff1d(non_ambiguous_verbs,
                                       np.array(list(reduce(lambda x, y: np.union1d(x, y),
                                                            [self.v_control_subj_in, self.v_control_subj_out,
                                                             self.v_raising_subj_in, self.v_raising_subj_out,
                                                             self.v_control_obj_in, self.v_control_obj_out,
                                                             self.v_raising_obj_in, self.v_raising_obj_out,
                                                             self.adj_control_subj_in, self.adj_control_subj_out,
                                                             self.adj_raising_subj_in, self.adj_raising_subj_out]))))
