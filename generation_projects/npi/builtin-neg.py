# Authors: Anna Alsop
# Script for generating NPI sentences with predicates with built-in negation as licensors

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=builtin-neg.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# generate sentences for "ever"

# set total number of paradigms to generate
number_to_generate = 100
sentences = set()

# gather word classes that will be accessed frequently
# PITFALL:
# ever doesn't occur with progressive
# Every boy who has ever eaten a potato is tall.
# *? Every boy who is ever eating a potato is tall.

# PITFALL #2:
# ever occurs after auxiliary "do"
# The boy rarely ever did say that the girl wears jeans.
# * The boy rarely did ever say that the girl wears jeans.

all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
# all non-NPI licensing embedding verbs
all_embedding_verbs = get_all_conjunctive([("category_2", "V_embedding"), ("finite", "1")])
all_non_progressive_embedding_verbs = get_all("ing", "0", all_embedding_verbs)
# all built-in negation NPI licensors
all_embedding_neg_items = np.append(get_all("category_2", "V_neg"),
                                    np.append(get_all("category_2", "Adj_neg"), get_all("category_2", "P_neg")))
# NPI licensing embedding verbs with a subject in the embedded clause
neg_verbs_embedded_subject = np.append(get_all_conjunctive([("category_2", "V_neg"), ("category", "(S\\NP)/(S\\NP)")]),
                                       get_all_conjunctive([("category_2", "V_neg"), ("category", "(S\\NP)/(S[from]\\NP)")]))
non_progressive_neg_verbs_embedded_subject = get_all("ing", "0", neg_verbs_embedded_subject)
# NPI licensing adjectives
all_neg_adjectives = get_all("category_2", "Adj_neg")
# All NPI items with subject in embedded clause (Adjectives + verbs)
neg_items_embedded_subject = np.append(neg_verbs_embedded_subject, all_neg_adjectives)
# NPI licensing prepositions (e.g. without)
all_neg_prepositions = get_all("category_2", "P_neg")
# Embedders (Cs/Ps: that, from) used with embedding verbs
all_embedders = np.append(get_all("expression", "that"), get_all("expression", "from"))
all_nouns = get_all("category", "N")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # doubt: (V1 simple past for simplicity)
    # D1    N1     (Aux1) V_neg   that D2    N2   ever/also V1   D3    N3
    # The/a person (has)  doubted that the/a girl ever/also sang the/a song.

    # regret: (V1 must be simple past)
    # D1    N1     (Aux1) V_neg  that D2    N2   ever/also V1   D3    N3
    # The/a person (did)  regret that the/a girl ever/also sang the/a song.

    # prevent: (V1 must be -ing)
    # D1    N1     (Aux1) V_neg     D2    N2   from ever/also V1      D3    N3
    # The/a person (had)  prevented the/a girl from ever/also singing the/a song.

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    V1_non_neg = choice(get_matched_by(N1, "arg_1", all_non_progressive_embedding_verbs))
    # same tense on both verbs
    V1_neg_options = get_matched_by(N1, "arg_1", non_progressive_neg_verbs_embedded_subject)
    V1_neg = choice(np.array(list(filter(lambda x: x["finite"] == V1_non_neg["finite"] and
                                                   x["bare"] == V1_non_neg["bare"] and
                                                   x["pres"] == V1_non_neg["pres"] and
                                                   x["past"] == V1_non_neg["past"] and
                                                   x["en"] == V1_non_neg["en"] and
                                                   x["3sg"] == V1_non_neg["3sg"],
                                                    V1_neg_options)), dtype=data_type))
    Aux1 = return_aux(V1_non_neg, N1, allow_negated=False)
    Embedder_non_neg = choice(get_matched_by(V1_non_neg, "arg_2", all_embedders))
    Embedder_neg = choice(get_matched_by(V1_neg, "arg_2", all_embedders) if V1_neg["category"] == "(S\\NP)/(S\\NP)" else get_matched_by(V1_neg, "arg_3", all_embedders))
    N2 = choice(all_animate_nouns)
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    V2_non_neg = choice(get_matches_of_conj([(N2, "arg_1"),(V1_non_neg, "arg_clause")], all_non_progressive_transitive_verbs))
    V2_neg = choice(get_matches_of_conj([(N2, "arg_1"), (V1_neg, "arg_clause")], all_non_progressive_transitive_verbs))
    N3_non_neg = choice(get_matches_of(V2_non_neg, "arg_2", all_nouns))
    N3_neg = choice(get_matches_of(V2_neg, "arg_2", all_nouns))
    D3_non_neg = choice(get_matched_by(N3_non_neg, "arg_1", all_common_dets))
    D3_neg = choice(get_matched_by(N3_neg, "arg_1", all_common_dets))

    # check for do/does/did for both aux verbs, make the aux directly adjacent to verb.
    if Aux1[0] in ["do", "does", "did"]:
        Aux1_final = ""
        V1_non_neg_final = Aux1[0] + " " + V1_non_neg[0]
        V1_neg_final = Aux1[0] + " " + V1_neg[0]
    else:
        Aux1_final = Aux1[0]
        V1_non_neg_final = V1_non_neg[0]
        V1_neg_final = V1_neg[0]

    # check for prevent; make "from" after D2 N2.
    if Embedder_neg[0] == "from":
        Embedder_neg_final = ""
        N2_neg = N2[0] + " " + Embedder_neg[0]
    else:
        Embedder_neg_final = Embedder_neg[0]
        N2_neg = N2[0]

    # D1    N1     (Aux1) V_neg  that D2    N2   ever/also V1   D3    N3
    # The/a person (did)  regret that the/a girl ever/also sang the/a song.

    # build sentences with non-neg verb
    sentence_1 = "%s %s %s %s %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_non_neg_final, Embedder_non_neg[0], D2[0], N2[0], V2_non_neg[0], D3_non_neg[0], N3_non_neg[0])
    sentence_2 = "%s %s %s %s %s %s %s also %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_non_neg_final, Embedder_non_neg[0], D2[0], N2[0], V2_non_neg[0], D3_non_neg[0], N3_non_neg[0])
    sentence_3 = "%s %s %s ever %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_non_neg_final, Embedder_non_neg[0], D2[0], N2[0], V2_non_neg[0], D3_non_neg[0], N3_non_neg[0])
    sentence_4 = "%s %s %s also %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_non_neg_final, Embedder_non_neg[0], D2[0], N2[0], V2_non_neg[0], D3_non_neg[0], N3_non_neg[0])

    # build sentences with neg verb
    sentence_5 = "%s %s %s %s %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_neg_final, Embedder_neg_final, D2[0], N2_neg, V2_neg[0], D3_neg[0], N3_neg[0])
    sentence_6 = "%s %s %s %s %s %s %s also %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_neg_final, Embedder_neg_final, D2[0], N2_neg, V2_neg[0], D3_neg[0], N3_neg[0])
    sentence_7 = "%s %s %s ever %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_neg_final, Embedder_neg_final, D2[0], N2_neg, V2_neg[0], D3_neg[0], N3_neg[0])
    sentence_8 = "%s %s %s also %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_neg_final, Embedder_neg_final, D2[0], N2_neg, V2_neg[0], D3_neg[0], N3_neg[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)
    sentence_5 = remove_extra_whitespace(sentence_5)
    sentence_6 = remove_extra_whitespace(sentence_6)
    sentence_7 = remove_extra_whitespace(sentence_7)
    sentence_8 = remove_extra_whitespace(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have non-licensing item
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=0_scope=1_npi-present=1" % V1_non_neg[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=0_scope=1_npi-present=0" % V1_non_neg[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=0_scope=0_npi-present=1" % V1_non_neg[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=0_scope=0_npi-present=0" % V1_non_neg[0], 1, sentence_4))

        # sentences 5-8 have built-in negation licensing item
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=1_scope=1_npi-present=1" % V1_neg[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=1_scope=1_npi-present=0" % V1_neg[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=1_scope=0_npi-present=1" % V1_neg[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=builtin-neg_npi=ever_neg-item=%s_licensor=1_scope=0_npi-present=0" % V1_neg[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "ever"

# repeat for "any"