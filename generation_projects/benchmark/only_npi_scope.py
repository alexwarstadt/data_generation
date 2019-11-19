from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="npi_licensing",
                         uid="only_npi_scope",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=True)
        self.safe_verbs = np.setdiff1d(all_verbs, all_ing_verbs)
        self.safe_subjs = np.setdiff1d(all_nominals, all_proper_names)

    def sample(self):
        # Only the drivers who John     will    help     should ever love the dancers
        # ONLY subj        rel subj_emb aux_emb V_emb    aux    EVER VP
        # The drivers who only John     will    help     should ever love the dancers
        # subj        rel ONLY subj_emb aux_emb V_emb    aux    EVER VP

        V = choice(self.safe_verbs)
        subj = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", self.safe_subjs)))
        args = verb_args_from_verb(V, allow_negated=False, subj=subj)
        VP = V_to_VP_mutate(V, args=args, aux=False)
        rel = choice(get_matched_by(args["subj"], "arg_1", all_relativizers))
        V_emb = choice(get_matched_by(subj, "arg_2", all_transitive_verbs))
        args_emb = verb_args_from_verb(V_emb, allow_negated=False)

        data = {
            "sentence_good": "Only %s %s %s %s %s %s ever %s." % (subj[0], rel[0], args_emb["subj"][0], args_emb["aux"][0], V_emb[0], args["aux"][0], VP[0]),
            "sentence_bad": "%s %s only %s %s %s %s ever %s." % (subj[0], rel[0], args_emb["subj"][0], args_emb["aux"][0], V_emb[0], args["aux"][0], VP[0]),
            "two_prefix_prefix_good": "Only %s %s %s %s %s %s" % (subj[0], rel[0], args_emb["subj"][0], args_emb["aux"][0], V_emb[0], args["aux"][0]),
            "two_prefix_prefix_bad": "%s %s only %s %s %s %s" % (subj[0], rel[0], args_emb["subj"][0], args_emb["aux"][0], V_emb[0], args["aux"][0]),
            "two_prefix_word": "ever"
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)
