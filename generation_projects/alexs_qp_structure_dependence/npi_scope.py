# Authors: Alex Warstadt
# Script for generating NPI sentences manipulating scope

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import string_beautify
from random import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/structure_dependence/npi_scope/3_21-10k"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
train_output = open(os.path.join(project_root, rel_output_path, "train.tsv"), "w")
test_output = open(os.path.join(project_root, rel_output_path, "test_full.tsv"), "w")
test2_output = open(os.path.join(project_root, rel_output_path, "test.tsv"), "w")
dev_output = open(os.path.join(project_root, rel_output_path, "dev.tsv"), "w")


# set total number of paradigms to generate
number_to_generate = 10000
sentences = set()
test_counter = 0    # Jiant requires test data to be in numbered, two-column format

# gather word classes that will be accessed frequently
all_frequent_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_nonfinite_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0")])
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
all_negative_auxiliaries = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "1")])
all_non_negative_auxiliaries = np.setdiff1d(get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)")]), all_negative_auxiliaries)
all_UE_UE_quantifiers = get_all_conjunctive([("restrictor_DE", "0"), ("category", "(S/(S\\NP))/N"), ("frequent", "1")])

# sample sentences until desired number
while len(sentences) < number_to_generate:
    # sentence template
    # D1   N1   who Aux1   V1      any/the/D2    N2      Aux2    V2    any/the/D3  N3
    # the  boy  Rel should buy     any/the/some  apples  didn't  sing  any/the/a   song

    # D1   N1   who Aux1   V1   any/the/D2    N2      Aux2   V2    any/the/D3  N3
    # the  boy  Rel didn't buy  any/the/some  apples  should sing  any/the/a   song

    # build all lexical items
    #TODO: throw in modifiers
    V1 = choice(all_nonfinite_transitive_verbs)
    V2 = choice(all_nonfinite_transitive_verbs)
    N1 = choice(get_matches_of(V1, "arg_1", all_frequent_nouns))
    N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
    N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
    D1 = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
    D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers))
    D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers))
    NegAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)))
    PosAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)))
    NegAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)))
    PosAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)))
    Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))

    sentence_1 = "%s %s %s %s %s %s %s %s %s %s %s." % (D1[0], N1[0], Rel[0], PosAux1[0], V1[0], D2[0], N2[0], NegAux2[0], V2[0], "any", N3[0])
    sentence_2 = "%s %s %s %s %s %s %s %s %s %s %s." % (D1[0], N1[0], Rel[0], PosAux1[0], V1[0], "any", N2[0], NegAux2[0], V2[0], D3[0], N3[0])
    sentence_3 = "%s %s %s %s %s %s %s %s %s %s %s." % (D1[0], N1[0], Rel[0], NegAux1[0], V1[0], D2[0], N2[0], PosAux2[0], V2[0], "any", N3[0])
    sentence_4 = "%s %s %s %s %s %s %s %s %s %s %s." % (D1[0], N1[0], Rel[0], NegAux1[0], V1[0], "any", N2[0], PosAux2[0], V2[0], D3[0], N3[0])

    # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
    # but the code outputs a determiner with an empty string. might want to change this)
    sentence_1 = string_beautify(sentence_1)
    sentence_2 = string_beautify(sentence_2)
    sentence_3 = string_beautify(sentence_3)
    sentence_4 = string_beautify(sentence_4)

    in_domain_writer = np.random.choice([train_output, dev_output, test_output], 1, p=[0.5, 0.25, 0.25])[0]
    out_of_domain_writer = np.random.choice([dev_output, test_output], 1)[0] \
        if in_domain_writer == train_output \
        else in_domain_writer
    paradigm_in_domain = 1 if in_domain_writer == train_output else 0

    # write sentences to output
    if sentence_1 not in sentences:
        in_domain_writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=0-npi_embedded=0-licensor_precede=1-paradigm_in_domain=%d" % (NegAux2[0], paradigm_in_domain), 1, sentence_1))
        in_domain_writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=0-npi_embedded=1-licensor_precede=0-paradigm_in_domain=%d" % (NegAux2[0], paradigm_in_domain), 0, sentence_2))
        out_of_domain_writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=1-npi_embedded=0-licensor_precede=1-paradigm_in_domain=%d" % (NegAux1[0], paradigm_in_domain), 0, sentence_3))
        out_of_domain_writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=1-npi_embedded=1-licensor_precede=1-paradigm_in_domain=%d" % (NegAux1[0], paradigm_in_domain), 1, sentence_4))

    if in_domain_writer == test_output:
        test2_output.write("%d\t%s\n" % (test_counter, sentence_1))
        test_counter += 1
        test2_output.write("%d\t%s\n" % (test_counter, sentence_2))
        test_counter += 1

    if out_of_domain_writer == test_output:
        test2_output.write("%d\t%s\n" % (test_counter, sentence_3))
        test_counter += 1
        test2_output.write("%d\t%s\n" % (test_counter, sentence_4))
        test_counter += 1

    # keep track of which sentences have already been generated
    sentences.add(sentence_1)

# the end :)






# # repeat for "ever"
#
# # PITFALL:
# # ever doesn't occur with progressive
# # Every boy who has ever eaten a potato is tall.
# # *? Every boy who is ever eating a potato is tall.
# sentences = set()
# all_non_progressive_transitive_verbs = get_all("ing", "0", all_transitive_verbs)
# while len(sentences) < number_to_generate:
#     # sentence template
#     # D1     N1   who  (Aux)  ever  V1      the  N2      V2    D2  N3
#     # every  boy  who  (has)  ever  bought  the  apples  sang  a   song
#
#     N1 = choice(all_animate_nouns)
#     D1_up = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
#     D1_down = choice(get_matched_by(N1, "arg_1", all_DE_UE_quantifiers))
#     V1 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
#     Aux1 = return_aux(V1, N1, allow_negated=False)
#     N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns))
#     D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers))
#     V2 = choice(get_matched_by(N1, "arg_1", all_non_progressive_transitive_verbs))
#     Aux2 = return_aux(V2, N1, allow_negated=False)
#     N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns))
#     D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers))
#
#     # the replacement for "ever" depends on the tense of the verb
#     # if the auxiliary is empty (i.e. the main verb is finite), use the tense of the verb, else use the auxiliary
#     if Aux1[0] == "":
#         emb_adv = "now" if V1["pres"] == "1" else "once"
#     else:
#         emb_adv = "now" if Aux1["pres"] == "1" else "once"
#     if Aux2[0] == "":
#         matrix_adv = "now" if V2["pres"] == "1" else "once"
#     else:
#         matrix_adv = "now" if Aux2["pres"] == "1" else "once"
#
#
#
#     sentence_1 = "%s %s who %s ever %s %s %s %s %s %s %s ." % (D1_up[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
#     sentence_2 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_up[0], N1[0], Aux1[0], emb_adv, V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
#     sentence_3 = "%s %s who %s %s %s %s %s ever %s %s %s ." % (D1_up[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
#     sentence_4 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_up[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], matrix_adv, V2[0], D3[0], N3[0])
#
#     sentence_5 = "%s %s who %s ever %s %s %s %s %s %s %s ." % (D1_down[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
#     sentence_6 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_down[0], N1[0], Aux1[0], emb_adv, V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
#     sentence_7 = "%s %s who %s %s %s %s %s ever %s %s %s ." % (D1_down[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], V2[0], D3[0], N3[0])
#     sentence_8 = "%s %s who %s %s %s %s %s %s %s %s %s ." % (D1_down[0], N1[0], Aux1[0], V1[0], D2[0], N2[0], Aux2[0], matrix_adv, V2[0], D3[0], N3[0])
#
#     # remove doubled up spaces (this is because of empty determiner AND EMPTY AUXILIARY).
#     sentence_1 = remove_extra_whitespace(sentence_1)
#     sentence_2 = remove_extra_whitespace(sentence_2)
#     sentence_3 = remove_extra_whitespace(sentence_3)
#     sentence_4 = remove_extra_whitespace(sentence_4)
#     sentence_5 = remove_extra_whitespace(sentence_5)
#     sentence_6 = remove_extra_whitespace(sentence_6)
#     sentence_7 = remove_extra_whitespace(sentence_7)
#     sentence_8 = remove_extra_whitespace(sentence_8)
#
#
#     # write sentences to output
#     if sentence_1 not in sentences:
#         # sentences 1-4 have quantifiers with UE restrictor
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=1_npi-present=1" % D1_up[0], 0, sentence_1))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=1_npi-present=0" % D1_up[0], 1, sentence_2))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=0_npi-present=1" % D1_up[0], 0, sentence_3))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=0_scope=0_npi-present=0" % D1_up[0], 1, sentence_4))
#
#         # sentences 5-8 have quantifiers with DE restrictor
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=1_npi-present=1" % D1_down[0], 1, sentence_5))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=1_npi-present=0" % D1_down[0], 1, sentence_6))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=0_npi-present=1" % D1_down[0], 0, sentence_7))
#         output.write("%s\t%d\t\t%s\n" % ("experiment=NPI_env=quantifier_npi=any_quantifier=%s_licensor=1_scope=0_npi-present=0" % D1_down[0], 1, sentence_8))
#
#     sentences.add(sentence_1)
#
# output.close()