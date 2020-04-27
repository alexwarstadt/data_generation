from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from generation_projects.inductive_biases.syntactic_category_helper import SyntacticCategoryGenerator
import random
# import generation_projects.inductive_biases.person_helper

class MyGenerator(SyntacticCategoryGenerator):
    def __init__(self):
        super().__init__(uid="syntactic_category_control",
                         linguistic_feature_type="syntactic",
                         linguistic_feature_description="Is there an adjective present?",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)
        # clause_adjs = get_matched_by(get_all("expression", "John")[0], "arg_1", get_all("category_2", "Adj_clausal"))
        # clause_verb_roots = list(set(get_all("category", "(S\\NP)/S")["root"]))
        # random.shuffle(clause_adjs)
        # random.shuffle(clause_verb_roots)
        # self.clause_adjs_in_domain = clause_adjs[:len(clause_adjs)/2]
        # self.clause_adjs_out_domain = clause_adjs[len(clause_adjs)/2:]
        # self.clause_verbs_in_domain = filter(lambda x: x["root"] in clause_verb_roots[:len(clause_verb_roots)/2], all_ing_verbs)
        # self.clause_verbs_out_domain = filter(lambda x: x["root"] in clause_verb_roots[len(clause_verb_roots)/2:], all_bare_verbs)
        # self.be_verbs = get_all()

    def sample(self):
        # Training 1
        # The man is happy that Bill left.
        # DP      BE Adj1  THAT S

        # Training 0
        # The man is saying that Bill left.
        # DP      BE V1     THAT S

        # Test 1
        # The man seems disappointed that Bill left.
        # DP      SEEM  Adj2     THAT S

        # Test 0
        # The man seems to think that Bill left.
        # DP      SEEM  TO V2    THAT S

        DP = N_to_DP_mutate(choice(all_animate_nouns))
        be = choice(get_matched_by(DP, "arg_1", all_finite_copulas))
        seem = "seem" if DP["sg"] == "0" else "seems"
        S = make_sentence()
        Adj1 = choice(self.clause_adjs_in_domain)
        Adj2 = choice(self.clause_adjs_out_domain)
        V1 = choice(self.clause_verbs_in_domain)
        V2 = choice(self.clause_verbs_out_domain)


        track_sentence = [
                (DP[0], be[0], Adj1[0], S[0]), #training 1/1
                (DP[0], be[0], V1[0], S[0]), #training 0/0
                (DP[0], Adj2[0], S[0]), #Test 1/0
                (DP[0], V2[0], S[0]), #Test 0/1
            ]

        data = self.build_paradigm(
            training_1_1="%s %s %s that %s." % (DP[0], be[0], Adj1[0], S[0]),
            training_0_0="%s %s %s that %s." % (DP[0], be[0], V1[0], S[0]),
            test_1_0="%s %s %s that %s." % (DP[0], seem, Adj2[0], S[0]),
            test_0_1="%s %s to %s that %s." % (DP[0], seem, V2[0], S[0]),
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=5000, rel_output_path="outputs/inductive_biases/" + generator.uid)
