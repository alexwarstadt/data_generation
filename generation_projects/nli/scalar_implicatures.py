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
        self.all_plural_inanimate_nouns = np.intersect1d(self.all_inanimate_nouns, self.all_plural_nouns)


        self.w = w
        self.s = s

    #def get_bare(self,V):
     #   bare = get_all_conjunctive(("expression",V),("bare","1"))
      #  return bare

    def sample(self):



        w = self.w
        s = self.s

        V = choice(self.all_plural_verbs)
        bare = get_bare(V)
        #print(bare)
        #bare = get_all_conjunctive([("expression",V[0]),("bare","1")])
        #print(bare[0])

        if w=="some":


            type = "quantifier"
            position = choice(["subject","object"])
            #position = "object"
            print(position)
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
                N2 = choice(get_matches_of(V, "arg_2", all_plural_nouns))


                Aux = return_aux(V, N1, allow_negated=False)
                #print(Aux)

                bareV = get_all_conjunctive([("expression", V[0]), ("bare", "1")])
                print(V)
                print(bareV)


                W = " ".join([DP1[0],Aux[0],V[0],"some ",N2[0]])
                S = " ".join([DP1[0],Aux[0],V[0],"all ",N2[0]])
                notW = " ".join([DP1[0],Aux[0],V[0],"no ",N2[0]])
                notS = " ".join([DP1[0],Aux[0],"not",bareV[0],"all",N2[0]])


        elif w=="or":
            type= "connective"
            position = choice("subject","object")

            if position=="subject":
                """connectives in subject position"""



                x=choice([0,1])

                if x == 0:
                    """plural members"""

                    V = choice(self.all_plural_verbs)
                    N = choice(get_matches_of(V, "arg_1", all_plural_nouns))
                    if N["animate"]=="0":
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns))
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns))

                else:
                    """singular members"""

                    V = choice(all_singular_verbs)
                    N = choice(get_matches_of(V, "arg_1", all_singular_nouns))
                    if N["animate"]=="0":
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns))
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns))

                #print(V[0], V["pres"], V["past"])


                v_args = verb_args_from_verb(V, subj=N)

                bareV = get_all_conjunctive([("expression", V[0]), ("bare", "1")])

                Aux = return_aux(V, N, allow_negated=False)


                VP = " ".join([Aux[0],
                               V[0]] +
                              [x[0] for x in v_args["args"]])

                #print("here1")

                if V["past"] == "1":
                    DO = "did"
                elif V["pres"]=="1":
                        DO= "do"





                if V["pres"]=="1" or V["past"]=="1" :

                    #print("here3")
                    negVP =  " ".join([DO+" not both "+ bareV[0]] +
                                [x[0] for x in v_args["args"]])


                    #print("here3b")


                else:


                    #print("here4")
                    negVP =  " ".join([Aux[0]," not both ",
                               V[0]] +
                              [x[0] for x in v_args["args"]])
                    #print("here4b")


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
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns))
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns))

                else:
                    """singular members"""

                    V = choice(all_singular_verbs)
                    N1 = choice(get_matches_of(V, "arg_1", all_singular_nouns))
                    if N1["animate"] == "0":
                        N2 = choice(get_matches_of(V, "arg_1", self.all_plural_inanimate_nouns))
                    else:
                        N2 = choice(get_matches_of(V, "arg_1", all_plural_animate_nouns))

                Aux = return_aux(V, N, allow_negated=False)

                if V["pres"]==1:
                    NAux=("do",None)
                elif V["past"]==1:
                    NAux=("did",None)
                else:
                    NAux = return_aux(V, N, allow_negated=False)


                W = " ".join([DP1[0],Aux[0],V[0],N1[0], "or", N2[0]])
                S = " ".join([DP1[0],Aux[0],V[0],N1[0], "and", N2[0]])
                notW = " ".join([DP1[0],Aux[0],"neither", N1[0],"nor", N2[0]])
                notS = " ".join([DP1[0],NAux[0],"not",bareV[0],"both",N1[0], "and", N2[0]])




            #print("here6")

        elif w =="can":
            type="modal"
            position="position"

            #print("A")


            V=choice(get_all("bare","1",all_verbs))


            N = choice(get_matches_of(V, "arg_1", all_nouns))
            DP = N_to_DP_mutate(N)


            v_args = verb_args_from_verb(V, subj=N)

            time = choice("past","pres")

            if time=="past":
                CAN="could"
                CANT="couldn't"
                HAVETO="had to"
                NOTHAVETO="didn't have to"
            else:
                CAN="can"
                CANT="can't"
                HAVETO="have to"
                if N("sg")==1:
                    NOTHAVETO="doesn't have to"
                else:
                    NOTHAVETO = "don't have to"
            #print("B")

            VP = " ".join([V[0]] +
                          [x[0] for x in v_args["args"]])


            W = DP[0]+" "+CAN+" "+VP
            S = DP[0]+" "+HAVETO+" "+VP
            notW = DP[0]+" "+CANT+" "+VP
            notS = DP[0]+" "+NOTHAVETO+" "+VP

        #print("here7")
        C1 = [[W, notS], ["neutral", "entailment"]]
        C2 = [(C1[0])[::-1], ["neutral", "entailment"]]
        C3= [[W,S], ["neutral", "contradiction"]]
        C4= [(C3[0])[::-1], ["entailment", "contradiction"]]
        C5= [[notS,notW], ["neutral", "contradiction"]]

        C6 = [(C5[0])[::-1], ["entailment", "contradiction"]]
        C7 = [[S,notW], ["contradiction", "contradiction"]]
        C8 = [(C7[0])[::-1], ["contradiction", "contradiction"]]
        C9 = [[W,notW], ["contradiction", "contradiction"]]
        C10 = [(C9[0])[::-1], ["contradiction", "contradiction"]]
        C11 = [[S,notS], ["contradiction", "contradiction"]]
        C12 = [(C11[0])[::-1], ["contradiction", "contradiction"]]

        C_set = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12]


        #print("here8")

        data=[]

        track_sentence = C1[0]



        print("here9")
        for i in range(12):

            C = (C_set[i])[0]
            metadata = C_set[i][1]


            sentence_pair = {
                "sentence_1": "%s." % (C[0]),
                "sentence_2": "%s." % (C[1]),
                "gold_label_log": metadata[0],
                "gold_label_prag": metadata[1],
                "type": type,
                "position": position
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

            #try:
                new_data, track_sentence = self.sample()


                if track_sentence not in past_sentences:
                    print("hi")
                    past_sentences.append(track_sentence)

                    print(past_sentences)

                    for C in new_data:
                        for field in self.data_fields:
                            if field in C:
                                C[field] = string_beautify(C[field])
                                C.update(constant_data)
                        generated_data.append(C)
           # except Exception as e:
            #    self.log_exception(e)
        jsonlines.Writer(output).write_all(generated_data)



generator = SIGenerator("some","all")
generator.generate_paradigm(number_to_generate=1, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

# generator = SIGenerator("or","and")
# generator.generate_paradigm(number_to_generate=0, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)
#
#
# generator = SIGenerator("can", "have to")
# generator.generate_paradigm(number_to_generate=0, rel_output_path="outputs/nli/%s.jsonl" % generator.uid)

