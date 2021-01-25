#from utils import data_generator
import utils.vocab_sets_db as db
import utils.vocab_table_db as vocab
from utils.data_type import EX
from utils.constituent_building_db import *
from utils.conjugate_db import *
from utils.randomize import choice

class CSCGenerator():#data_generator.BenchmarkGenerator):
    def __init__(self):
        # super().__init__(field="syntax",
        #                  linguistics="island_effects",
        #                  uid="adjunct_island",
        #                  simple_lm_method=True,
        #                  one_prefix_method=False,
        #                  two_prefix_method=False,
        #                  lexically_identical=True)
        all_transitive_verbs = db.get_all_conjunctive(vocab.all_transitive_verbs)
        all_ing_verbs = db.get_all_conjunctive(vocab.all_ing_verbs)
        self.all_ing_transitives = np.intersect1d(all_transitive_verbs, all_ing_verbs)
        self.adverbs = ["before", "while", "after", "without"]
        self.all_nouns = db.get_all_conjunctive(vocab.all_nouns)
        self.all_non_finite_transitive_verbs = db.get_all_conjunctive(vocab.all_non_finite_transitive_verbs)
        self.all_wh_words = db.get_all_conjunctive(vocab.all_wh_words)

    def sample(self):
        # What did      John read  before filing the book?
        # Wh   Aux_mat  Subj V_mat ADV    V_emb  Obj
        # What did      John read  the book before filing?
        # Wh   Aux_mat  Subj V_mat Obj      ADV    V_emb

        # V_mat = choice(all_non_finite_transitive_verbs)
        # Subj = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_1", all_nouns)))
        # Aux_mat = return_aux(V_mat, Subj, allow_negated=False)
        # Obj = N_to_DP_mutate(choice(get_matches_of(V_mat, "arg_2", all_nouns)))
        # V_emb = choice(get_matched_by(Obj, "arg_2", get_matched_by(Subj, "arg_1", self.all_ing_transitives)))
        # Wh = choice(get_matched_by(Obj, "arg_1", all_wh_words))
        # Adv = choice(self.adverbs)

        V_mat = choice(self.all_non_finite_transitive_verbs)
        Subj = N_to_DP_mutate(choice(db.get_matches_of(V_mat, "arg_1", sample_space=self.all_nouns)))
        Aux_mat = return_aux(V_mat, Subj, allow_negated=False)
        Obj = N_to_DP_mutate(choice(db.get_matches_of(V_mat, "arg_2", sample_space=self.all_nouns)))
        match_arg1 = db.get_matched_by(Subj, "arg_1", self.all_ing_transitives, subtable=True)
        match_arg2 = db.get_matched_by(Obj, "arg_2", match_arg1, subtable=True)
        V_emb = choice(match_arg2)
        Wh = choice(db.get_matched_by(Obj, "arg_1", self.all_wh_words, subtable=True))
        Adv = choice(self.adverbs)

        data = {
            "sentence_good": "%s %s %s %s %s %s %s?" % (Wh[EX], Aux_mat[EX], Subj[EX], V_mat[EX], Adv, V_emb[EX], Obj[EX]),
            "sentence_bad": "%s %s %s %s %s %s %s?" % (Wh[EX], Aux_mat[EX], Subj[EX], V_mat[EX], Obj[EX], Adv, V_emb[EX])
        }
        return data, data["sentence_good"]

generator = CSCGenerator()
# generator.generate_paradigm(rel_output_path="outputs/blimp/%s.jsonl" % generator.uid)
for i in range(100):
    _, sentence = generator.sample()
    print(sentence)