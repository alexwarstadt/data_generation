# Authors: Alex Warstadt
# Script for generating NPI sentences with quantifiers as licensors

from utils.vocab_table import *
from utils.conjugate import *
from random import choice
from utils.string_utils import remove_extra_whitespace

# initialize output file
output = open("../outputs/npi/environment=quantifiers.tsv", "w")

# set total number of sentences to generate
number_to_generate = 1000
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1")])
all_quantifiers = get_all("category", "(S/(S\\NP))/N")
all_UE_quantifiers = get_all("restrictor_DE", "0", all_quantifiers)
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who V1      any/the/D2    N2      V2    any/the/D3  N3
    # every  boy  who bought  any/the/some  apples  sang  any/the/a   song

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_quantifiers))
    V1 = choice(get_matched_by(N1, "arg_2", all_transitive_verbs))
    conjugate(V1, N1)
    N2 = choice(get_matches_of(V1, "arg_1", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_UE_quantifiers))        # restrict to UE quantifiers, otherwise there could be another licensor
    V2 = choice(get_matched_by(N1, "arg_2", all_transitive_verbs))
    conjugate(V2, N1)
    N3 = choice(get_matches_of(V2, "arg_1", all_non_singular_nouns))
    D3 = choice(get_matched_by(N3, "arg_1", all_UE_quantifiers))

    # build sentences
    sentence_1 = "%s %s who %s any %s %s %s %s ." % (D1[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s the %s %s %s %s ." % (D1[0], N1[0], V1[0], N2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s any %s ." % (D1[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s the %s ." % (D1[0], N1[0], V1[0], D2[0], N2[0], V2[0], N3[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)

    # write sentences to output
    if sentence_1 not in sentences:
        if D1["restrictor_DE"] == "1":
            # If the quantifier restrictor is DE, then "any" in the RC is acceptable
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        else:
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=1_npi-present=1", 0, sentence_1))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=1_npi-present=0", 1, sentence_2))

        if D1["scope_DE"] == "1":
            # If the quantifier scope is DE, then matrix "any" is acceptable: No boy who ate the apple sang any/the songs
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_3))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_4))
        elif D1["restrictor_DE"] == "1":
            # If ONLY the restrictor is DE, then matrix "any" is unacceptable: Every who ate the apple sang any/the songs
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=0_npi-present=1", 0, sentence_3))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=0_npi-present=0", 1, sentence_4))
        else:
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=0_npi-present=1", 0, sentence_3))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=0_npi-present=0", 1, sentence_4))

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
    D1 = choice(get_matched_by(N1, "arg_1", all_quantifiers))
    V1 = choice(get_matched_by(N1, "arg_2", all_non_progressive_transitive_verbs))
    Aux1 = return_aux(V1, N1)
    N2 = choice(get_matches_of(V1, "arg_1", all_non_singular_nouns))
    D2 = choice(get_matched_by(N2, "arg_1", all_UE_quantifiers))
    V2 = choice(get_matched_by(N1, "arg_2", all_transitive_verbs))
    Aux2 = return_aux(V2, N1)
    N3 = choice(get_matches_of(V2, "arg_1"))
    D3 = choice(get_matched_by(N3, "arg_1", all_UE_quantifiers))

    sentence_1 = "%s %s who %s ever %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s who %s once %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s %s once %s %s %s ." % (D1[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])

    # remove doubled up spaces (this is because of empty determiner AND EMPTY AUXILIARY).
    sentence_1 = remove_extra_whitespace(sentence_1)
    sentence_2 = remove_extra_whitespace(sentence_2)
    sentence_3 = remove_extra_whitespace(sentence_3)
    sentence_4 = remove_extra_whitespace(sentence_4)

    if sentence_1 not in sentences:
        if D1["restrictor_DE"] == "1":
            # If the quantifier restrictor is DE, then "any" in the RC is acceptable
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        else:
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=1_npi-present=1", 0, sentence_1))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=1_npi-present=0", 1, sentence_2))

        if D1["scope_DE"] == "1":
            # If the quantifier scope is DE, then matrix "any" is acceptable: No boy who ate the apple sang any/the songs
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_3))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_4))
        elif D1["restrictor_DE"] == "1":
            # If ONLY the restrictor is DE, then matrix "any" is unacceptable: Every who ate the apple sang any/the songs
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=0_npi-present=1", 0, sentence_3))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=0_npi-present=0", 1, sentence_4))
        else:
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=0_npi-present=1", 0, sentence_3))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=0_npi-present=0", 1, sentence_4))

    sentences.add(sentence_1)

output.close()