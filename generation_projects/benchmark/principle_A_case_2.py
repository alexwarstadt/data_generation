from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class BindingGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax/semantics",
                         linguistics="binding",
                         uid="principle_A_case_2",
                         simple_lm_method=True,
                         one_prefix_method=True,
                         two_prefix_method=False,
                         lexically_identical=False)
        self.all_safe_nouns = np.setdiff1d(all_nouns, all_singular_neuter_animate_nouns)
        self.special_verbs = np.append(get_all("expression", "imagine"), np.append(get_all("expression", "forget about"), get_all("expression", "think about")))

    def sample(self):
        # John imagines himself       seeing     Mary
        # N1   V1       refl_match    Vembed_ing N2
        # John imagines himself      saw           Mary
        # N1   V1       refl_match   Vembed_finite N2

        special_verbs = choice(self.special_verbs)
        V1 = choice(get_all("root", special_verbs["root"]))
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_nouns)))
        Vembed_base = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        Verb_embed = get_all("root", Vembed_base["root"])
        Vembed_ing = choice(get_all('ing', "1", Verb_embed))
        Vembed_finite = choice(get_matched_by(N1, "arg_1", get_all('finite', "1", Verb_embed)))
        refl_match = choice(get_matched_by(N1, "arg_1", all_reflexives))
        N2 = N_to_DP_mutate(choice(get_matches_of(Vembed_base, "arg_2", all_nouns)))

        V1 = conjugate(V1, N1)

        data = {
            "sentence_good": "%s %s %s %s %s." % (N1[0], V1[0], refl_match[0], Vembed_ing[0], N2[0]),
            "sentence_bad": "%s %s %s %s %s." % (N1[0], V1[0], refl_match[0], Vembed_finite[0], N2[0]),
            "one_prefix_prefix": "%s %s %s" % (N1[0], V1[0], refl_match[0]),
            "one_prefix_word_good": Vembed_ing[0],
            "one_prefix_word_bad": Vembed_finite[0]
        }
        return data, data["sentence_good"]

binding_generator = BindingGenerator()
binding_generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % binding_generator.uid)
