# Authors: Alex Warstadt
# Script for generating NPI sentences with quantifiers as licensors

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=quantifiers.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_quantifiers = get_all("category", "(S/(S\\NP))/N")
all_UE_UE_quantifiers = get_all("restrictor_DE", "0", all_quantifiers)
all_DE_UE_quantifiers = get_all("restrictor_DE", "1", get_all("scope_DE", "0", all_quantifiers)) #TODO: FC any takes singulars
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who V1      any/the/D2    N2      V2    any/the/D3  N3
    # every  boy  who bought  any/the/some  apples  sang  any/the/a   song

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
    D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
    V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers))        # restrict to UE quantifiers, otherwise there could be another licensor
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    conjugate(V2, N1, allow_negated=False)
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers))

    # build sentences with UE quantifier
    sentence_1 = "%s %s who %s any %s %s %s %s ." % (D1_up[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s the %s %s %s %s ." % (D1_up[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s any %s ." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s the %s ." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])

    # build sentences with DE quantifier
    sentence_5 = "%s %s who %s any %s %s %s %s ." % (D1_down[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_6 = "%s %s who %s the %s %s %s %s ." % (D1_down[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s any %s ." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])
    sentence_8 = "%s %s who %s %s %s %s the %s ." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])

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
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=1_npi-present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=1_npi-present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=0_npi-present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=0_npi-present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=1_npi-present=1" % D1_down[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=1_npi-present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=0_npi-present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=0_npi-present=0" % D1_down[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# the end :)






# repeat for "ever"

# PITFALL:
# ever doesn't occur with progressive
# Every boy who has ever eaten a potato is tall.
# *? Every boy who is ever eating a potato is tall.
sentences = set()
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who  (Aux)  ever  V1      the  N2      V2    D2  N3
    # every  boy  who  (has)  ever  bought  the  apples  sang  a   song

    N1 = choice(all_animate_nouns)
    D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
    D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
    V1 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers))
    V2 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    Aux2 = return_aux(V2, N1, allow_negated=False)
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers))

    # the replacement for "ever" depends on the tense of the verb
    # if the auxiliary is empty (i.e. the main verb is finite), use the tense of the verb, else use the auxiliary
    if Aux1[0] == "":
        emb_adv = "now" if V1["pres"] == "1" else "once"
    else:
        emb_adv = "now" if Aux1["pres"] == "1" else "once"
    if Aux2[0] == "":
        matrix_adv = "now" if V2["pres"] == "1" else "once"
    else:
        matrix_adv = "now" if Aux2["pres"] == "1" else "once"



    sentence_1 = "%s %s who %s ever %s %s %s %s %s %s %s ." % (D1_up[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_up[0], N1[0], Aux1[0], emb_adv, V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s ever %s %s %s ." % (D1_up[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_up[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], matrix_adv, V2[0], D3[0], N3[0])

    sentence_5 = "%s %s who %s ever %s %s %s %s %s %s %s ." % (D1_down[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_6 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_down[0], N1[0], Aux1[0], emb_adv, V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s ever %s %s %s ." % (D1_down[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_8 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_down[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], matrix_adv, V2[0], D3[0], N3[0])

    # remove doubled up spaces (this is because of empty determiner AND EMPTY AUXILIARY).
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
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=1_npi-present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=1_npi-present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=0_npi-present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=0_npi-present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=1_npi-present=1" % D1_down[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=1_npi-present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=0_npi-present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=0_npi-present=0" % D1_down[0], 1, sentence_8))

    sentences.add(sentence_1)

output.close()