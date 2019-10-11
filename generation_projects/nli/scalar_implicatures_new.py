from utils import data_generator
from utils.conjugate import *
from utils.constituent_building import *
from utils.string_utils import string_beautify
from utils.vocab_sets import *
from utils import jsonlines
import logging
import datetime
import traceback


class SIGenerator(data_generator.NLIGenerator):
    def __init__(self, w, s):
        super().__init__(
            uid="scalar_implicatures"
        )

        self.all_plural_verbs = get_all("3sg", "0", all_verbs)
        self.all_singular_verbs = get_all("3sg", "1", all_verbs)
        self.all_plural_inanimate_nouns = np.intersect1d(all_inanimate_nouns, all_plural_nouns)

        self.w = w
        self.s = s

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

        if w=="some":


            trigger = "quantifier"
            position = choice(["subject","object"])
            #position = "object"
            #print(position)
            if position=="subject":
                """quantifiers in subject position"""



                V = choice(self.all_plural_verbs)


                N = choice(get_matches_of(V, "arg_1", all_plural_nouns))


                v_args = verb_args_from_verb(V, subj=N)

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
                N2 = choice(get_matches_of(V, "arg_2", all_plural_nouns), [N1])

                V_args = verb_args_from_verb(V, subj=N1, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)

                #Aux = return_aux(V, N1, allow_negated=False)
                #print(Aux)




                # W = " ".join([DP1[0],Aux[0],V[0],"some ",N2[0]])
                # S = " ".join([DP1[0],Aux[0],V[0],"all ",N2[0]])
                # notW = " ".join([DP1[0],Aux[0],V[0],"no ",N2[0]])
                # notS = " ".join([DP1[0],Aux[0],"not",bareV[0],"all",N2[0]])

                W = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],"some ",N2[0]])
                S = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],"all ",N2[0]])
                notW = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],"no ",N2[0]])
                notS = " ".join([DP1[0],Neg_V_args["aux_neg"][0], Neg_V_args["verb_neg"][0],"all",N2[0]])

        elif w=="three" or w =="two":


            trigger = "numeral_"+w+"-"+s
            position = choice(["subject","object"])
            #position = "object"

            if position=="subject":
                """numerals in subject position"""



                V = choice(self.all_plural_verbs)




                N = choice(get_matches_of(V, "arg_1", all_plural_nouns))


                V_args = verb_args_from_verb(V, subj=N)
                Neg_V_args = negate_V_args(V_args)


                Aux = return_aux(V, N, allow_negated=False)

                VP = " ".join([Aux[0],
                               V[0]] +
                              [x[0] for x in v_args["args"]])
                negVP = " ".join([Neg_V_args["aux_neg"][0],
                                  Neg_V_args["verb_neg"][0]] +
                              [x[0] for x in Neg_v_args["args"]])


                W = w+N[0]+" "+VP
                S = s+N[0]+" "+VP
                notW = w+N[0]+" "+negVP
                notS = s+N[0]+" "+negVP


            else:
                """numerals in object position"""

                V = choice(all_transitive_verbs)

                N1 = choice(get_matches_of(V, "arg_1", all_nouns))
                DP1= N_to_DP_mutate(N1)
                #print(DP1[0])
                N2 = choice(get_matches_of(V, "arg_2", all_plural_nouns), [N1])

                V_args = verb_args_from_verb(V, subj=N1, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)

                #Aux = return_aux(V, N1, allow_negated=False)
                #print(Aux)




                # W = " ".join([DP1[0],Aux[0],V[0],"some ",N2[0]])
                # S = " ".join([DP1[0],Aux[0],V[0],"all ",N2[0]])
                # notW = " ".join([DP1[0],Aux[0],V[0],"no ",N2[0]])
                # notS = " ".join([DP1[0],Aux[0],"not",bareV[0],"all",N2[0]])

                W = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],w,N2[0]])
                S = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],s,N2[0]])
                notW = " ".join([DP1[0],Neg_V_args["aux_neg"][0], Neg_V_args["verb_neg"][0],w,N2[0]])
                notS = " ".join([DP1[0],Neg_V_args["aux_neg"][0], Neg_V_args["verb_neg"][0],s,N2[0]])


        elif w=="or":
            trigger = "connective"
            position = choice("subject","object")

            if position=="subject":
                """connectives in subject position"""



                x=choice([0,1])

                if x == 0:
                    """plural members"""

                    V = choice(self.all_plural_verbs)
                    N = choice(get_matches_of(V, "arg_1", all_plural_nouns))
                    if N["animate"]=="0":
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns), [N])
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns), [N])

                else:
                    """singular members"""

                    V = choice(self.all_singular_verbs)
                    N = choice(get_matches_of(V, "arg_1", all_singular_nouns))
                    if N["animate"]=="0":
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns), [N])
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns), [N])

                #print(V[0], V["pres"], V["past"])




                V_args = verb_args_from_verb(V, subj=N, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)

                #Aux = return_aux(V, N, allow_negated=False)


                VP = " ".join([V_args["aux"][0], V_args["verb"][0]]+[x[0] for x in V_args["args"]])
                negVP = " ".join([Neg_V_args["aux_neg"][0], "both", Neg_V_args["verb_neg"][0]]+[x[0] for x in Neg_V_args["args"]])

                #print("here1")

                # if V["past"] == "1":
                #     DO = "did"
                # elif V["pres"]=="1":
                #         DO= "do"



                # if V["pres"]=="1" or V["past"]=="1" :
                #
                #     #print("here3")
                #     negVP =  " ".join([DO+" not both "+ bareV[0]] +
                #                 [x[0] for x in v_args["args"]])
                #
                #
                #     #print("here3b")
                #
                #
                # else:
                #
                #
                #     #print("here4")
                #     negVP =  " ".join([Aux[0]," not both ",
                #                V[0]] +
                #               [x[0] for x in v_args["args"]])
                #     #print("here4b")


                W = N[0] + " or " + N2[0] + " " + VP
                S = N[0] + " and " + N2[0] + " " + VP

                notW = "neither " + N[0] + " nor " + N2[0] + " " + VP

                notS = N[0] + " and " + N2[0] + " " + negVP


            else:
                """connectives in object position"""

                V = choice(all_transitive_verbs)
                bareV = get_all_conjunctive([("expression", V[0]), ("bare", "1")])

                N = choice(get_matches_of(V, "arg_1", all_nouns))
                DP1= N_to_DP_mutate(N)


                x = choice([0, 1])

                if x == 0:
                    """plural members"""

                    V = choice(self.all_plural_verbs)
                    N1 = choice(get_matches_of(V, "arg_1", all_plural_nouns))
                    if N1["animate"] == "0":
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns), [N1])
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns), [N1])

                else:
                    """singular members"""

                    V = choice(all_singular_verbs)
                    N1 = choice(get_matches_of(V, "arg_1", all_singular_nouns))
                    if N1["animate"] == "0":
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns), [N1])
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns), [N1])



                # Aux = return_aux(V, N, allow_negated=False)
                #
                # if V["pres"]==1:
                #     NAux=("do",None)
                # elif V["past"]==1:
                #     NAux=("did",None)
                # else:
                #     NAux = return_aux(V, N, allow_negated=False)

                V_args = verb_args_from_verb(V, subj=N, allow_negated=False)
                Neg_V_args = negate_V_args(V_args)

                W = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],N1[0], "or", N2[0]])
                S = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],N1[0], "and", N2[0]])
                notW = " ".join([DP1[0],V_args["aux"][0], V_args["verb"][0],"neither", N1[0],"nor", N2[0]])
                notS = " ".join([DP1[0],Neg_V_args["aux_neg"][0], "both", Neg_V_args["verb_neg"][0],"both",N1[0], "and", N2[0]])





                #Aux = return_aux(V, N, allow_negated=False)


                #print("here1")

                # if V["past"] == "1":
                #     DO = "did"
                # elif V["pres"]=="1":
                #         DO= "do"





            #print("here6")

        elif w =="can":
            trigger="modal"
            position="NA"

            #print("A")


            V=choice(get_all("bare","1",all_verbs))


            N = choice(get_matches_of(V, "arg_1", all_nouns))
            DP = N_to_DP_mutate(N)


            v_args = verb_args_from_verb(V, subj=N)

            time = choice("past","pres")

            if time=="past":
                CAN="could"
                CANT="couldn't"
                HAVETO="needed to"
                NOTHAVETO="didn't need to"
            else:
                CAN="can"
                CANT="can't"
                HAVETO="need to"
                if N("sg")==1:
                    NOTHAVETO="doesn't need to"
                else:
                    NOTHAVETO = "don't need to"
            #print("B")

            VP = " ".join([V[0]] +
                          [x[0] for x in v_args["args"]])


            W = DP[0]+" "+CAN+" "+VP
            S = DP[0]+" "+HAVETO+" "+VP
            notW = DP[0]+" "+CANT+" "+VP
            notS = DP[0]+" "+NOTHAVETO+" "+VP

        elif w=="adj":
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

            DP = N_to_DP_mutate(N)

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
            DP = N_to_DP_mutate(N)
            V_idx = choice(0,1)
            location = choice(get_all_conjunctive([("category", "N"), ("locale", "1")]))
            DP_loc = (N_to_DP_mutate(location))[0]

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

            else:
                lexemes = "went towards - got to"

                W = N[0] + " went towards "+DP_loc
                S = N[0] + " got to "+DP_loc
                notW = N[0] + " did not go towards "+DP_loc
                notS = N[0] + " did not get to "+DP_loc








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

        if w=="three" or w =="two":
            C2 = [(C1[0])[::-1], ["neutral", "neutral", "no_impl", "target"]]
            C5 = [[notS, notW], ["neutral", "neutral", "no_impl", "target"]]
            C6 = [(C5[0])[::-1], ["entailment", "neutral", "no_impl", "target"]]



        else:
            C2 = [(C1[0])[::-1], ["neutral", "entailment", "implicature_NtoP", "target"]]
            C5 = [[notS, notW], ["neutral", "contradiction", "negated implicature_N", "target"]]
            C6 = [(C5[0])[::-1], ["entailment", "contradiction", "reverse negated implicature_N", "target"]]

        C_set = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12]


        #print("here8")

        data=[]

        track_sentence = C1[0]








#        print("here9")
        for i in range(12):

            C = (C_set[i])[0]
            metadata = C_set[i][1]



            sentence_pair = {
                "sentence_1": "%s." % (C[0]),
                "sentence_2": "%s." % (C[1]),
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

    def log_exception(self, e):
        logging.debug("".join(traceback.format_tb(e.__traceback__)) + str(e) + "\n")

    def generate_paradigm(self, number_to_generate=12, rel_output_path=None, absolute_path=None):
        if rel_output_path is not None:
            project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
            output = open(os.path.join(project_root, rel_output_path), "a")

        elif absolute_path is not None:
            output = open(absolute_path, "w")
        else:
            raise Exception("You need to give an output path")
        past_sentences = []
        generated_data = []
        constant_data = self.make_metadata_dict()
        #print(len(past_sentences))

        while len(past_sentences) < number_to_generate:

            try:
                new_data, track_sentence = self.sample()
                print(track_sentence)

                if track_sentence not in past_sentences:

                    past_sentences.append(track_sentence)


                    for C in new_data:
                        for field in self.data_fields:
                            if field in C:
                                C[field] = string_beautify(C[field])
                                C.update(constant_data)
                        generated_data.append(C)
            except Exception as e:
                self.log_exception(e)
        jsonlines.Writer(output).write_all(generated_data)



#generator = SIGenerator("some","all")
#generator.generate_paradigm(number_to_generate=5, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

#generator = SIGenerator("or","and")
#generator.generate_paradigm(number_to_generate=200, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

#generator = SIGenerator("can", "have to")
#generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

#generator = SIGenerator("two","three")
#generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

#generator = SIGenerator("three","four")
#generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

#generator = SIGenerator("adj","adj")
#generator.generate_paradigm(number_to_generate=200, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

generator = SIGenerator("verb","verb")
generator.generate_paradigm(number_to_generate=1, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
