# Authors: Alex Warstadt
# Script for generating NPI sentences with quantifiers as licensors

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import string_beautify
# from random import choice
import numpy as np
from utils.randomize import choice

# initialize output file
rel_output_path = "outputs/npi/environment=quantifiers2.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 10
sentences = set()


# ========== GENERATE FOR ANY ===========
# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_quantifiers = get_all("category", "(S/(S\\NP))/N")
all_UE_UE_quantifiers = get_all("restrictor_DE", "0", all_quantifiers)
all_DE_UE_quantifiers = get_all("restrictor_DE", "1", get_all("scope_DE", "0", all_quantifiers))
all_DE_UE_quantifiers = np.setdiff1d(all_DE_UE_quantifiers, get_all("expression", "any"))
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
any_decoys = np.concatenate((get_all("expression", "the"), get_all_conjunctive([("expression", "that"), ("category_2", "D")]),
                         get_all("expression", "this"), get_all("expression", "these"), get_all("expression", "those")))
# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who V1      any/the/D2    N2      V2    any/the/D3  N3
    # every  boy  who bought  any/the/some  apples  sang  any/the/a   song

    # build all lexical items
    #TODO: throw in modifiers
    try:
        N1 = choice(all_animate_nouns)
        D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
        V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])       # restrict to UE quantifiers, otherwise there could be another licensor
        V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs), [V1])
        V2 = conjugate(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])
        any_decoy_N2 = choice(get_matched_by(N2, "arg_1", any_decoys))
        any_decoy_N3 = choice(get_matched_by(N3, "arg_1", any_decoys))
    except IndexError:
        print(N1[0], N2[0], V2[0])
        continue

    # build sentences with UE quantifier
    sentence_1 = "%s %s who %s any %s %s %s %s." % (D1_up[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], any_decoy_N2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s any %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], any_decoy_N3[0], N3[0])

    # build sentences with DE quantifier
    sentence_5 = "%s %s who %s any %s %s %s %s." % (D1_down[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_6 = "%s %s who %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], any_decoy_N2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s any %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])
    sentence_8 = "%s %s who %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], any_decoy_N3[0], N3[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)
    sentence_5 = string_beautify(sentence_5)
    sentence_6 = string_beautify(sentence_6)
    sentence_7 = string_beautify(sentence_7)
    sentence_8 = string_beautify(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=0-scope=1-npi_present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=0-scope=1-npi_present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=0-scope=0-npi_present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=0-scope=0-npi_present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=1-scope=1-npi_present=1" % D1_down[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=1-scope=1-npi_present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=1-scope=0-npi_present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=any-crucial_item=%s-licensor=1-scope=0-npi_present=0" % D1_down[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# the end :)






# ========== GENERATE FOR EVER ===========

# PITFALL:
# ever doesn't occur with progressive
# Every boy who has ever eaten a potato is tall.
# *? Every boy who is ever eating a potato is tall.

# PITFALL #2:
# ever occurs after auxiliary "do"
# The boy rarely ever did say that the girl wears jeans.
# * The boy rarely did ever say that the girl wears jeans.

sentences = set()
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who  (Aux)  ever  V1      the  N2      V2    D2  N3
    # every  boy  who  (has)  ever  bought  the  apples  sang  a   song
    try:
        N1 = choice(all_animate_nouns)
        D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
        V1 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers), [D1_down, D1_up])
        V2 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs), [V1])
        Aux2 = return_aux(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])
        decoy = choice(["often", "also", "obviously", "clearly", "fortunately"])
    except IndexError:
        print(N1[0], N2[0], V2[0])
        continue

    if Aux1[0] in ["do", "does", "did"]:
        Aux1_final = ""
        V1_final = Aux1[0] + " " + V1[0]
    else:
        Aux1_final = Aux1[0]
        V1_final = V1[0]

    if Aux2[0] in ["do", "does", "did"]:
        Aux2_final = ""
        V2_final = Aux2[0] + " " + V2[0]
    else:
        Aux2_final = Aux2[0]
        V2_final = V2[0]

    sentence_1 = "%s %s who %s ever %s %s %s %s %s %s %s." % (D1_up[0], N1[0], Aux1_final, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_2 = "%s %s who %s %s %s %s %s %s %s %s %s." % (D1_up[0], N1[0], Aux1_final, decoy, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s ever %s %s %s." % (D1_up[0], N1[0], Aux1_final, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s %s %s %s %s %s." % (D1_up[0], N1[0], Aux1_final, V1_final, D2[0], N2[0], Aux2_final, decoy, V2_final, D3[0], N3[0])

    sentence_5 = "%s %s who %s ever %s %s %s %s %s %s %s." % (D1_down[0], N1[0], Aux1_final, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_6 = "%s %s who %s %s %s %s %s %s %s %s %s." % (D1_down[0], N1[0], Aux1_final, decoy, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s ever %s %s %s." % (D1_down[0], N1[0], Aux1_final, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_8 = "%s %s who %s %s %s %s %s %s %s %s %s." % (D1_down[0], N1[0], Aux1_final, V1_final, D2[0], N2[0], Aux2_final, decoy, V2_final, D3[0], N3[0])

    # remove doubled up spaces (this is because of empty determiner AND EMPTY AUXILIARY).
    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)
    sentence_5 = string_beautify(sentence_5)
    sentence_6 = string_beautify(sentence_6)
    sentence_7 = string_beautify(sentence_7)
    sentence_8 = string_beautify(sentence_8)


    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=0-scope=1-npi_present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=0-scope=1-npi_present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=0-scope=0-npi_present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=0-scope=0-npi_present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=1-scope=1-npi_present=1" % D1_down[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=1-scope=1-npi_present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=1-scope=0-npi_present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=ever-crucial_item=%s-licensor=1-scope=0-npi_present=0" % D1_down[0], 1, sentence_8))

    sentences.add(sentence_1)



# ========== GENERATE FOR YET ===========

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who  V1      D2    N2      YET/decoy      V2    N3    YET/decoy
    # every  boy  who  bought  some  apples  yet/regularly  sang  song  yet/regularly

    # build all lexical items
    #TODO: throw in modifiers
    try:
        N1 = choice(all_animate_nouns)
        D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
        V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])       # restrict to UE quantifiers, otherwise there could be another licensor
        V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs), [V1])
        V2 = conjugate(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], N2[0], V2[0])
        continue

    # build sentences with UE quantifier
    sentence_1 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], "yet", V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "yet")
    sentence_4 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # build sentences with DE quantifier
    sentence_5 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], "yet", V2[0], D3[0], N3[0])
    sentence_6 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "yet")
    sentence_8 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)
    sentence_5 = string_beautify(sentence_5)
    sentence_6 = string_beautify(sentence_6)
    sentence_7 = string_beautify(sentence_7)
    sentence_8 = string_beautify(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=0-scope=1-npi_present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=0-scope=1-npi_present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=0-scope=0-npi_present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=0-scope=0-npi_present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=1-scope=1-npi_present=1" % D1_down[0], 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=1-scope=1-npi_present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=1-scope=0-npi_present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=yet-crucial_item=%s-licensor=1-scope=0-npi_present=0" % D1_down[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)
    
    
# ========== GENERATE FOR AT ALL ===========

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who  V1      D2    N2      YET/decoy      V2    N3    YET/decoy
    # every  boy  who  bought  some  apples  at all/regularly  sang  song  at all/regularly

    # build all lexical items
    #TODO: throw in modifiers
    try:
        N1 = choice(all_animate_nouns)
        D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
        V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])       # restrict to UE quantifiers, otherwise there could be another licensor
        V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs), [V1])
        V2 = conjugate(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], N2[0], V2[0])
        continue

    # build sentences with UE quantifier
    sentence_1 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], "at all", V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "at all")
    sentence_4 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # build sentences with DE quantifier
    sentence_5 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], "at all", V2[0], D3[0], N3[0])
    sentence_6 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "at all")
    sentence_8 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)
    sentence_5 = string_beautify(sentence_5)
    sentence_6 = string_beautify(sentence_6)
    sentence_7 = string_beautify(sentence_7)
    sentence_8 = string_beautify(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=0-scope=1-npi_present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=0-scope=1-npi_present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=0-scope=0-npi_present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=0-scope=0-npi_present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=1-scope=1-npi_present=1" % D1_down[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=1-scope=1-npi_present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=1-scope=0-npi_present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=atall-crucial_item=%s-licensor=1-scope=0-npi_present=0" % D1_down[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)




# ========== GENERATE FOR IN YEARS ===========

sentences = set()
all_past_or_perfect_verbs = np.union1d(get_all("past", "1", all_transitive_verbs), get_all("en", "1", all_transitive_verbs))
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who  V1      D2    N2      in years/decoy      V2    N3    in years/decoy
    # every  boy  who  bought  some  apples  in years/regularly  sang  song  in years/regularly

    # build all lexical items
    #TODO: throw in modifiers
    try:
        N1 = choice(all_animate_nouns)
        D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
        V1 = choice(get_matched_by(N1, "arg_1", all_past_or_perfect_verbs))
        V1 = conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])       # restrict to UE quantifiers, otherwise there could be another licensor
        V2 = choice(get_matched_by(N1, "arg_1", all_past_or_perfect_verbs), [V1])
        V2 = conjugate(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], N2[0], V2[0])
        continue

    # build sentences with UE quantifier
    sentence_1 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], "in years", V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "in years")
    sentence_4 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # build sentences with DE quantifier
    sentence_5 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], "in years", V2[0], D3[0], N3[0])
    sentence_6 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "in years")
    sentence_8 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)
    sentence_5 = string_beautify(sentence_5)
    sentence_6 = string_beautify(sentence_6)
    sentence_7 = string_beautify(sentence_7)
    sentence_8 = string_beautify(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=0-scope=1-npi_present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=0-scope=1-npi_present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=0-scope=0-npi_present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=0-scope=0-npi_present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=1-scope=1-npi_present=1" % D1_down[0], 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=1-scope=1-npi_present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=1-scope=0-npi_present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=inyears-crucial_item=%s-licensor=1-scope=0-npi_present=0" % D1_down[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)




# ========== GENERATE FOR EITHER ===========

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who  V1      D2    N2      YET/decoy      V2    N3    YET/decoy
    # every  boy  who  bought  some  apples  yet/regularly  sang  song  yet/regularly

    # build all lexical items
    #TODO: throw in modifiers
    try:
        N1 = choice(all_animate_nouns)
        D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
        V1 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
        V1 = conjugate(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])       # restrict to UE quantifiers, otherwise there could be another licensor
        V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs), [V1])
        V2 = conjugate(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers), [D1_up, D1_down])
        decoy = choice(["regularly", "on weekends", "on occasion", "for a while", "as well"])
    except IndexError:
        print(N1[0], N2[0], V2[0])
        continue

    # build sentences with UE quantifier
    sentence_1 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], "either", V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "either")
    sentence_4 = "%s %s who %s %s %s %s %s %s %s." % (D1_up[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # build sentences with DE quantifier
    sentence_5 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], "either", V2[0], D3[0], N3[0])
    sentence_6 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], decoy, V2[0], D3[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], "either")
    sentence_8 = "%s %s who %s %s %s %s %s %s %s." % (D1_down[0], N1[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0], decoy)

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)
    sentence_5 = string_beautify(sentence_5)
    sentence_6 = string_beautify(sentence_6)
    sentence_7 = string_beautify(sentence_7)
    sentence_8 = string_beautify(sentence_8)

    # write sentences to output
    if sentence_1 not in sentences:
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=0-scope=1-npi_present=1" % D1_up[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=0-scope=1-npi_present=0" % D1_up[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=0-scope=0-npi_present=1" % D1_up[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=0-scope=0-npi_present=0" % D1_up[0], 1, sentence_4))

        # sentences 5-8 have quantifiers with DE restrictor
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=1-scope=1-npi_present=1" % D1_down[0], 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=1-scope=1-npi_present=0" % D1_down[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=1-scope=0-npi_present=1" % D1_down[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=quantifier-npi=either-crucial_item=%s-licensor=1-scope=0-npi_present=0" % D1_down[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)





output.close()