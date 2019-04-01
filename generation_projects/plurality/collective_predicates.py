# Authors: Hagen Blix
# Script for generating sentences with collective predicates

# import pattern.en
# from pattern.en import conjugate as pconj
from utils.conjugate2 import *
from utils.string_utils import remove_extra_whitespace
from random import choice
import numpy as np
import os


# initialize output file
rel_output_path = "outputs/plurals/environment=collectivepredicates.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of paradigms to generate
number_to_generate = 2000
sentences = set()



# gather word classes that will be accessed frequently
all_irregular_nouns = get_all_conjunctive([("category", "N"), ("irrpl", "1")])
# all_irregular_nouns_pl = get_all("pl", "1", all_irregular_nouns)
all_regular_nouns = get_all_conjunctive([("category", "N"), ("irrpl", "")])
all_regular_nouns_sg = get_all("sg", "1", all_regular_nouns)
all_regular_nouns_animate = get_all("animate", "1", all_regular_nouns_sg)
all_regular_nouns_inanimate = get_all("animate", "0", all_regular_nouns_sg)
# all_regular_nouns_pl = get_all("pl", "1", all_regular_nouns)
all_coll_pred = get_all("category_2", "IV_ag_pl")
all_ncoll_pred = get_all("category_2", "IV_ag")

while len(sentences) < number_to_generate/3:

    Nirr_sg = choice(all_irregular_nouns)
    while Nirr_sg["sgequalspl"] == "1": # Exclude sg=pl nouns
        Nirr_sg = choice(all_irregular_nouns)

    Nirr_pl = Nirr_sg.copy()
    Nirr_pl[0] = Nirr_pl["pluralform"]
    Nirr_pl["sg"] = 0
    Nirr_pl["pl"] = 1

    if Nirr_sg["animate"] == "1":
        Nreg_sg = choice(all_regular_nouns_animate)
        while " " in Nreg_sg:
            Nreg_sg = choice(all_regular_nouns_animate)
    else:
        Nreg_sg = choice(all_regular_nouns_inanimate)
        while " " in Nreg_sg:
            Nreg_sg = choice(all_regular_nouns_inanimate)
    Nreg_pl = Nreg_sg.copy()
    Nreg_pl[0] = pattern.en.pluralize(Nreg_pl[0])
    Nreg_pl["sg"] = 0
    Nreg_pl["pl"] = 1


    # Apparently this isn't coded?
    # coll_pred = choice(get_matched_by(Nirr_sg, "arg_1", all_coll_pred))
    # ncoll_pred = choice(get_matched_by(Nirr_sg, "arg_1", all_ncoll_pred))
    coll_pred = choice(all_coll_pred)
    ncoll_pred = choice(all_ncoll_pred)

    while " " in ncoll_pred[0]:
        ncoll_pred = choice(all_ncoll_pred) # Avoid things I can't inflect
    # TODO Doesn't match the noun and the verb for animacy etc?
    # TODO: You might want to exhaust the list of irregular nouns?

    # Determiners (just strings):
    definiteness = np.random.choice([True, False])

    if definiteness:
    # Definites:
        det_def_abstract = np.random.choice([1, 2, 3], p=[0.9, 0.05, 0.05])
        if det_def_abstract == 1:
            Dreg_sg = "the"
            Dirr_sg = "the"
            Dreg_pl = "the"
            Dirr_pl = "the"
        elif det_def_abstract == 2:
            Dreg_sg = "this"
            Dirr_sg = "this"
            Dreg_pl = "these"
            Dirr_pl = "these"
        elif det_def_abstract == 3:
            Dreg_sg = "that"
            Dirr_sg = "that"
            Dreg_pl = "those"
            Dirr_pl = "those"
    else:
    # Indefinites:
        det_indef_abstract = np.random.choice([True, False], p=[0.85, 0.15])  # True = indef article, False = some
        if det_indef_abstract:
            Dreg_pl = ""
            try:
                if Nreg_sg["start_with_vowel"] == 1:
                    Dreg_sg = "an"
                else:
                    Dreg_sg = "a"

            except:
                if Nreg_sg[0][0] in ["a", "e", "i", "o"]:
                    Dreg_sg = "an"
                else:
                    Dreg_sg = "a"

            if Nirr_sg[0][0] in ["a", "e", "i", "o"]:
                Dirr_sg = "an"
            else:
                Dirr_sg = "a"
            Dirr_pl = ""
        else:
            Dreg_sg = "some"
            Dirr_sg = "some"
            Dreg_pl = "some"
            Dirr_pl = "some"


    # Build Paradigms
    # Step 1: Generate conjugation pattern:
    the_aux = np.random.choice([0,1])
    the_tense = np.random.choice([0,1])
    the_neg = np.random.choice([0,1], p=[0.8, 0.2])
    if the_tense == 0:
        tensestring = "true"
    else:
        tensestring = "false"

    copy_verb = coll_pred.copy()
    conjugate2(copy_verb,Nreg_sg,the_aux,the_tense,the_neg)
    sentence_1 = remove_extra_whitespace(Dreg_sg + " " + Nreg_sg[0] + " " + copy_verb[0])
    sentence_1_meta = "experiment=plurals_env=collective_predicates_reg=1_sg=1_coll=1" + "_present=" + tensestring
    sentence_1_grammaticality = 0

    copy_verb = ncoll_pred.copy()
    conjugate2(copy_verb,Nreg_sg,the_aux,the_tense,the_neg)
    sentence_2 = remove_extra_whitespace(Dreg_sg + " " + Nreg_sg[0] + " " + copy_verb[0])
    sentence_2_meta = "experiment=plurals_env=collective_predicates_reg=1_sg=1_coll=0" + "_present=" + tensestring
    sentence_2_grammaticality = 1

    copy_verb = coll_pred.copy()
    conjugate2(copy_verb, Nreg_pl, the_aux, the_tense, the_neg)
    sentence_3 = remove_extra_whitespace(Dreg_pl + " " + Nreg_pl[0] + " " + copy_verb[0])
    sentence_3_meta = "experiment=plurals_env=collective_predicates_reg=1_sg=0_coll=1" + "_present=" + tensestring
    sentence_3_grammaticality = 1

    copy_verb = ncoll_pred.copy()
    conjugate2(copy_verb, Nreg_pl, the_aux, the_tense, the_neg)
    sentence_4 = remove_extra_whitespace(Dreg_pl + " " + Nreg_pl[0] + " " + copy_verb[0])
    sentence_4_meta = "experiment=plurals_env=collective_predicates_reg=1_sg=0_coll=0" + "_present=" + tensestring
    sentence_4_grammaticality = 1

    copy_verb = coll_pred.copy()
    conjugate2(copy_verb, Nirr_sg, the_aux, the_tense, the_neg)
    sentence_5 = remove_extra_whitespace(Dirr_sg + " " + Nirr_sg[0] + " " + copy_verb[0])
    sentence_5_meta = "experiment=plurals_env=collective_predicates_reg=0_sg=1_coll=1" + "_present=" + tensestring
    sentence_5_grammaticality = 0

    copy_verb = ncoll_pred.copy()
    conjugate2(copy_verb, Nirr_sg, the_aux, the_tense, the_neg)
    sentence_6 = remove_extra_whitespace(Dirr_sg + " " + Nirr_sg[0] + " " + copy_verb[0])
    sentence_6_meta = "experiment=plurals_env=collective_predicates_reg=0_sg=1_coll=0" + "_present=" + tensestring
    sentence_6_grammaticality = 1

    copy_verb = coll_pred.copy()
    conjugate2(copy_verb, Nirr_pl, the_aux, the_tense, the_neg)
    sentence_7 = remove_extra_whitespace(Dirr_pl + " " + Nirr_pl[0] + " " + copy_verb[0])
    sentence_7_meta = "experiment=plurals_env=collective_predicates_reg=0_sg=0_coll=1" + "_present=" + tensestring
    sentence_7_grammaticality = 1

    copy_verb = ncoll_pred.copy()
    conjugate2(copy_verb, Nirr_pl, the_aux, the_tense, the_neg)
    sentence_8 = remove_extra_whitespace(Dirr_pl + " " + Nirr_pl[0] + " " + copy_verb[0])
    sentence_8_meta = "experiment=plurals_env=collective_predicates_reg=0_sg=0_coll=0" + "_present=" + tensestring
    sentence_8_grammaticality = 1


    if sentence_1 not in sentences and sentence_2 not in sentences and sentence_5 not in sentences:
        # sentences 1-4 have quantifiers with UE restrictor
        output.write("%s\t%d\t\t%s\n" % (sentence_1_meta, sentence_1_grammaticality, sentence_1))
        output.write("%s\t%d\t\t%s\n" % (sentence_2_meta, sentence_2_grammaticality, sentence_2))
        output.write("%s\t%d\t\t%s\n" % (sentence_3_meta, sentence_3_grammaticality, sentence_3))
        output.write("%s\t%d\t\t%s\n" % (sentence_4_meta, sentence_4_grammaticality, sentence_4))
        output.write("%s\t%d\t\t%s\n" % (sentence_5_meta, sentence_5_grammaticality, sentence_5))
        output.write("%s\t%d\t\t%s\n" % (sentence_6_meta, sentence_6_grammaticality, sentence_6))
        output.write("%s\t%d\t\t%s\n" % (sentence_7_meta, sentence_7_grammaticality, sentence_7))
        output.write("%s\t%d\t\t%s\n" % (sentence_8_meta, sentence_8_grammaticality, sentence_8))


    # keep track of which sentences have already been generated
    sentences.add(sentence_1)
    sentences.add(sentence_2)
    sentences.add(sentence_5)



output.close()