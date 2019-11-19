from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class BindingGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="binding",
                         uid="principle_A_domain_3",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.all_gendered_singular_nouns = get_all("sg", "1", all_gendered_nouns)
        self.all_safe_gendered_nouns = np.setdiff1d(self.all_gendered_singular_nouns, all_relational_nouns)
        self.all_sing_embedding_verbs = np.union1d(get_all_conjunctive([("pres", "1"), ("3sg", "1")], all_embedding_verbs), get_all("bare", "1", all_embedding_verbs))
        self.all_sing_refl_preds = np.union1d(get_all_conjunctive([("pres", "1"), ("3sg", "1")], all_refl_preds), get_all("bare", "1", all_refl_preds))

    def sample(self):
        # John thinks Mary saw      herself.
        # N1   V1     N2   Vembed   refl_match
        # Mary thinks  John saw     herself.
        # N2   V1      N1   Vembed  refl_match

        V1 = choice(self.all_sing_embedding_verbs)
        Vembed = choice(self.all_sing_refl_preds)
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_gendered_nouns)))
        refl_mismatch = choice(get_matched_by(N1, "arg_1", all_reflexives))
        N2 = choice(get_matches_of(Vembed, "arg_1", self.all_safe_gendered_nouns))
        while is_match_disj(N2, refl_mismatch["arg_1"]):
            N2 = choice(get_matches_of(Vembed, "arg_1", self.all_safe_gendered_nouns))
        refl_match = choice(get_matched_by(N2, "arg_1", all_reflexives))
        N2 = N_to_DP_mutate(N2)
        V1 = conjugate(V1, N1)
        Vembed = conjugate(Vembed, N2)

        data = {
            "sentence_good": "%s %s %s %s %s." % (N1[0], V1[0], N2[0], Vembed[0], refl_match[0]),
            "sentence_bad": "%s %s %s %s %s." % (N2[0], V1[0], N1[0], Vembed[0], refl_match[0]),
            "two_prefix_prefix_good": "%s %s %s %s" % (N1[0], V1[0], N2[0], Vembed[0]),
            "two_prefix_prefix_bad": "%s %s %s %s" % (N2[0], V1[0], N1[0], Vembed[0]),
            "two_prefix_word": refl_match[0]
        }
        return data, data["sentence_good"]

binding_generator = BindingGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % binding_generator.uid)

