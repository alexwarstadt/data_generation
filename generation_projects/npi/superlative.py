# Authors: Anna Alsop (based on Alex Warstadt's quantifier.py)
# Script for generating NPI sentences with superlatives as licensors

from utils.conjugate import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/npi/environment=superlative.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# generate sentences for "ever"

# set total number of paradigms to generate
number_to_generate = 1000
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
all_superlative_adjectives = get_all("category_2", "Adj_super")
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
all_past_perfect_transitive_verbs = np.append(get_all("past", "1", all_transitive_verbs), get_all("en", "1", all_transitive_verbs))
all_en_verbs = get_all("en", "1", all_transitive_verbs)
all_past_verbs = get_all("past", "1", all_transitive_verbs)
all_embedding_verbs = get_all_conjunctive([("category_2","V_embedding"),("finite","1")])
all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1"), ("appearance", "")])
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))

# gather NPI replacements
any_replacements = np.append(get_all("expression", "the"),
                                 np.append(get_all("expression", "these"),
                                 np.append(get_all("expression", "those"),
                                 np.append(get_all("expression", "this"), get_all_conjunctive([("expression", "that"),
                                           ("category_2", "D")])))))
ever_replacements = np.array(["often", "also", "fortunately", "obviously", "clearly"])
adverb_npi_replacements = np.array(["regularly", "on weekends", "on occasion", "for a while", "as well"])

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1    N1  (Aux1) V1     the Adj_super N2  that the N3   Aux2 ever V2_en.
    # The/a boy (has)  bought the fastest   car that the girl had  ever seen.

    # build all lexical items
    N1 = choice(all_animate_nouns) # boy
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adj_super = choice(all_superlative_adjectives) # fastest
    Adj = choice(get_all("expression", Adj_super["adjs"])) # fast
    N2 = choice(get_matches_of(Adj, "arg_1", all_nouns)) # car
    # select verb that selects for N1, N2
    V1_options = np.array(list(filter(lambda x: np.logical_and(is_match_disj(N2, x["arg_2"]), is_match_disj(N1, x["arg_1"])),
                                      all_non_progressive_transitive_verbs)), dtype=data_type)
    V1 = choice(V1_options) # bought
    Aux1 = return_aux(V1, N1, allow_negated=False)
    # select -en verb that selects for N2
    V2_options = np.array(list(filter(lambda x: is_match_disj(N2, x["arg_2"]), all_en_verbs)), dtype=data_type)
    V2 = choice(V2_options)
    N3 = choice(get_matches_of(V2, "arg_1", all_nouns))  # girl
    Aux2 = return_aux(V2, N3, allow_negated=False) # had or has
    NPI_replacement = choice(ever_replacements)

    # check for do/does/did for Aux1 (Aux2 is always had/has/have), make the aux directly adjacent to verb.
    if Aux1[0] in ["do", "does", "did"]:
        Aux1_final = ""
        V1_final = Aux1[0] + " " + V1[0]
    else:
        Aux1_final = Aux1[0]
        V1_final = V1[0]

    # build sentences with plain adjective
    sentence_1 = "%s %s %s %s the %s %s that the %s %s ever %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj[0], N2[0],
                                                                     N3[0], Aux2[0], V2[0])
    sentence_2 = "%s %s %s %s the %s %s that the %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj[0], N2[0],
                                                                   N3[0], Aux2[0], NPI_replacement, V2[0])
    sentence_3 = "%s %s %s ever %s the %s %s that the %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj[0], N2[0],
                                                                     N3[0], Aux2[0], V2[0])
    sentence_4 = "%s %s %s %s %s the %s %s that the %s %s %s ." % (D1[0], N1[0], Aux1_final, NPI_replacement,
                                                                   V1_final, Adj[0], N2[0], N3[0], Aux2[0], V2[0])

    # build sentences with superlative adjective
    sentence_5 = "%s %s %s %s the %s %s that the %s %s ever %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj_super[0],
                                                                     N2[0], N3[0], Aux2[0], V2[0])
    sentence_6 = "%s %s %s %s the %s %s that the %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj_super[0],
                                                                   N2[0], N3[0], Aux2[0], NPI_replacement, V2[0])
    sentence_7 = "%s %s %s ever %s the %s %s that the %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj_super[0],
                                                                     N2[0], N3[0], Aux2[0], V2[0])
    sentence_8 = "%s %s %s %s %s the %s %s that the %s %s %s ." % (D1[0], N1[0], Aux1_final, NPI_replacement,
                                                                   V1_final, Adj_super[0], N2[0], N3[0], Aux2[0], V2[0])

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
        # sentences 1-4 have plain adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=0-scope=1-npi_present=1" % Adj[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=0-scope=1-npi_present=0" % Adj[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=0-scope=0-npi_present=1" % Adj[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=0-scope=0-npi_present=0" % Adj[0], 1, sentence_4))

        # sentences 5-8 have superlative adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=1-scope=1-npi_present=1" % Adj_super[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=1-scope=1-npi_present=0" % Adj_super[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=1-scope=0-npi_present=1" % Adj_super[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=ever-adj=%s-licensor=1-scope=0-npi_present=0" % Adj_super[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "ever"

# repeat for "any"

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1      N1   (Aux1) V1    the Adj_super N2     that the/any N3         Aux2  V2_en.
    # The/any boys (have) eaten the biggest   burger that the/any waitresses had   seen.

    # build all lexical items
    N1 = choice(all_animate_nouns)
    NPI_replacement_N1 = choice(get_matched_by(N1, "arg_1", any_replacements))
    Adj_super = choice(all_superlative_adjectives)
    Adj = choice(get_all("expression", Adj_super["adjs"]))
    N2 = choice(get_matches_of(Adj, "arg_1", all_nouns))
    # select verb that selects for N1, N2
    V1_options = np.array(
        list(filter(lambda x: np.logical_and(is_match_disj(N2, x["arg_2"]), is_match_disj(N1, x["arg_1"])),
                    all_transitive_verbs)), dtype=data_type)
    V1 = choice(V1_options)
    Aux1 = return_aux(V1, N1, allow_negated=False)
    # select -en verb that selects for N2
    V2_options = np.array(list(filter(lambda x: is_match_disj(N2, x["arg_2"]), all_en_verbs)), dtype=data_type)
    V2 = choice(V2_options)
    N3 = choice(get_matches_of(V2, "arg_1", all_non_singular_nouns))
    Aux2 = return_aux(V2, N3, allow_negated=False)
    NPI_replacement_N3 = choice(get_matched_by(N3, "arg_1", any_replacements))

    # check for do/does/did for Aux1 (Aux2 is always had/has/have), make the aux directly adjacent to verb.
    if Aux1[0] in ["do", "does", "did"]:
        Aux1_final = ""
        V1_final = Aux1[0] + " " + V1[0]
    else:
        Aux1_final = Aux1[0]
        V1_final = V1[0]

    # build sentences with plain adjective
    sentence_1 = "%s %s %s %s the %s %s that any %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj[0], N2[0], N3[0],
                                                                Aux2[0], V2[0])
    sentence_2 = "%s %s %s %s the %s %s that %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj[0], N2[0],
                                                               NPI_replacement_N3[0], N3[0], Aux2[0], V2[0])
    sentence_3 = "any %s %s %s the %s %s that %s %s %s ." % (N1[0], Aux1_final, V1_final, Adj[0], N2[0], N3[0], Aux2[0],
                                                             V2[0])
    sentence_4 = "%s %s %s %s the %s %s that %s %s %s ." % (NPI_replacement_N1[0], N1[0], Aux1_final, V1_final, Adj[0],
                                                            N2[0], N3[0], Aux2[0], V2[0])

    # build sentences with superlative adjective
    sentence_5 = "%s %s %s %s the %s %s that any %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj_super[0], N2[0],
                                                                N3[0], Aux2[0], V2[0])
    sentence_6 = "%s %s %s %s the %s %s that %s %s %s %s ." % (D1[0], N1[0], Aux1_final, V1_final, Adj_super[0], N2[0],
                                                               NPI_replacement_N3[0], N3[0], Aux2[0], V2[0])
    sentence_7 = "any %s %s %s the %s %s that %s %s %s ." % (N1[0], Aux1_final, V1_final, Adj_super[0], N2[0], N3[0],
                                                             Aux2[0], V2[0])
    sentence_8 = "%s %s %s %s the %s %s that %s %s %s ." % (NPI_replacement_N1[0], N1[0], Aux1_final, V1_final,
                                                            Adj_super[0], N2[0], N3[0], Aux2[0], V2[0])

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
        # sentences 1-4 have plain adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=0-scope=1-npi_present=1" % Adj[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=0-scope=1-npi_present=0" % Adj[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=0-scope=0-npi_present=1" % Adj[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=0-scope=0-npi_present=0" % Adj[0], 1, sentence_4))

        # sentences 5-8 have superlative adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=1-scope=1-npi_present=1" % Adj_super[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=1-scope=1-npi_present=0" % Adj_super[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=1-scope=0-npi_present=1" % Adj_super[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=any-adj=%s-licensor=1-scope=0-npi_present=0" % Adj_super[0], 1, sentence_8))

    sentences.add(sentence_1)

# end of "any"

# repeat for "at all"
# caution: weak NPI but no good under superlative

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1  N1   who V1_past the Adj_super N2     (at all/on weekends) (Aux2) V2   N3    (at all/on weekends).
    # The boys who ate     the biggest   burger (at all/on weekends) (Aux2) sang songs (at all/on weekends).

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adj_super = choice(all_superlative_adjectives)
    Adj = choice(get_all("expression", Adj_super["adjs"]))
    N2 = choice(get_matches_of(Adj, "arg_1", all_nouns))
    # select verb that selects for N1, N2
    V1_options = np.array(
        list(filter(lambda x: np.logical_and(is_match_disj(N2, x["arg_2"]), is_match_disj(N1, x["arg_1"])),
                    all_past_verbs)), dtype=data_type)
    V1 = choice(V1_options)
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    Aux2 = return_aux(V2, N3, allow_negated=False)
    NPI_replacement = choice(adverb_npi_replacements)

    # build sentences with plain adjective
    sentence_1 = "%s %s who %s the %s %s at all %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_2 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], NPI_replacement, Aux2[0],
                                                           V2[0], N3[0])
    sentence_3 = "%s %s who %s the %s %s %s %s %s at all ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_4 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

    # build sentences with superlative adjective
    sentence_5 = "%s %s who %s the %s %s at all %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_6 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], NPI_replacement,
                                                           Aux2[0], V2[0], N3[0])
    sentence_7 = "%s %s who %s the %s %s %s %s %s at all ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_8 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

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
        # sentences 1-4 have plain adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=0-scope=1-npi_present=1" % Adj[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=0-scope=1-npi_present=0" % Adj[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=0-scope=0-npi_present=1" % Adj[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=0-scope=0-npi_present=0" % Adj[0], 1, sentence_4))

        # sentences 5-8 have superlative adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=1-scope=1-npi_present=1" % Adj_super[0], 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=1-scope=1-npi_present=0" % Adj_super[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=1-scope=0-npi_present=1" % Adj_super[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=atall-adj=%s-licensor=1-scope=0-npi_present=0" % Adj_super[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "at all"

# repeat for "yet"

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1  N1   who V1_past the Adj_super N2     (yet/on weekends) (Aux2) V2   N3    (yet/on weekends).
    # The boys who ate     the biggest   burger (yet/on weekends) (Aux2) sang songs (yet/on weekends).

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adj_super = choice(all_superlative_adjectives)
    Adj = choice(get_all("expression", Adj_super["adjs"]))
    N2 = choice(get_matches_of(Adj, "arg_1", all_nouns))
    # select verb that selects for N1, N2
    V1_options = np.array(
        list(filter(lambda x: np.logical_and(is_match_disj(N2, x["arg_2"]), is_match_disj(N1, x["arg_1"])),
                    all_past_verbs)), dtype=data_type)
    V1 = choice(V1_options)
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    Aux2 = return_aux(V2, N3, allow_negated=False)
    NPI_replacement = choice(adverb_npi_replacements)

    # build sentences with plain adjective
    sentence_1 = "%s %s who %s the %s %s yet %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                            N3[0])
    sentence_2 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], NPI_replacement, Aux2[0],
                                                           V2[0], N3[0])
    sentence_3 = "%s %s who %s the %s %s %s %s %s yet ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                            N3[0])
    sentence_4 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

    # build sentences with superlative adjective
    sentence_5 = "%s %s who %s the %s %s yet %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                            N3[0])
    sentence_6 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], NPI_replacement,
                                                           Aux2[0], V2[0], N3[0])
    sentence_7 = "%s %s who %s the %s %s %s %s %s yet ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                            N3[0])
    sentence_8 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

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
        # sentences 1-4 have plain adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=0-scope=1-npi_present=1" % Adj[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=0-scope=1-npi_present=0" % Adj[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=0-scope=0-npi_present=1" % Adj[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=0-scope=0-npi_present=0" % Adj[0], 1, sentence_4))

        # sentences 5-8 have superlative adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=1-scope=1-npi_present=1" % Adj_super[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=1-scope=1-npi_present=0" % Adj_super[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=1-scope=0-npi_present=1" % Adj_super[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=yet-adj=%s-licensor=1-scope=0-npi_present=0" % Adj_super[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "yet"

# repeat for "in years"
# strong NPI, but good under superlative

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1  N1   who V1_past the Adj_super N2     (in years/on weekends) (Aux2) V2   N3    (in years/on weekends).
    # The boys who ate     the biggest   burger (in years/on weekends) (Aux2) sang songs (in years/on weekends).

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adj_super = choice(all_superlative_adjectives)
    Adj = choice(get_all("expression", Adj_super["adjs"]))
    N2 = choice(get_matches_of(Adj, "arg_1", all_nouns))
    # select verb that selects for N1, N2
    V1_options = np.array(
        list(filter(lambda x: np.logical_and(is_match_disj(N2, x["arg_2"]), is_match_disj(N1, x["arg_1"])),
                    all_past_verbs)), dtype=data_type)
    V1 = choice(V1_options)
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    Aux2 = return_aux(V2, N3, allow_negated=False)
    NPI_replacement = choice(adverb_npi_replacements)

    # build sentences with plain adjective
    sentence_1 = "%s %s who %s the %s %s in years %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_2 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], NPI_replacement, Aux2[0],
                                                           V2[0], N3[0])
    sentence_3 = "%s %s who %s the %s %s %s %s %s in years ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_4 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

    # build sentences with superlative adjective
    sentence_5 = "%s %s who %s the %s %s in years %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_6 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], NPI_replacement,
                                                           Aux2[0], V2[0], N3[0])
    sentence_7 = "%s %s who %s the %s %s %s %s %s in years ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_8 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

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
        # sentences 1-4 have plain adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=0-scope=1-npi_present=1" % Adj[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=0-scope=1-npi_present=0" % Adj[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=0-scope=0-npi_present=1" % Adj[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=0-scope=0-npi_present=0" % Adj[0], 1, sentence_4))

        # sentences 5-8 have superlative adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=1-scope=1-npi_present=1" % Adj_super[0], 1, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=1-scope=1-npi_present=0" % Adj_super[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=1-scope=0-npi_present=1" % Adj_super[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=inyears-adj=%s-licensor=1-scope=0-npi_present=0" % Adj_super[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "in years"

# repeat for "either"
# strong NPI, no good under superlative

sentences = set()
while len(sentences) < number_to_generate:
    # sentence template
    # D1  N1   who V1_past the Adj_super N2     (either/on weekends) (Aux2) V2   N3    (in years/on weekends).
    # The boys who ate     the biggest   burger (either/on weekends) (Aux2) sang songs (in years/on weekends).

    # build all lexical items
    N1 = choice(all_animate_nouns)
    D1 = choice(get_matched_by(N1, "arg_1", all_common_dets))
    Adj_super = choice(all_superlative_adjectives)
    Adj = choice(get_all("expression", Adj_super["adjs"]))
    N2 = choice(get_matches_of(Adj, "arg_1", all_nouns))
    # select verb that selects for N1, N2
    V1_options = np.array(
        list(filter(lambda x: np.logical_and(is_match_disj(N2, x["arg_2"]), is_match_disj(N1, x["arg_1"])),
                    all_past_verbs)), dtype=data_type)
    V1 = choice(V1_options)
    V2 = choice(get_matched_by(N1, "arg_1", all_transitive_verbs))
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    Aux2 = return_aux(V2, N3, allow_negated=False)
    NPI_replacement = choice(adverb_npi_replacements)

    # build sentences with plain adjective
    sentence_1 = "%s %s who %s the %s %s either %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_2 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], NPI_replacement, Aux2[0],
                                                           V2[0], N3[0])
    sentence_3 = "%s %s who %s the %s %s %s %s %s either ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_4 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

    # build sentences with superlative adjective
    sentence_5 = "%s %s who %s the %s %s either %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_6 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], NPI_replacement,
                                                           Aux2[0], V2[0], N3[0])
    sentence_7 = "%s %s who %s the %s %s %s %s %s either ." % (D1[0], N1[0], V1[0], Adj_super[0], N2[0], Aux2[0], V2[0],
                                                               N3[0])
    sentence_8 = "%s %s who %s the %s %s %s %s %s %s ." % (D1[0], N1[0], V1[0], Adj[0], N2[0], Aux2[0], V2[0], N3[0],
                                                           NPI_replacement)

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
        # sentences 1-4 have plain adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=0-scope=1-npi_present=1" % Adj[0], 0, sentence_1))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=0-scope=1-npi_present=0" % Adj[0], 1, sentence_2))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=0-scope=0-npi_present=1" % Adj[0], 0, sentence_3))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=0-scope=0-npi_present=0" % Adj[0], 1, sentence_4))

        # sentences 5-8 have superlative adjective
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=1-scope=1-npi_present=1" % Adj_super[0], 0, sentence_5))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=1-scope=1-npi_present=0" % Adj_super[0], 1, sentence_6))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=1-scope=0-npi_present=1" % Adj_super[0], 0, sentence_7))
        output.write("%s\t%d\t\t%s\n" % ("experiment=NPI-env=superlative-npi=either-adj=%s-licensor=1-scope=0-npi_present=0" % Adj_super[0], 1, sentence_8))

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# end of "either"

# end of superlative

output.close()