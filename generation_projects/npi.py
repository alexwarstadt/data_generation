from utils.vocab_table import *
from utils.conjugate import *
from random import choice

# initialize output file
output = open("../outputs/npi_environment=quantifiers.tsv", "w")

# set total number of sentences to generate
number_to_generate = 10000
sentences = set()

# gather word classes that will be accessed frequently
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1")])
all_quantifiers = get_all("category", "(S/(S\\NP))/N")
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1     N1   who V1   any/the N2      V2    D2 N3
    # every  boy  who ate  any/the apples  sang  a  song

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "argument_1", all_quantifiers))
    V1 = choice(get_matched_by(N1, "argument_2", all_transitive_verbs))
    V1 = conjugate(V1, N1)
    N2 = choice(get_matches_of(V1, "argument_1", all_non_singular_nouns))
    V2 = choice(get_matched_by(N1, "argument_2", all_transitive_verbs))
    V2 = conjugate(V2, N1)
    N3 = choice(get_matches_of(V2, "argument_1"))
    D2 = choice(get_matched_by(N3, "argument_1", all_quantifiers))

    # build sentences
    sentence_1 = "%s %s who %s any %s %s %s %s ." % (D1[0], N1[0], V1[0], N2[0], V2[0], D2[0], N3[0])
    sentence_2 = "%s %s who %s the %s %s %s %s ." % (D1[0], N1[0], V1[0], N2[0], V2[0], D2[0], N3[0])

    # write sentences to output
    if sentence_1 not in sentences:
        if D1["restrictor_DE"] == "1":
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=1", 1, sentence_1))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=1_scope=1_npi-present=0", 1, sentence_2))
        else:
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=1_npi-present=1", 0, sentence_1))
            output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_licensor=0_scope=1_npi-present=0", 1, sentence_2))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)
    sentences.add(sentence_2)

# the end :)




