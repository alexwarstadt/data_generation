# Authors: Anna Alsop
# Script for generating NPI sentences with adverbs as licensors

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=adverbs.tsv"
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
all_common_dets = np.append(get_all("expression", "the"), np.append(get_all("expression", "a"), get_all("expression", "an")))
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1")])
all_nonfreq_adverbs = get_all_conjunctive([("frequent", "0"), ("category_2", "Adv")])
all_freq_adverbs = get_all_conjunctive([("frequent", "1"), ("category_2", "Adv")])
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_embedding_verbs = get_all_conjunctive([("category_2","V_embedding"),("finite","1")])
all_nouns = get_all("category", "N")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1   Adv     ever/also V1   that D2    N2   V2   D3    N3
    # The/a boy  rarely  ever/also says that the/a girl sang the/a song

    # build all lexical items
    #TODO: throw in modifiers
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_frequent_dets))
    Adv_freq = choice(all_freq_adverbs)
    Adv_nonfreq = choice(all_nonfreq_adverbs)
    V1 = choice(get_matched_by(N1, "arg_1", all_embedding_verbs))
    conjugate(V1, N1)
    N2 = choice(all_animate_nouns)
    D2 = choice(get_matched_by(N2, "arg_1", all_common_dets))
    V2 = choice(get_matched_by(N2, "arg_1", all_non_progressive_transitive_verbs))
    conjugate(V2, N2)
    N3 = choice(get_matches_of(V2, "arg_2", all_nouns))
    D3 = choice(get_matched_by(N3, "arg_1", all_frequent_dets))

    # build sentences with frequent adverb
    sentence_1 = "%s %s %s ever %s that %s %s %s %s %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_2 = "%s %s %s also %s that %s %s %s %s %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s %s %s that %s %s ever %s %s %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_4 = "%s %s %s %s that %s %s also %s %s %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])

    # build sentences with nonfrequent adverb
    sentence_5 = "%s %s %s ever %s that %s %s %s %s %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_6 = "%s %s %s also %s that %s %s %s %s %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_7 = "%s %s %s %s that %s %s ever %s %s %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])
    sentence_8 = "%s %s %s %s that %s %s also %s %s %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], D2[0], N2[0], V2[0], D3[0], N3[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=0_scope=1_npi-present=1" % Adv_freq[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=0_scope=1_npi-present=0" % Adv_freq[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=0_scope=0_npi-present=1" % Adv_freq[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=0_scope=0_npi-present=0" % Adv_freq[0], 1, sentence_4))

        # sentences 5-8 have nonfrequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=1_scope=1_npi-present=1" % Adv_nonfreq[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=1_scope=1_npi-present=0" % Adv_nonfreq[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=1_scope=0_npi-present=1" % Adv_nonfreq[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=ever_adverb=%s_licensor=1_scope=0_npi-present=0" % Adv_nonfreq[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "ever"

# repeat for "any"

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1   who  Adv    V1     any/the/0  N2       V2   any/the/0  N3
    # The/a boy  who  rarely helps  any/the/0  children sang any/the/0  songs

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adv_freq = choice(all_freq_adverbs)
    Adv_nonfreq = choice(all_nonfreq_adverbs)
    V1 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    conjugate(V1, N1)
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    V2 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
    conjugate(V2, N1)
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))

    # build sentences with frequent adverb
    sentence_1 = "%s %s who %s %s any %s %s %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], N2[0], V2[0], N3[0])
    sentence_2 = "%s %s who %s %s the %s %s %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], N2[0], V2[0], N3[0])
    sentence_3 = "%s %s who %s %s %s %s any %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], N2[0], V2[0], N3[0])
    sentence_4 = "%s %s who %s %s %s %s the %s ." % (D1[0], N1[0], Adv_freq[0], V1[0], N2[0], V2[0], N3[0])

    # build sentences with nonfrequent adverb
    sentence_5 = "%s %s who %s %s any %s %s %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], N2[0], V2[0], N3[0])
    sentence_6 = "%s %s who %s %s the %s %s %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], N2[0], V2[0], N3[0])
    sentence_7 = "%s %s who %s %s %s %s any %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], N2[0], V2[0], N3[0])
    sentence_8 = "%s %s who %s %s %s %s the %s ." % (D1[0], N1[0], Adv_nonfreq[0], V1[0], N2[0], V2[0], N3[0])

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
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=0_scope=1_npi-present=1" % Adv_freq[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=0_scope=1_npi-present=0" % Adv_freq[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=0_scope=0_npi-present=1" % Adv_freq[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=0_scope=0_npi-present=0" % Adv_freq[0], 1, sentence_4))

        # sentences 5-8 have nonfrequent adverb
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=1_scope=1_npi-present=1" % Adv_nonfreq[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=1_scope=1_npi-present=0" % Adv_nonfreq[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=1_scope=0_npi-present=1" % Adv_nonfreq[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=adverbs_npi=any_adverb=%s_licensor=1_scope=0_npi-present=0" % Adv_nonfreq[0], 1, sentence_8))

    sentences.add(sentence_1)

output.close()