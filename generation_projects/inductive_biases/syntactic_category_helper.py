from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random
# import generation_projects.inductive_biases.person_helper

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

#
# generator = MyGenerator()
# generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
