from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="island_effects",
                         uid="coordinate_structure_constraint_complex_left_branch",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.all_D_wh = get_all("category_2", "D_wh")
        self.which_what = np.append(get_all_conjunctive([("expression", "which")], self.all_D_wh), get_all_conjunctive([("expression", "what")], self.all_D_wh))

    def sample(self):
        # What pie did  John cook and Mary eat?
        # wh   N3  V_do N1   V1   and N2   V2_match
        # What did  John cook pie and Mary eat?
        # wh   V_do N1   V1   N3  and N2   V2_match

        V1 = choice(all_non_finite_transitive_verbs)
        N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
        N3 = choice(get_matches_of(V1, "arg_2", get_all('pl', '1', all_common_nouns)))
        V_do = return_aux(V1, N1, allow_negated=False)
        V2 = choice(get_matched_by(N3, "arg_2", all_transitive_verbs))

        # make sure V1 and V2 are the same form
        Verb2 = get_all("root", V2["root"])
        if V1['bare'] == '1':
            Vmatch = "bare"
        elif V1['ing'] == '1':
            Vmatch = "ing"
        elif V1['en'] == '1':
            Vmatch = "en"
        else:
            pass
        V2_match = choice(get_all(Vmatch, "1", Verb2))
        N2 = N_to_DP_mutate(choice(get_matches_of(V2_match, "arg_1", all_nouns)))

        if N3['animate'] == "1":
            wh = choice(self.which_what)
        else:
            wh = choice(self.all_D_wh)

        data = {
            "sentence_good": "%s %s %s %s %s and %s %s?" % (wh[0], N3[0], V_do[0], N1[0], V1[0], N2[0], V2_match[0]),
            "sentence_bad": "%s %s %s %s %s and %s %s?" % (wh[0], V_do[0], N1[0], V1[0], N3[0], N2[0], V2_match[0]),
            "two_prefix_prefix_good": "%s %s %s %s %s and" % (wh[0], N3[0], V_do[0], N1[0], V1[0]),
            "two_prefix_prefix_bad": "%s %s %s %s %s and" % (wh[0], V_do[0], N1[0], V1[0], N3[0]),
            "two_prefix_word": N2[0]
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
