# Author: Alex Warstadt
# Script for generating Chomsky's "structure dependent" sentences for QP1
# Loosens some restrictions from polar_q so that complementizer + finite verb is not such a reliable cue

from utils.conjugate import *
from utils.constituent_building import verb_args_from_verb
from utils.constituent_building import N_to_DP_mutate
from utils.randomize import choice
import numpy as np
from utils.string_utils import string_beautify
import pattern.en



def get_bare_form(verb):
    words = verb[0].split(" ")
    words[0] = pattern.en.lemma(words[0])
    words[0] = \
        "escape" if words[0] == "escap" else \
        "leave" if words[0] == "left" else \
        words[0]
    try:
        to_return = get_all_conjunctive([("expression", " ".join(words)), ("bare", "1")])[0]
    except IndexError:
        pass
    return to_return



# initialize output file
rel_output_path = "outputs/alexs_qp_structure_dependence/polar_q/10k_new/CoLA/"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
train_output = open(os.path.join(project_root, rel_output_path, "train.tsv"), "w")
test_output = open(os.path.join(project_root, rel_output_path, "test_full.tsv"), "w")
test2_output = open(os.path.join(project_root, rel_output_path, "test.tsv"), "w")
dev_output = open(os.path.join(project_root, rel_output_path, "dev.tsv"), "w")

# set total number of sentences to generate
number_to_generate = 10000
sentences = set()
counter = 0    # Jiant requires test data to be in numbered, two-column format

# gather word classes that will be accessed frequently
all_nouns = get_all_conjunctive([("category", "N"), ("frequent", "1")])
all_singular_nouns = get_all("sg", "0", all_nouns)
all_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP")])
all_frontable_aux = get_all("frontable", "1")   # TODO: don't worry about frontable aux
all_aux = get_all("category", "(S\\NP)/(S[bare]\\NP)")   # TODO: don't worry about frontable aux
animate_noun = choice(get_all("expression", "actor"))
inanimate_noun = choice(get_all("expression", "movie"))
all_consistent_transitive_verbs = np.union1d(
    get_matched_by(animate_noun, "arg_1", get_matched_by(animate_noun, "arg_2", all_transitive_verbs)),
    get_matched_by(inanimate_noun, "arg_1", get_matched_by(inanimate_noun, "arg_2", all_transitive_verbs))
)

# sample sentences until desired number

for writer in [train_output, dev_output, test_output]:
    counter = 0
    while counter < number_to_generate:
        # Aux1/2 D1  N1  who Aux1  V1    D2  N2  Aux2 V2      D3  N3
        # is/has the man who (has) met   the boy (is) kissing the patient ?

        # Aux1/2 D1  N1  Aux2 V2      D3  N3      who Aux2  V2    D2  N2
        # is/has the man (is) kissing the patient who (has) met   the boy ?

        # The arguments of V2 must match in animacy/number
        try:
            V2_f = choice(all_consistent_transitive_verbs)
            V2_nf = get_bare_form(V2_f) if V2_f["finite"] == "1" else V2_f
            N1 = N_to_DP_mutate(choice(get_matches_of(V2_f, "arg_1", all_nouns)))
            V1_f = choice(get_matched_by(N1, "arg_1", all_transitive_verbs), [V2_f])
            V1_nf = get_bare_form(V1_f) if V1_f["finite"] == "1" else V1_f
            if V1_f["pres"] == V2_f["pres"] == "1" and V1_f["3sg"] == V2_f["3sg"] == "0":
                print(V1_f[0], V2_f[0])
                continue
            if (V1_f["past"] == "1" and V2_nf["en"] == "1") or (V2_f["past"] == "1" and V1_nf["en"] == "1"):
                print(V1_f[0], V2_f[0], V2_f[0], V1_f[0])
                continue
            N3 = N_to_DP_mutate(choice(np.intersect1d(get_matches_of(V2_f, "arg_2", all_nouns), get_matches_of(V1_f, "arg_1", all_nouns)), [N1]))
            N2 = N_to_DP_mutate(choice(get_matches_of(V1_f, "arg_2", all_nouns), [N1, N3]))
            Aux1_f = choice(get_matched_by(V1_f, "arg_2", get_matched_by(N1, "arg_1", all_aux)))
            Aux1_nf = choice(get_matched_by(V1_nf, "arg_2", get_matched_by(N1, "arg_1", all_aux))) if V1_f["finite"] == "1" else Aux1_f
            Aux2_f = choice(get_matched_by(V2_f, "arg_2", get_matched_by(N1, "arg_1", all_aux)))
            Aux2_nf = choice(get_matched_by(V2_nf, "arg_2", get_matched_by(N1, "arg_1", all_aux))) if V2_f["finite"] == "1" else Aux2_f
            Rel = choice(get_matched_by(N1, "arg_1", get_all("category_2", "rel")))
        except IndexError:
            print("index error")
            continue

        sentence_1 = "%s %s %s %s %s %s %s %s?" % (Aux2_nf[0], N1[0], Rel[0], Aux1_f[0], V1_f[0], N2[0], V2_nf[0], N3[0])
        sentence_2 = "%s %s %s %s %s %s %s %s?" % (Aux1_nf[0], N1[0], Rel[0], V1_nf[0], N2[0], Aux2_f[0], V2_f[0], N3[0])
        sentence_3 = "%s %s %s %s %s %s %s %s?" % (Aux2_nf[0], N1[0], V2_nf[0], N3[0], Rel[0], Aux1_f[0], V1_f[0], N2[0])
        sentence_4 = "%s %s %s %s %s %s %s %s?" % (Aux1_nf[0], N1[0], Aux2_f[0], V2_f[0], N3[0], Rel[0], V1_nf[0], N2[0])

        sentence_1 = string_beautify(sentence_1)
        sentence_2 = string_beautify(sentence_2)
        sentence_3 = string_beautify(sentence_3)
        sentence_4 = string_beautify(sentence_4)

        if sentence_1 not in sentences:
            if writer == test_output:
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=1-last=1-aux1=%s-aux2=%s" % (Aux1_f[0], Aux2_nf[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=0-last=0-aux1=%s-aux2=%s" % (Aux1_nf[0], Aux2_f[0]), 0, sentence_2))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=1-last=0-aux1=%s-aux2=%s" % (Aux1_f[0], Aux2_nf[0]), 1, sentence_3))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=0-highest=0-last=1-aux1=%s-aux2=%s" % (Aux1_nf[0], Aux2_f[0]), 0, sentence_4))
                test2_output.write("%d\t%s\n" % (counter, sentence_1))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_2))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_3))
                counter += 1
                test2_output.write("%d\t%s\n" % (counter, sentence_4))
                counter += 1
            else:
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=1-last=1-aux1=%s-aux2=%s" % (Aux1_f[0], Aux2_nf[0]), 1, sentence_1))
                writer.write("%s\t%d\t\t%s\n" % ("exp=polar-src=1-highest=0-last=0-aux1=%s-aux2=%s" % (Aux1_nf[0], Aux2_f[0]), 0, sentence_2))
                counter += 2
        sentences.add(sentence_1)
        writer.flush()


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



