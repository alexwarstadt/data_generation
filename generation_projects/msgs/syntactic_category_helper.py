from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
# import generation_projects.msgs.person_helper

class SyntacticCategoryGenerator(data_generator.InductiveBiasesGenerator):
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
        clause_adjs = get_matched_by(get_all("expression", "John")[0], "arg_1", get_all("category_2", "Adj_clausal"))
        clause_verb_roots = list(set(get_all("category", "(S\\NP)/S")["root"]))
        np.random.shuffle(clause_adjs)
        np.random.shuffle(clause_verb_roots)
        self.clause_adjs_in_domain = clause_adjs[:int(len(clause_adjs)/2)]
        self.clause_adjs_out_domain = clause_adjs[int(len(clause_adjs)/2):]
        self.clause_verbs_in_domain = list(filter(lambda x: x["root"] in clause_verb_roots[:int(len(clause_verb_roots)/2)], all_ing_verbs))
        self.clause_verbs_out_domain = list(filter(lambda x: x["root"] in clause_verb_roots[int(len(clause_verb_roots)/2):], all_bare_verbs))

        adjs = get_matched_by(get_all("expression", "John")[0], "arg_1", get_all("category_2", "Adj_pred"))
        locales = get_all("locale", "1", all_nouns)
        locales = np.array(list(filter(lambda x: "public" not in x["expression"] and "Great" not in x["expression"], locales)))
        names = np.intersect1d(all_singular_nouns, np.intersect1d(all_animate_nouns, all_proper_names))
        common_nouns = np.intersect1d(all_singular_nouns, np.intersect1d(all_animate_nouns, all_common_nouns))


        self.adjs_in_domain, self.adjs_out_domain = self.split(adjs)
        self.locales_in_domain, self.locales_out_domain = self.split(locales)
        self.names_in_domain, self.names_out_domain = self.split(names)
        self.common_nouns_in_domain, self.common_nouns_out_domain = self.split(common_nouns)
        self.one_word_noun = get_all("category_2", "N_pred")


    def split(self, l):
        np.random.shuffle(l)
        return l[:int(len(l)/2)], l[int(len(l)/2):]

