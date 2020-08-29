# Author: Alex Warstadt
# Script for generating Chomsky's "structure dependent" sentences for QP1
# Loosens some restrictions from polar_q so that complementizer + finite verb is not such a reliable cue

from utils.conjugate import *
from utils.constituent_building import verb_args_from_verb
from utils.constituent_building import N_to_DP_mutate
from utils.randomize import choice
import numpy as np
from utils.string_utils import string_beautify
from functools import reduce
import traceback
import random


# initialize output file
rel_output_path = "outputs/subject_aux_inversion"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
train_output = open(os.path.join(project_root, rel_output_path, "train.tsv"), "w")
test_output = open(os.path.join(project_root, rel_output_path, "test_full.tsv"), "w")
test2_output = open(os.path.join(project_root, rel_output_path, "test.tsv"), "w")
dev_output = open(os.path.join(project_root, rel_output_path, "dev.tsv"), "w")

# set total number of sentences to generate
number_to_generate = 10000
sentences = set()
counter = 0    # Jiant requires test data to be in numbered, two-column format

def get_all_verb_forms(verb):
    return get_all("root", verb["root"])

def get_all_verb_forms_list(verb_list):
    return np.array(list(reduce(lambda x, y: np.union1d(x, y), [get_all_verb_forms(v) for v in verb_list])))

# gather word classes that will be accessed frequently
all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
# all_singular_nouns = get_all("sg", "0", all_nouns)
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_possible_transitive_subjects = np.array(list(reduce(lambda x, y: np.union1d(x, y), [get_matches_of(v, "arg_1", all_nouns) for v in all_transitive_verbs])))
all_intransitive_verbs = get_all("category", "S\\NP")
all_verbs = np.union1d(all_transitive_verbs, all_intransitive_verbs)
all_non_finite_verbs =  get_all("finite", "0", all_verbs)
all_finite_verbs =  get_all("finite", "1", all_verbs)
all_frontable_aux = get_all("frontable", "1") #TODO: don't worry about frontable aux
all_pres_plural_verbs = get_all_conjunctive([("pres", "1"), ("3sg", "0")], all_verbs)
all_homophonous_verbs = get_all("homophonous", "1")
all_bare_verbs = get_all("bare", "1")
all_en_verbs = get_all("en", "1")

all_non_finite_transitive_verbs = np.intersect1d(all_non_finite_verbs, all_transitive_verbs)
all_finite_transitive_verbs = np.intersect1d(all_finite_verbs, all_transitive_verbs)
all_non_homophonous_finite_transitive_verbs = np.setdiff1d(all_finite_transitive_verbs, all_homophonous_verbs)
all_finite_non_present_plural_transitive_verbs = np.setdiff1d(all_finite_transitive_verbs, all_pres_plural_verbs)
all_non_bare_non_finite_transitive_verbs = np.setdiff1d(all_non_finite_transitive_verbs, all_bare_verbs)
all_non_en_non_finite_transitive_verbs = np.setdiff1d(all_non_finite_transitive_verbs, all_en_verbs)


animate_noun = choice(get_all("animate", "1"))
document_noun = choice(get_all("document", "1"))
all_consistent_transitive_verbs = np.union1d(
    get_all_verb_forms_list(get_matched_by(animate_noun, "arg_1", get_matched_by(animate_noun, "arg_2", all_transitive_verbs))),
    get_all_verb_forms_list(get_matched_by(document_noun, "arg_1", get_matched_by(document_noun, "arg_2", all_transitive_verbs)))
)
all_consistent_finite_transitive_verbs = np.intersect1d(all_finite_verbs, all_consistent_transitive_verbs)
all_consistent_non_finite_transitive_verbs = np.intersect1d(all_non_finite_verbs, all_consistent_transitive_verbs)
all_non_homophonous_consistent_finite_transitive_verbs = np.setdiff1d(all_consistent_finite_transitive_verbs, all_homophonous_verbs)
all_consistent_finite_non_present_plural_transitive_verbs = np.setdiff1d(all_consistent_finite_transitive_verbs, all_pres_plural_verbs)

# sample sentences until desired number

def sample_2_2():
    # Aux1/2 D1  N1  who Aux1  V1    D2  N2  Aux2 V2      D3  N3
    # is/has the man who (has) met   the boy (is) kissing the patient ?

    # Aux1/2 D1  N1  Aux2 V2      D3  N3      who Aux2  V2    D2  N2
    # is/has the man (is) kissing the patient who (has) met   the boy ?

    # The arguments of V2 must match in animacy/number
    V2 = choice(all_consistent_non_finite_transitive_verbs)
    N1 = choice(get_matches_of(V2, "arg_1", all_nouns))
    V1 = choice(get_matched_by(N1, "arg_1", all_non_finite_transitive_verbs))
    Aux1 = choice(get_matched_by(V1, "arg_2", get_matched_by(N1, "arg_1", all_frontable_aux)))
    N3 = choice(
        get_matched_by(V2, "arg_2",
                       get_matched_by(V1, "arg_1",
                                      get_matches_of(Aux1, "arg_1",
                                                     get_all_conjunctive([("animate", N1["animate"]), ("document", N1["document"])], all_nouns)))),
        [N1])

    N2 = choice(get_matches_of(V1, "arg_2", all_nouns), [N1, N3])
    N1 = N_to_DP_mutate(N1)
    N2 = N_to_DP_mutate(N2)
    N3 = N_to_DP_mutate(N3)
    Aux2 = choice(get_matched_by(V2, "arg_2", get_matched_by(N1, "arg_1", all_frontable_aux)), [Aux1])
    Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))

    sentence_1 = "%s %s %s %s %s %s %s %s?" % (Aux2[0], N1[0], Rel[0], Aux1[0], V1[0], N2[0], V2[0], N3[0])
    sentence_2 = "%s %s %s %s %s %s %s %s?" % (Aux1[0], N1[0], Rel[0], V1[0], N2[0], Aux2[0], V2[0], N3[0])
    sentence_3 = "%s %s %s %s %s %s %s %s?" % (Aux2[0], N1[0], V2[0], N3[0], Rel[0], Aux1[0], V1[0], N2[0])
    sentence_4 = "%s %s %s %s %s %s %s %s?" % (Aux1[0], N1[0], Aux2[0], V2[0], N3[0], Rel[0], V1[0], N2[0])
    return sentence_1, sentence_2, sentence_3, sentence_4


def sample_1_1():
    # Aux2 D1  N1  who V1_f D2  N2  V2_nf   D3  N3                  1 aux
    # Are  the men who met  the boy kissing the patient ?

    # Aux1 D1  N1  who V1_nf D2  N2  V2_f     D3  N3                1 aux
    # Will the men who meet  the boy kissed the patient ?

    # Aux2 D1  N1  V2_nf   D3  N3      who V1_f D2  N2              1 aux
    # Are  the men kissing the patient who met  the boy ?

    # Aux1 D1  N1  V2_f   D3  N3      who V1_nf D2  N2              1 aux
    # Will the men kissed the patient who meet  the boy ?

    # Fail conditions:
    # V1_f = pres.pl, V2_nf = bare
    # V1_f = past.homo, V2_nf = en
    # V2_f = pres.pl, V1_nf = bare
    # V2_f = past.homo, V1_nf = en

    V2_f = choice(all_consistent_finite_transitive_verbs)
    V2_nf = choice(np.intersect1d(get_all_verb_forms(V2_f), all_consistent_non_finite_transitive_verbs))
    N1 = choice(get_matches_of(V2_f, "arg_1"))

    if V2_nf["bare"] == "1":  # V1_f = pres.pl, V2_nf = bare
        try:
            V1_f = choice(get_matched_by(N1, "arg_1", all_finite_non_present_plural_transitive_verbs))
        except Exception:
            pass
    elif V2_nf["en"] == "1":  # V1_f = past.homo, V2_nf = en
        V1_f = choice(get_matched_by(N1, "arg_1", all_non_homophonous_finite_transitive_verbs))
    else:
        V1_f = choice(get_matched_by(N1, "arg_1", all_finite_transitive_verbs))

    if V2_f["pres"] == "1" and V2_f["3sg"] == "0":  # V2_f = pres.pl, V1_nf = bare
        V1_nf = choice(get_matched_by(N1, "arg_1", np.intersect1d(get_all_verb_forms(V1_f), all_non_bare_non_finite_transitive_verbs)))
    elif V2_f["pres"] == "0" and V2_f["homophonous"] == "1":  # V2_f = past.homo, V1_nf = en
        V1_nf = choice(get_matched_by(N1, "arg_1", np.intersect1d(get_all_verb_forms(V1_f), all_non_en_non_finite_transitive_verbs)))
    else:
        V1_nf = choice(get_matched_by(N1, "arg_1", np.intersect1d(get_all_verb_forms(V1_f), all_non_finite_transitive_verbs)))

    Aux1 = return_aux(V1_nf, N1)
    N3 = choice(
        get_matched_by(V2_f, "arg_2",
                       get_matched_by(V1_f, "arg_1",
                                      get_matches_of(Aux1, "arg_1",
                                                     get_all_conjunctive([("animate", N1["animate"]), ("document", N1["document"])], all_nouns)))),
        [N1])
    try:
        N2 = choice(get_matches_of(V1_f, "arg_2", all_nouns), [N1, N3])
    except Exception:
        pass
    N1 = N_to_DP_mutate(N1)
    N2 = N_to_DP_mutate(N2)
    N3 = N_to_DP_mutate(N3)
    Aux2 = return_aux(V2_nf, N1)
    Rel = choice(get_matched_by(N1, "arg_1", get_matched_by(N3, "arg_1", get_all("category_2", "rel"))))

    sentence_1 = " ".join([Aux2[0], N1[0], Rel[0], V1_f[0], N2[0], V2_nf[0], N3[0], "?"])
    sentence_2 = " ".join([Aux1[0], N1[0], Rel[0], V1_nf[0], N2[0], V2_f[0], N3[0], "?"])
    sentence_3 = " ".join([Aux2[0], N1[0], V2_nf[0], N3[0], Rel[0], V1_f[0], N2[0], "?"])
    sentence_4 = " ".join([Aux1[0], N1[0], V2_f[0], N3[0], Rel[0], V1_nf[0], N2[0], "?"])
    return sentence_1, sentence_2, sentence_3, sentence_4



for writer in [test_output, train_output, dev_output]:
    counter = 0
    while counter < number_to_generate:
        try:
            if random.choice([True, False]):
                sentence_1, sentence_2, sentence_3, sentence_4 = sample_1_1()
                template = "1_aux_per_sentence"
            else:
                sentence_1, sentence_2, sentence_3, sentence_4 = sample_2_2()
                template = "2_aux_per_sentence"
        except Exception as e:
            print("".join(traceback.format_tb(e.__traceback__)) + str(e))
            continue
        sentence_1 = string_beautify(sentence_1)
        sentence_2 = string_beautify(sentence_2)
        sentence_3 = string_beautify(sentence_3)
        sentence_4 = string_beautify(sentence_4)

        if sentence_1 not in sentences:
            if writer == test_output:
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=1-last=1-template=%s" % template, 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=0-last=0-template=%s" % template, 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=1-last=0-template=%s" % template, 1, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=0-last=1-template=%s" % template, 0, sentence_4))
                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
                test2_output.flush()
            else:
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=1-last=1-template=%s" % template, 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=0-last=0-template=%s" % template, 0, sentence_2))
                counter += 2
            writer.flush()
        sentences.add(sentence_1)


train_output.close()
test_output.close()
test2_output.close()
dev_output.close()






"""
Think more about the paradigm

1.  1   Has the teacher [who is] praising the essay criticized the student?
2.  0   Is the teacher [who praising] the essay has criticized the student?
3.  1   Has the teacher criticized the student [who is] praising the essay?
4.  0   Is the teacher has criticized the student [who praising] the essay? 


1.  1   Has the teacher who is praising the essay has criticized the student?
2.  0   Is the teacher who is praising the essay has criticized the student?
3.  1   Has the teacher has criticized the student who is praising the essay?
4.  0   Is the teacher has criticized the student who is praising the essay? 


Question: Does the model use the bigram of complementizer + finite verb to identify grammatical sentences?
- Response 1: If this were so we would expect to see incorrect classification on ungrammatical sentences with the same bigram
- Response 2: If we eliminate this as a reliable cue...
    1.  1   Has the teacher [who praising the essay criticized the student?
    2.  0   Is the teacher [who praising] the essay has criticized the student?
    3.  1   Has the teacher criticized the student [who is] praising the essay?
    4.  0   Is the teacher has criticized the student [who praising] the essay? 



"""



