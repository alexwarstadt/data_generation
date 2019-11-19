from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice

class Generator(data_generator.BenchmarkGenerator):
    def __init__(self):
        super().__init__(field="syntax_semantics",
                         linguistics="control_raising",
                         uid="expletive_it_object_raising",
                         simple_lm_method=True,
                         one_prefix_method=False,
                         two_prefix_method=True,
                         lexically_identical=False)
        self.clause_embedding_adjectives = get_all("category_2", "Adj_clausal", get_all("arg_1", "expression=it"))
        self.raising_verbs = get_all("category_2", "V_raising_object")
        self.control_verbs = get_all("category_2", "V_control_object")

    def sample(self):
        # John   may        consider it to be unfortunate that Bill has left.
        # m_subj Aux_raise  V_raise  IT TO BE Adj         THAT sentence
        # John   may          persuade   it to be unfortunate that Bill has left.
        # m_subj Aux_control  V_control  IT TO BE Adj         THAT sentence

        no_match = True
        while no_match:
            try:
                V_raise = choice(self.raising_verbs)
                V_control = choice(self.control_verbs)
                m_subj = N_to_DP_mutate(choice(get_matches_of(V_raise, "arg_1", get_matches_of(V_control, "arg_1"))))
            except Exception:
                continue
            no_match = False
        Aux_raise = return_aux(V_raise, m_subj)
        Aux_control = return_aux(V_control, m_subj)
        Adj = choice(self.clause_embedding_adjectives)
        V_emb = choice(all_verbs)
        sentence = make_sentence_from_verb(V_emb)

        data = {
            "sentence_good": "%s %s %s it to be %s that %s." % (m_subj[0], Aux_raise[0], V_raise[0], Adj[0], sentence),
            "sentence_bad": "%s %s %s it to be %s that %s." % (m_subj[0], Aux_control[0], V_control[0], Adj[0], sentence),
            "two_prefix_prefix_good": "%s %s %s it to be" % (m_subj[0], Aux_raise[0], V_raise[0]),
            "two_prefix_prefix_bad": "%s %s %s it to be" % (m_subj[0], Aux_control[0], V_control[0]),
            "two_prefix_word": Adj[0]
        }
        return data, data["sentence_good"]

generator = Generator()
generator.generate_paradigm(rel_output_path="outputs/benchmark/%s.jsonl" % generator.uid)

