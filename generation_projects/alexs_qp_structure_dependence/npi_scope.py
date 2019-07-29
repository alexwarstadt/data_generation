# Authors: Alex Warstadt
# Script for generating NPI sentences manipulating scope

# TODO: document metadata

from utils.conjugate import *
from utils.string_utils import string_beautify
from utils.randomize import choice
import numpy as np

# initialize output file
rel_output_path = "outputs/alexs_qp_structure_dependence/npi_scope/30k/CoLA/"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
train_output = open(os.path.join(project_root, rel_output_path, "train.tsv"), "w")
test_output = open(os.path.join(project_root, rel_output_path, "test_full.tsv"), "w")
test2_output = open(os.path.join(project_root, rel_output_path, "test.tsv"), "w")
dev_output = open(os.path.join(project_root, rel_output_path, "dev.tsv"), "w")


# set total number of paradigms to generate
number_to_generate = 10000
sentences = set()
counter = 0    # Jiant requires test data to be in numbered, two-column format

# gather word classes that will be accessed frequently
all_frequent_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_animate_nouns = get_all_conjunctive([("category", "N"), ("animate", "1"), ("frequent", "1")])
all_nonfinite_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0")])
all_non_singular_nouns = np.intersect1d(np.append(get_all("pl", "1"), get_all("mass", "1")), get_all("frequent", "1"))
all_negative_auxiliaries = get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)"), ("negated", "1")])
all_non_negative_auxiliaries = np.setdiff1d(get_all_conjunctive([("category", "(S\\NP)/(S[bare]\\NP)")]), all_negative_auxiliaries)
all_UE_UE_quantifiers = get_all_conjunctive([("restrictor_DE", "0"), ("category", "(S/(S\\NP))/N"), ("frequent", "1")])

# sample sentences until desired number
for writer in [train_output, dev_output, test_output]:
    counter = 0
    while counter < number_to_generate:
    # sentence template
    # D1   N1   who Aux1   V1      any/the/D2    N2      Aux2    V2    any/the/D3  N3
    # the  boy  Rel should buy     any/the/some  apples  didn't  sing  any/the/a   song

    # D1   N1   who Aux1   V1   any/the/D2    N2      Aux2   V2    any/the/D3  N3
    # the  boy  Rel didn't buy  any/the/some  apples  should sing  any/the/a   song

    # build all lexical items
    #TODO: throw in modifiers
        V1 = choice(all_nonfinite_transitive_verbs)
        V2 = choice(all_nonfinite_transitive_verbs, [V1])
        N1 = choice(get_matches_of(V1, "arg_1", all_frequent_nouns))
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D1 = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers))
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers))
        NegAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)))
        PosAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)))
        NegAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)), [NegAux1])
        PosAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)), [PosAux1])
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

        if sentence_1 not in sentences:
            if writer == test_output:
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=0-npi_embedded=0-licensor_precede=1" % (NegAux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=0-npi_embedded=1-licensor_precede=0" % (NegAux2[0]), 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=1-npi_embedded=0-licensor_precede=1" % (NegAux1[0]), 0, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=1-npi_embedded=1-licensor_precede=1" % (NegAux1[0]), 1, sentence_4))
                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
            else:
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=0-npi_embedded=0-licensor_precede=1" % (NegAux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=any-aux=%s-licensor_embedded=0-npi_embedded=1-licensor_precede=0" % (NegAux2[0]), 0, sentence_2))
                counter += 2
            # keep track of which sentences have already been generated
            sentences.add(sentence_1)

# the end :)


# # repeat for "ever"
#
# # PITFALL:
# # ever doesn't occur with progressive
# # Every boy who has ever eaten a potato is tall.
# # *? Every boy who is ever eating a potato is tall.
sentences = set()
all_non_progressive_transitive_verbs = get_all("ing", "0", all_nonfinite_transitive_verbs)
for writer in [train_output, dev_output, test_output]:
    counter = 0
    while counter < number_to_generate:
    # sentence template
    # D1   N1   Rel Aux1    (ever)  V1      D2    N2      Aux2    (ever)  V2    D3  N3
    # the  boy  who should  (ever)  buy     some  apples  didn't  (ever)  sing  a   song

    # D1   N1   Rel Aux1    (ever)  V1   D2    N2      Aux2    (ever)  V2    D3  N3
    # the  boy  who didn't  (ever)  buy  some  apples  should  (ever)  sing  a   song

        # build all lexical items
        #TODO: throw in modifiers
        V1 = choice(all_non_progressive_transitive_verbs)
        V2 = choice(all_non_progressive_transitive_verbs, [V1])
        N1 = choice(get_matches_of(V1, "arg_1", all_frequent_nouns))
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D1 = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers))
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers))
        NegAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)))
        PosAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)))
        NegAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)), [NegAux1])
        PosAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)), [PosAux1])
        Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))

        sentence_1 = "%s %s %s %s %s %s %s %s ever %s %s %s." % (D1[0], N1[0], Rel[0], PosAux1[0], V1[0], D2[0], N2[0], NegAux2[0], V2[0], D3[0], N3[0])
        sentence_2 = "%s %s %s %s ever %s %s %s %s %s %s %s." % (D1[0], N1[0], Rel[0], PosAux1[0], V1[0], D2[0], N2[0], NegAux2[0], V2[0], D3[0], N3[0])
        sentence_3 = "%s %s %s %s %s %s %s %s ever %s %s %s." % (D1[0], N1[0], Rel[0], NegAux1[0], V1[0], D2[0], N2[0], PosAux2[0], V2[0], D3[0], N3[0])
        sentence_4 = "%s %s %s %s ever %s %s %s %s %s %s %s." % (D1[0], N1[0], Rel[0], NegAux1[0], V1[0], D2[0], N2[0], PosAux2[0], V2[0], D3[0], N3[0])

        # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
        # but the code outputs a determiner with an empty string. might want to change this)
        sentence_1 = string_beautify(sentence_1)
        sentence_2 = string_beautify(sentence_2)
        sentence_3 = string_beautify(sentence_3)
        sentence_4 = string_beautify(sentence_4)

        if sentence_1 not in sentences:
            if writer == test_output:
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=ever-aux=%s-licensor_embedded=0-npi_embedded=0-licensor_precede=1" % (NegAux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=ever-aux=%s-licensor_embedded=0-npi_embedded=1-licensor_precede=0" % (NegAux2[0]), 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=ever-aux=%s-licensor_embedded=1-npi_embedded=0-licensor_precede=1" % (NegAux1[0]), 0, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=ever-aux=%s-licensor_embedded=1-npi_embedded=1-licensor_precede=1" % (NegAux1[0]), 1, sentence_4))
                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
            else:
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=ever-aux=%s-licensor_embedded=0-npi_embedded=0-licensor_precede=1" % (NegAux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=ever-aux=%s-licensor_embedded=0-npi_embedded=1-licensor_precede=0" % (NegAux2[0]), 0, sentence_2))
                counter += 2
            # keep track of which sentences have already been generated
            sentences.add(sentence_1)


# # repeat for "yet"
#
# # PITFALL:
# # ever doesn't occur with progressive
# # Every boy who has ever eaten a potato is tall.
# # *? Every boy who is ever eating a potato is tall.
sentences = set()
for writer in [train_output, dev_output, test_output]:
    counter = 0
    while counter < number_to_generate:
    # sentence template
    # D1   N1   Rel Aux1    V1   D2    N2      (yet)  Aux2    V2    D3  N3    (yet)
    # the  boy  who should  buy  some  apples  (yet)  didn't  sing  a   song  (yet)

    # D1   N1   Rel Aux1    V1   D2    N2      (yet)  Aux2    V2    D3  N3    (yet)
    # the  boy  who didn't  buy  some  apples  (yet)  should  sing  a   song  (yet)

        # build all lexical items
        #TODO: throw in modifiers
        V1 = choice(all_nonfinite_transitive_verbs)
        V2 = choice(all_nonfinite_transitive_verbs, [V1])
        N1 = choice(get_matches_of(V1, "arg_1", all_frequent_nouns))
        N2 = choice(get_matches_of(V1, "arg_2", all_non_singular_nouns), [N1])
        N3 = choice(get_matches_of(V2, "arg_2", all_non_singular_nouns), [N1, N2])
        D1 = choice(get_matched_by(N1, "arg_1", all_UE_UE_quantifiers))
        D2 = choice(get_matched_by(N2, "arg_1", all_UE_UE_quantifiers))
        D3 = choice(get_matched_by(N3, "arg_1", all_UE_UE_quantifiers))
        NegAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)))
        PosAux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)))
        NegAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_negative_auxiliaries)), [NegAux1])
        PosAux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_non_negative_auxiliaries)), [PosAux1])
        Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))

        sentence_1 = "%s %s %s %s %s %s %s %s %s %s %s yet." % (D1[0], N1[0], Rel[0], PosAux1[0], V1[0], D2[0], N2[0], NegAux2[0], V2[0], D3[0], N3[0])
        sentence_2 = "%s %s %s %s %s %s %s yet %s %s %s %s." % (D1[0], N1[0], Rel[0], PosAux1[0], V1[0], D2[0], N2[0], NegAux2[0], V2[0], D3[0], N3[0])
        sentence_3 = "%s %s %s %s %s %s %s %s %s %s %s yet." % (D1[0], N1[0], Rel[0], NegAux1[0], V1[0], D2[0], N2[0], PosAux2[0], V2[0], D3[0], N3[0])
        sentence_4 = "%s %s %s %s %s %s %s yet %s %s %s %s." % (D1[0], N1[0], Rel[0], NegAux1[0], V1[0], D2[0], N2[0], PosAux2[0], V2[0], D3[0], N3[0])

        # remove doubled up spaces (this is because the bare plural doesn't have a determiner,
        # but the code outputs a determiner with an empty string. might want to change this)
        sentence_1 = string_beautify(sentence_1)
        sentence_2 = string_beautify(sentence_2)
        sentence_3 = string_beautify(sentence_3)
        sentence_4 = string_beautify(sentence_4)

        if sentence_1 not in sentences:
            if writer == test_output:
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=yet-aux=%s-licensor_embedded=0-npi_embedded=0-licensor_precede=1" % (NegAux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=yet-aux=%s-licensor_embedded=0-npi_embedded=1-licensor_precede=0" % (NegAux2[0]), 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=yet-aux=%s-licensor_embedded=1-npi_embedded=0-licensor_precede=1" % (NegAux1[0]), 0, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=yet-aux=%s-licensor_embedded=1-npi_embedded=1-licensor_precede=1" % (NegAux1[0]), 1, sentence_4))
                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
            else:
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=yet-aux=%s-licensor_embedded=0-npi_embedded=0-licensor_precede=1" % (NegAux2[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("experiment=npi_scope-npi=yet-aux=%s-licensor_embedded=0-npi_embedded=1-licensor_precede=0" % (NegAux2[0]), 0, sentence_2))
                counter += 2
            # keep track of which sentences have already been generated
            sentences.add(sentence_1)



train_output.close()
test_output.close()
test2_output.close()
dev_output.close()
