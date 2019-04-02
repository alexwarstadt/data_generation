# Authors: Anna Alsop (based on Alex Warstadt's quantifier.py)
# Script for generating NPI sentences with adverbs as licensors

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import random
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=adverbs.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# generate sentences for "ever"

# set total number of paradigms to generate
number_to_generate = 50
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
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_nonfreq_adverbs = get_all_conjunctive([("frequent", "0"), ("category_2", "Adv")])
all_freq_adverbs = get_all_conjunctive([("frequent", "1"), ("category_2", "Adv")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_intransitive_verbs = get_all("category", "S\\NP")
all_non_progressive_intransitive_verbs = get_all("ing", "0", all_intransitive_verbs)
all_embedding_verbs = get_all_conjunctive([("category_2","V_embedding"),("finite","1")])
all_nouns = get_all("category", "N")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# gather NPI replacements
any_replacements = np.append(get_all("expression", "the"),
                                 np.append(get_all("expression", "these"),
                                 np.append(get_all("expression", "those"),
                                 np.append(get_all("expression", "this"), get_all("expression", "that")))))
ever_replacements = np.array(["often", "also", "fortunately", "certainly", "clearly"])
adverb_npi_replacements = np.array(["regularly", "on weekends", "on occasion", "for a while", "as well"])

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1  Aux1  Adv    ever/also V1   that D2    N2   (Aux) V2   D3    N3
    # The/a boy (has) rarely ever/also said that the/a girl (has) sung the/a song

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adv_freq = choice(all_freq_adverbs)
    Adv_nonfreq = choice(all_nonfreq_adverbs)
    NPI_replacement = choice(ever_replacements)
    V1 = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(all_animate_nouns)
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))

    # select transitive or intransitive V2
    x = random.random()
    if x < 1/2:
        # transitive V2
        V2 = choice(get_matched_by(N2, "arg_1", all_non_progressive_transitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_nouns))
        D3 = choice(get_matched_by(N3, "arg_1", all_common_dets))
    else:
        # intransitive V2 - gives empty string for N3 and D3 slots
        V2 = choice(get_matched_by(N2, "arg_1", all_non_progressive_intransitive_verbs))
        Aux2 = return_aux(V2, N2, allow_negated=False)
        N3 = " "
        D3 = " "

    # check for do/does/did for both aux verbs, make the aux directly adjacent to verb.
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

    # build sentences with frequent adverb
    sentence_1 = "%s %s %s %s ever %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_2 = "%s %s %s %s %s %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], NPI_replacement, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_3 = "%s %s %s %s %s that %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0],  V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_4 = "%s %s %s %s %s that %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0],  V1_final, D2[0], N2[0], Aux2_final, NPI_replacement, V2_final, D3[0], N3[0])

    # build sentences with nonfrequent adverb
    sentence_5 = "%s %s %s %s ever %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_6 = "%s %s %s %s %s %s that %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], NPI_replacement, V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_7 = "%s %s %s %s %s that %s %s %s ever %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, D2[0], N2[0], Aux2_final, V2_final, D3[0], N3[0])
    sentence_8 = "%s %s %s %s %s that %s %s %s %s %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, D2[0], N2[0], Aux2_final, NPI_replacement, V2_final, D3[0], N3[0])

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
        # sentences 1-4 have frequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=0-scope=1-npi_present=1" % Adv_freq[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=0-scope=1-npi_present=0" % Adv_freq[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=0-scope=0-npi_present=1" % Adv_freq[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=0-scope=0-npi_present=0" % Adv_freq[0], 1, sentence_4))

        # sentences 5-8 have nonfrequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=1-scope=1-npi_present=1" % Adv_nonfreq[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=1-scope=1-npi_present=0" % Adv_nonfreq[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=1-scope=0-npi_present=1" % Adv_nonfreq[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=ever-crucial_item=%s-licensor=1-scope=0-npi_present=0" % Adv_nonfreq[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "ever"

# repeat for "any"

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1   who  (Aux1) Adv    V1     any/the/0 N2       V2   any/the/0  N3
    # The/a boy  who  (had)  rarely helped any/the/0 children sang any/the/0  songs

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adv_freq = choice(all_freq_adverbs)
    Adv_nonfreq = choice(all_nonfreq_adverbs)
    V1 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    Aux1 = return_aux(V1, N1, allow_negated=False)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    V2 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    V2 = conjugate(V2, N1, allow_negated=False)
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))

    # check for do/does/did for aux verb, make the aux directly adjacent to verb.
    if Aux1[0] in ["do", "does", "did"]:
        Aux1_final = ""
        V1_final = Aux1[0] + " " + V1[0]
    else:
        Aux1_final = Aux1[0]
        V1_final = V1[0]

    # build sentences with frequent adverb
    sentence_1 = "%s %s who %s %s %s any %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], V2[0], N3[0])
    sentence_2 = "%s %s who %s %s %s the %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], V2[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s any %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], V2[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s %s the %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], V2[0], N3[0])

    # build sentences with nonfrequent adverb
    sentence_5 = "%s %s who %s %s %s any %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], V2[0], N3[0])
    sentence_6 = "%s %s who %s %s %s the %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], V2[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s any %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], V2[0], N3[0])
    sentence_8 = "%s %s who %s %s %s %s %s the %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], V2[0], N3[0])

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
        # sentences 1-4 have frequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=0-scope=1-npi_present=1" % Adv_freq[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=0-scope=1-npi_present=0" % Adv_freq[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=0-scope=0-npi_present=1" % Adv_freq[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=0-scope=0-npi_present=0" % Adv_freq[0], 1, sentence_4))

        # sentences 5-8 have nonfrequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=1-scope=1-npi_present=1" % Adv_nonfreq[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=1-scope=1-npi_present=0" % Adv_nonfreq[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=1-scope=0-npi_present=1" % Adv_nonfreq[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=any-crucial_item=%s-licensor=1-scope=0-npi_present=0" % Adv_nonfreq[0], 1, sentence_8))

    sentences.add(sentence_1)

# end of "any"

# repeat for "at all"

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1   who (Aux1) Adv    V1     N2       (at all/on weekends) (Aux2) V2   N3    (at all/on weekends)
    # The/a boy  who (had)  rarely helped children (at all/on weekends) (has)  sung songs (at all/on weekends)

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adv_freq = choice(all_freq_adverbs)
    Adv_nonfreq = choice(all_nonfreq_adverbs)
    # select transitive or intransitive V1
    x = random.random()
    if x < 1/2:
        # transitive V1
        V1 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    else:
        # intransitive V2 - gives empty string for N2 slot
        V1 = choice(get_matched_by(N1, "arg_1", all_non_progressive_intransitive_verbs))
        Aux1 = return_aux(V1, N1, allow_negated=False)
        N2 = " "

    # select transitive or intransitive V2
    if 1/3 < x < 2/3:
        # transitive V2
        V2 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
        Aux2 = return_aux(V2, N1, allow_negated=False)
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    else:
        # intransitive V2 - gives empty string for N3 slot
        V2 = choice(get_matched_by(N1, "arg_1", all_non_progressive_intransitive_verbs))
        Aux2 = return_aux(V2, N1, allow_negated=False)
        N3 = " "

    # check for do/does/did for aux verbs, make the aux directly adjacent to verb.
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

    # build sentences with frequent adverb
    sentence_1 = "%s %s who %s %s %s %s at all %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])
    sentence_2 = "%s %s who %s %s %s %s on weekends %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])
    sentence_3 = "%s %s who %s %s %s %s %s %s %s at all ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])
    sentence_4 = "%s %s who %s %s %s %s %s %s %s on weekends ." % (D1[0], N1[0], Aux1_final, Adv_freq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])

    # build sentences with nonfrequent adverb
    sentence_5 = "%s %s who %s %s %s %s at all %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])
    sentence_6 = "%s %s who %s %s %s %s on weekends %s %s %s ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])
    sentence_7 = "%s %s who %s %s %s %s %s %s %s at all ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])
    sentence_8 = "%s %s who %s %s %s %s %s %s %s on weekends ." % (D1[0], N1[0], Aux1_final, Adv_nonfreq[0], V1_final, N2[0], Aux2_final, V2_final, N3[0])

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
        # sentences 1-4 have frequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=0-scope=1-npi_present=1" % Adv_freq[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=0-scope=1-npi_present=0" % Adv_freq[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=0-scope=0-npi_present=1" % Adv_freq[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=0-scope=0-npi_present=0" % Adv_freq[0], 1, sentence_4))

        # sentences 5-8 have nonfrequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=1-scope=1-npi_present=1" % Adv_nonfreq[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=1-scope=1-npi_present=0" % Adv_nonfreq[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=1-scope=0-npi_present=1" % Adv_nonfreq[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=adverbs-npi=atall-crucial_item=%s-licensor=1-scope=0-npi_present=0" % Adv_nonfreq[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of adverbs

output.close()