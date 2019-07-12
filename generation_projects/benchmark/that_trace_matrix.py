from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.string_utils import string_beautify


class BindingGenerator(data_generator.Generator):
    def __init__(self):
        super().__init__()
        self.all_safe_nouns = np.setdiff1d(self.all_nouns, self.all_singular_neuter_animate_nouns)
        self.all_safe_common_nouns = np.intersect1d(self.all_safe_nouns, self.all_common_nouns)
        self.all_nonfinite_embedding_verbs = get_all_conjunctive([("finite", "0")], self.all_embedding_verbs)
        self.all_wh = get_all("category", "NP_wh")
        self.all_who = get_all_conjunctive([("expression", "who")], self.all_wh)

    def sample(self):
        # who does John think called Suzie
        # wh  V_do N1   V1    V2     N2

        # who does John think that called Suzie
        # wh  V_do N1   V1    that V2     N2

        V1 = choice(self.all_nonfinite_embedding_verbs)
        try:
            N1 = N_to_DP_mutate(choice(get_matches_of(V1, "arg_1", self.all_safe_nouns)))
        except IndexError:
            pass
        V_do = return_aux(V1,N1,allow_negated=False)
        # select transitive or intransitive V2
        x = random.random()
        if x < 1 / 2:
            # transitive V2
            V2 = choice(self.all_transitive_verbs)
            try:
                N2 = N_to_DP_mutate(choice(get_matches_of(V2, "arg_2", self.all_safe_nouns)))
            except IndexError:
                pass
        else:
            V2 = choice(self.all_intransitive_verbs)
            N2 = " "
        #wh = choice(get_matches_of(V2, "arg_1", self.all_wh))
        wh = choice(self.all_who)

        V2 = conjugate(V2, wh)
        #Vembed = conjugate(Vembed, N1)

        metadata = [
            "category=agreement-field=syntax/semantics-linguistics_term=binding-UID=that_trace_matrix-crucial_item=%s" % "",
            "category=agreement-field=syntax/semantics-linguistics_term=binding-UID=that_trace_matrix-crucial_item=%s" % "that"
        ]
        judgments = [1, 0]
        sentences = [
            "%s %s %s %s %s %s." % (wh[0], V_do[0], N1[0], V1[0], V2[0], N2[0]),
            "%s %s %s %s that %s %s." % (wh[0], V_do[0], N1[0], V1[0], V2[0], N2[0])
        ]
        return metadata, judgments, sentences


binding_generator = BindingGenerator()
binding_generator.generate_paradigm(absolute_path="G:/My Drive/NYU classes/Semantics team project seminar - Spring 2019/dataGeneration/data_generation/outputs/benchmark/that_trace_matrix.tsv")



