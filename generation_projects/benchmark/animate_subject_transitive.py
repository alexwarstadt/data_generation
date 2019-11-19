from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *

class AgreementGenerator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax",
                         linguistics="argument_structure",
                         uid="animate_subject_trans",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        self.all_inanim_subj_allowing_verbs = get_matched_by(choice(all_inanimate_nouns), "arg_1", all_transitive_verbs)
        self.all_anim_subj_allowing_verbs = get_matched_by(choice(all_animate_nouns), "arg_1", all_transitive_verbs)
        self.all_anim_subj_verbs = np.setdiff1d(self.all_anim_subj_allowing_verbs, self.all_inanim_subj_allowing_verbs)
        self.dets = ['the', 'some']

    def sample(self):
        # John      talked to the boy
        # N1_good   V1        N2
        # The table talked to the boy
        # N1_bad    V1        N2

        V1 = choice(self.all_anim_subj_verbs)
        N1_good = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", all_nouns)))
           if N1_good['sg'] == '1':
               N1_bad = N_to_DP_mutate(choice(get_all('sg', '1', all_inanimate_nouns)))
           elif N1_good['pl'] == '1':
               N1_bad = N_to_DP_mutate(choice(get_all('pl', '1', all_inanimate_nouns)))
           else:
               pass
        N2 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_2", all_nouns)))
        V1 = conjugate(V1, N1_good)

        data = {
            "sentence_good": "%s %s %s." % (N1_good[0], V1[0], N2[0]),
            "sentence_bad": "%s %s %s." % (N1_bad[0], V1[0], N2[0]),
            "two_prefix_prefix_good": "%s" % (N1_good[0]),
            "two_prefix_prefix_bad": "%s" % (N1_bad[0]),
            "two_prefix_word": V1[0]
        }
        return data, data["sentence_good"]

generator = AgreementGenerator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
