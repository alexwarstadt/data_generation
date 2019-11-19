from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="npi_licensing",
                         uid="sentential_negation_npi_scope",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.safe_matrix_verbs = np.setdiff1d(all_non_finite_verbs, all_ing_verbs)
        self.safe_emb_verbs = np.intersect1d(all_non_finite_verbs, all_transitive_verbs)
        self.safe_subjs = np.setdiff1d(all_nominals, all_proper_names)

    def sample(self):
        # The man who might   see Jane has not ever left.
        # subj    rel aux_emb VP_emb   aux NOT EVER VP
        # The man who might   not see Jane has ever left.
        # subj    rel aux_emb NOT VP_emb   aux EVER VP

        V = choice(self.safe_matrix_verbs)
        subj = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", self.safe_subjs)))
        args = verb_args_from_verb(V, allow_negated=False, subj=subj)
        VP = V_to_VP_mutate(V, aux=False, args=args)
        rel = choice(get_matched_by(args["subj"], "arg_1", all_relativizers))
        V_emb = choice(get_matched_by(subj, "arg_1", self.safe_emb_verbs))
        args_emb = verb_args_from_verb(V_emb, allow_negated=False, subj=args["subj"])
        VP_emb = V_to_VP_mutate(V_emb, aux=False, args=args_emb)

        data = {
            "sentence_good": "%s %s %s %s %s not ever %s." % (args["subj"][0], rel[0], args_emb["aux"][0], VP_emb[0], args["aux"][0], VP[0]),
            "sentence_bad": "%s %s %s not %s %s ever %s." % (args["subj"][0], rel[0], args_emb["aux"][0], VP_emb[0], args["aux"][0], VP[0]),
            "two_prefix_prefix_good": "%s %s %s %s %s not" % (args["subj"][0], rel[0], args_emb["aux"][0], VP_emb[0], args["aux"][0]),
            "two_prefix_prefix_bad": "%s %s %s not %s %s" % (args["subj"][0], rel[0], args_emb["aux"][0], VP_emb[0], args["aux"][0]),
            "two_prefix_word": "ever"
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
