from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.vocab_sets import *
from utils.string_utils import string_beautify
import random


class SIGenerator(data_generator.ScalarImplicatureGenerator):
    def __init__(self, w, s):
        super().__init__(
            uid="scalar_implicatures"
        )

        self.all_plural_verbs = get_all("3sg", "0", all_verbs)
        self.all_singular_verbs = get_all("3sg", "1", all_verbs)
        self.all_plural_inanimate_nouns = np.intersect1d(all_inanimate_nouns, all_plural_nouns)
        self.all_plural_common_nouns = np.intersect1d(all_common_nouns, all_plural_nouns)

        self.w = w
        self.s = s

        self.managed = choice(get_all("expression", "managed", get_all("past", "1")))
        self.tried = choice(get_all("expression", "tried", get_all("past", "1")))

    #def get_bare(self,V):
     #   bare = get_all_conjunctive(("expression",V),("bare","1"))
      #  return bare

    def sample(self):

        w = self.w
        s = self.s

        V = choice(self.all_plural_verbs)
        #bare = get_bare(V)
        #print(bare)
        #bare = get_all_conjunctive([("expression",V[0]),("bare","1")])
        #print(bare[0])

        lexemes = ""
        if w=="some":
            trigger = "quantifier"
            position = choice(["subject","object"])
            #position = "object"
            #print(position)

            if position=="subject":
                """quantifiers in subject position"""
                V = choice(self.all_plural_verbs)
                N = choice(get_matches_of(V, "arg_1", self.all_plural_common_nouns))
                v_args = verb_args_from_verb(V, subj=N, allow_quantifiers=False)
                Aux = return_aux(V, N, allow_negated=False)
                VP = " ".join([Aux[0],
                               V[0]] +
                              [x[0] for x in v_args["args"]])
                W = "some "+N[0]+" "+VP
                S = "all "+N[0]+" "+VP
                notW = "no "+N[0]+" "+VP
                notS = "not all "+N[0]+" "+VP

            else:
                """quantifiers in object position"""
                V = choice(all_transitive_verbs)
                N1 = choice(get_matches_of(V, "arg_1", all_nouns))
                DP1= N_to_DP_mutate(N1)
                #print(DP1[0])
                N2 = choice(get_matches_of(V, "arg_2", self.all_plural_common_nouns), [N1])
                V_args = verb_args_from_verb(V, subj=N1, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)

                W = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],"some ",N2[0]])
                S = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],"all ",N2[0]])
                notW = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],"no ",N2[0]])
                notS = " ".join([DP1[0],Neg_V_args["aux_neg"][0], Neg_V_args["verb_neg"][0],"all",N2[0]])

        elif w=="ten" or w =="two":
            trigger = "numeral_"+w+"-"+s
            position = choice(["subject","object"])
            #position = "object"

            if position=="subject":
                """numerals in subject position"""
                V = choice(self.all_plural_verbs)
                N = choice(get_matches_of(V, "arg_1", self.all_plural_common_nouns))
                V_args = verb_args_from_verb(V, subj=N)
                Neg_V_args = negate_V_args(V_args)
                Aux = return_aux(V, N, allow_negated=False)
                VP = " ".join([Aux[0],
                               V[0]] +
                              [x[0] for x in V_args["args"]])
                negVP = " ".join([Neg_V_args["aux_neg"][0],
                                  Neg_V_args["verb_neg"][0]] +
                              [x[0] for x in Neg_V_args["args"]])
                W = " ".join([w, N[0], VP])
                S = " ".join([s, N[0], VP])
                notW = " ".join([w, N[0], negVP])
                notS = " ".join([s, N[0], negVP])

            else:
                """numerals in object position"""
                V = choice(all_transitive_verbs)
                N1 = choice(get_matches_of(V, "arg_1", all_nouns))
                DP1= N_to_DP_mutate(N1, allow_quantifiers=False)
                #print(DP1[0])
                N2 = choice(get_matches_of(V, "arg_2", self.all_plural_common_nouns), [N1])
                V_args = verb_args_from_verb(V, subj=N1, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)

                W = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],w,N2[0]])
                S = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],s,N2[0]])
                notW = " ".join([DP1[0],Neg_V_args["aux_neg"][0], Neg_V_args["verb_neg"][0],w,N2[0]])
                notS = " ".join([DP1[0],Neg_V_args["aux_neg"][0], Neg_V_args["verb_neg"][0],s,N2[0]])


        elif w=="or":
            trigger = "connective"
            position = choice("subject","object")

            if position=="subject":
                """connectives in subject position"""

                # always generate plural verbs & nouns to avoid agreement issues with "and"
                V = choice(self.all_plural_verbs)
                N = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", all_plural_nouns)), allow_quantifiers=False)
                if N["animate"]=="0":
                    N2 = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns), [N]), allow_quantifiers=False)
                else:
                    N2 = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", all_plural_animate_nouns), [N]), allow_quantifiers=False)


                V_args = verb_args_from_verb(V, subj=N, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)
                #Aux = return_aux(V, N, allow_negated=False)
                VP = " ".join([V_args["aux"][0], V_args["verb"][0]]+[x[0] for x in V_args["args"]])
                negVP = " ".join([Neg_V_args["aux_neg"][0], "both", Neg_V_args["verb_neg"][0]]+[x[0] for x in Neg_V_args["args"]])

                W = N[0] + " or " + N2[0] + " " + VP
                S = N[0] + " and " + N2[0] + " " + VP
                notW = "neither " + N[0] + " nor " + N2[0] + " " + VP
                notS = N[0] + " and " + N2[0] + " " + negVP

            else:
                """connectives in object position"""
                V = choice(all_transitive_verbs)
                bareV = get_all_conjunctive([("expression", V[0]), ("bare", "1")])
                DP1 = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", all_nouns)), allow_quantifiers=False)

                # always generate plural verbs & nouns to avoid agreement issues with "and"
                V = choice(self.all_plural_verbs)
                N1 = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", all_plural_nouns)), allow_quantifiers=False)
                if N1["animate"] == "0":
                    N2 = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns), [N1]), allow_quantifiers=False)
                else:
                    N2 = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", all_plural_animate_nouns), [N1]), allow_quantifiers=False)

                # else:
                #     """singular members"""
                #     V = choice(self.all_singular_verbs)
                #     N1 = choice(get_matches_of(V, "arg_1", all_singular_nouns))
                #     if N1["animate"] == "0":
                #         N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns), [N1])
                #     else:
                #         N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns), [N1])

                V_args = verb_args_from_verb(V, subj=N1, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)

                W = " ".join([DP1[0], V_args["aux"][0], V_args["verb"][0], N1[0], "or", N2[0]])
                S = " ".join([DP1[0], V_args["aux"][0], V_args["verb"][0], N1[0], "and", N2[0]])
                notW = " ".join([DP1[0], V_args["aux"][0], V_args["verb"][0], "neither", N1[0],"nor", N2[0]])
                notS = " ".join([DP1[0], Neg_V_args["aux_neg"][0], "both", Neg_V_args["verb_neg"][0], "both", N1[0], "and", N2[0]])

        elif w =="can":
            trigger = "modal"
            position = "NA"
            V = choice(get_all("bare", "1", all_verbs))
            N = choice(get_matches_of(V, "arg_1", all_nouns))
            DP = N_to_DP_mutate(N, allow_quantifiers=False)
            v_args = verb_args_from_verb(V, subj=N, allow_quantifiers=False)
            time = choice("past","pres")

            if time == "past":
                CAN = "could"
                CANT = "couldn't"
                HAVETO = "needed to"
                NOTHAVETO = "didn't need to"
            else:
                CAN = "can"
                CANT = "can't"
                HAVETO = "need to"
                if N("sg") == 1:
                    NOTHAVETO = "doesn't need to"
                else:
                    NOTHAVETO = "don't need to"

            VP = " ".join([V[0]] +
                          [x[0] for x in v_args["args"]])

            W = DP[0]+" "+CAN+" "+VP
            S = DP[0]+" "+HAVETO+" "+VP
            notW = DP[0]+" "+CANT+" "+VP
            notS = DP[0]+" "+NOTHAVETO+" "+VP

        elif w == "adj":
            trigger = "adjective"
#TODO: remove universal quantifiers


            scal_adjs_an=(("smart","brilliant"),("big","enourmous"))#,["well-off","rich"],["good looking", "gorgeous"],["fine","great"],["fat","obese"]]
            scal_adjs_inan=(("good","excellent"),("big","enourmous"),("fine","great"))
            #scal_adjs_food={["good","excellent"],["tasty","delicious"],["warm","hot"]}
            adj_type=choice(["an","inan"])

            if adj_type=="an":
                N = choice(all_animate_nouns)
                adj_idx = choice(range(len(scal_adjs_an)))
                adj = scal_adjs_an[adj_idx]
            else:
                #inan_type=choice("inan","food")
                #TODO:ADD FOOD
                N = choice(all_inanimate_nouns)
                adj_idx = choice(range(len(scal_adjs_inan)))
                adj = scal_adjs_inan[adj_idx]
            print(adj)

                #if inan_type=="food":

                    #adjs = scalar_adjs_inan


            if N["sg"]=="1":
                BE=" is "
            else:
                BE=" are "

            DP = N_to_DP_mutate(N, allow_quantifiers=False)

            W_adj = adj[0]
            S_adj = adj[1]
            W = DP[0]+BE+W_adj
            S = DP[0]+BE+S_adj
            notW = DP[0]+BE+"not "+W_adj
            notS = DP[0]+BE+ "not " + S_adj

            lexemes = W_adj + "-" + S_adj

        elif w=="verb":
            trigger = "verb"
            scal_verbs=[["ran", "sprinted"],["went towards","got to"]]
            N = choice(all_animate_nouns)
            DP = N_to_DP_mutate(N, allow_quantifiers=False)
            V_idx = random.choice([0,1,2])
            location = choice(get_all_conjunctive([("category", "N"), ("locale", "1")]))
            DP_loc = (N_to_DP_mutate(location, allow_quantifiers=False))[0]

            if V_idx==0:
                lexemes = "ran - sprinted"
                VP_type=choice(["bare","prep"])

                if VP_type == "bare":
                    W= DP[0]+" ran"
                    S= DP[0]+" sprinted"
                    notW= DP[0]+" did not run"
                    notS=DP[0]+" did not sprint"
                else:
                    W= DP[0]+" ran to "+DP_loc
                    S= DP[0]+" sprinted to "+DP_loc
                    notW= DP[0]+" did not run to "+DP_loc
                    notS=DP[0]+" did not sprint to "+DP_loc

            elif V_idx==1:
                lexemes = "went towards - got to"

                W = N[0] + " went towards "+DP_loc
                S = N[0] + " got to "+DP_loc
                notW = N[0] + " did not go towards "+DP_loc
                notS = N[0] + " did not get to "+DP_loc

            elif V_idx==2:
                lexemes = "tried - managed"
                v_args = verb_args_from_verb(self.managed, N)
                VP = join_args(v_args["args"])
                W = " ".join([N[0], self.tried[0], VP])
                S = " ".join([N[0], self.managed[0], VP])
                notW = " ".join([N[0], "did not try", VP])
                notS = " ".join([N[0], "did not manage", VP])

        C1 = [[W, notS], ["neutral", "entailment", "implicature_PtoN", "target"]]
        #C2 = [(C1[0])[::-1], ["neutral", "entailment", "implicature_NtoP", "target"]]
        C3= [[W,S], ["neutral", "contradiction", "negated implicature_P", "target"]]
        C4= [(C3[0])[::-1], ["entailment", "contradiction","reverse negated implicature_P", "target"]]
        #C5= [[notS,notW], ["neutral", "contradiction", "negated implicature_N", "target"]]
        #C6 = [(C5[0])[::-1], ["entailment", "contradiction","reverse negated implicature_N", "target"]]

        C7 = [[S,notW], ["contradiction", "contradiction", "opposite", "control"]]
        C8 = [(C7[0])[::-1], ["contradiction", "contradiction", "opposite", "control"]]
        C9 = [[W,notW], ["contradiction", "contradiction", "negation","control"]]
        C10 = [(C9[0])[::-1], ["contradiction", "contradiction", "negation","control"]]
        C11 = [[S,notS], ["contradiction", "contradiction", "negation","control"]]
        C12 = [(C11[0])[::-1], ["contradiction", "contradiction", "negation","control"]]

        if w=="two" or w =="ten":
            C2 = [(C1[0])[::-1], ["neutral", "neutral", "no_impl", "target"]]
            C5 = [[notS, notW], ["neutral", "neutral", "no_impl", "target"]]
            C6 = [(C5[0])[::-1], ["entailment", "neutral", "no_impl", "target"]]

        else:
            C2 = [(C1[0])[::-1], ["neutral", "entailment", "implicature_NtoP", "target"]]
            C5 = [[notS, notW], ["neutral", "contradiction", "negated implicature_N", "target"]]
            C6 = [(C5[0])[::-1], ["entailment", "contradiction", "reverse negated implicature_N", "target"]]

        if lexemes == "":
            lexemes = self.w + " - " + self.s
        C_set = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12]
        data = []
        track_sentence = C1[0]

        for i in range(12):
            C = (C_set[i])[0]
            metadata = C_set[i][1]
            sentence_pair = {
                "sentence1": "%s." % (C[0]),
                "sentence2": "%s." % (C[1]),
                "gold_label_log": metadata[0],
                "gold_label_prag": metadata[1],
                "spec_relation": metadata[2],
                "item_type": metadata[3],
                "trigger": trigger,
                #"position": position
                "lexemes": lexemes
            }
            data.append(sentence_pair)
        return data, track_sentence



#200
generator = SIGenerator("some", "all")
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/IMPPRES/implicature/quantifiers.jsonl")

#200
generator = SIGenerator("or", "and")
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/IMPPRES/implicature/connectives.jsonl")

#100
generator = SIGenerator("can", "have to")
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/IMPPRES/implicature/modals.jsonl")

#100
generator = SIGenerator("two", "three")
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/IMPPRES/implicature/numerals_2_3.jsonl")

#100
generator = SIGenerator("ten", "one hundred")
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/IMPPRES/implicature/numerals_10_100.jsonl")

#200
generator = SIGenerator("adj", "adj")
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/IMPPRES/implicature/gradable_adjective.jsonl")

#200
generator = SIGenerator("verb", "verb")
generator.generate_paradigm(number_to_generate=10, rel_output_path="outputs/IMPPRES/implicature/gradable_verb.jsonl")
