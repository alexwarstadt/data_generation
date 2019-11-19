from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="control_raising",
                         uid="existential_there_object_raising",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        good_quantifiers_sg_str = ["a", "an", ""]
        good_quantifiers_pl_str = ["no", "some", "few", "fewer than three", "more than three", "many", "a lot of", ""]
        self.good_quantifiers_sg = reduce(np.union1d, [get_all("expression", s, all_quantifiers) for s in good_quantifiers_sg_str])
        self.good_quantifiers_pl = reduce(np.union1d, [get_all("expression", s, all_quantifiers) for s in good_quantifiers_pl_str])
        bad_emb_subjs = reduce(np.union1d, (all_relational_poss_nouns, all_proper_names, get_all("category", "NP")))
        self.safe_emb_subjs = np.setdiff1d(all_nominals, bad_emb_subjs)
        self.raising_verbs = get_all("category_2", "V_raising_object")
        self.control_verbs = get_all("category_2", "V_control_object")

    def sample(self):
        # John   believed there to be a party    happening
        # m_subj V_raise  THERE TO BE D emb_subj VP
        # John   persuaded there to be a party    happening
        # m_subj V_control THERE TO BE D emb_subj VP

        no_match = True
        while no_match:
            try:
                V_raise = choice(self.raising_verbs)
                V_control = choice(np.intersect1d(get_same_aux_verbs(V_raise), self.control_verbs))
                m_subj = N_to_DP_mutate(choice(get_matches_of(V_raise, "arg_1", get_matches_of(V_control, "arg_1"))))
            except Exception:
                continue
            no_match = False

        Aux = return_aux(V_raise, m_subj)

        emb_subj = N_to_DP_mutate(choice(self.safe_emb_subjs), determiner=False)
        D = choice(get_matched_by(emb_subj, "arg_1", self.good_quantifiers_sg)) \
            if emb_subj["sg"] == "1" \
            else choice(get_matched_by(emb_subj, "arg_1", self.good_quantifiers_pl))
        V = choice(get_matched_by(emb_subj, "arg_1", all_ing_verbs))
        allow_negated = D[0] != "no" and D[0] != "some"
        args = verb_args_from_verb(V, subj=emb_subj, allow_negated=allow_negated)
        VP = V_to_VP_mutate(V, args=args, aux=False)

        data = {
            "sentence_good": "%s %s %s there to be %s %s %s." % (m_subj[0], Aux[0], V_raise[0], D[0], emb_subj[0], VP[0]),
            "sentence_bad": "%s %s %s there to be %s %s %s." % (m_subj[0], Aux[0], V_control[0], D[0], emb_subj[0], VP[0]),
            "two_prefix_prefix_good": "%s %s %s" % (m_subj[0], Aux[0], V_raise[0]),
            "two_prefix_prefix_bad": "%s %s %s" % (m_subj[0], Aux[0], V_control[0]),
            "two_prefix_word": "there"
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

