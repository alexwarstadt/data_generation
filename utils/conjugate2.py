from utils.vocab_table import *
from random import choice
from utils.vocab_table import *
import random
from pattern.en import conjugate as pconj
import pattern.en
# can be installed via "pip install pattern"
# Reference: De Smedt, T. & Daelemans, W. (2012).
# Pattern for Python. Journal of Machine Learning Research, 13: 2031–2035.
# https://www.clips.uantwerpen.be/pattern

def conjugate2(verb, subj, aux=2, t=3, m="INDICATIVE",neg=0): # TODO: Does not work with the verbs that are coded with prepositions.
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param aux: 0 = no aux, 1 = aux, 2 = random
    :param t:  0 = prs, 1 = pst, 2 = fut, 3 = random (present or past)
    :param neg: 0 = no neg, 1 = neg, 2 = random
    :return: none, side effects only. Modifies string of verb to be inflected for tense/aspect (includes the auxiliary in the string)
    # TODO: Adverbs?
    """
    auxiliaries = ["have", "be", "will"] # perfect, imperfective, future
    tenses = ["present", "past"]
    the_person = 3
    if subj["pl"] == 1 or subj["pl"] == "1": # TODO Workaround for a bug where this is sometimes int and sometimes str?
        the_number = "plural"
    else:
        the_number = "singular"
    the_verb = pattern.en.lemma(verb[0])

    if aux == 2: # If aux is random, select +- aux
        aux = random.randint(0, 1)

    if neg == 2: # Same for negation
        neg = random.randint(0, 1)

    if t == 0:
        the_tense = tenses[0]
    elif t == 1:
        the_tense = tenses[1]
    elif t == 2:
        the_aux = "will"
        the_tense = "infinitive"
        aux = 4 # future tense
    elif t == 3:
        the_tense = random.choice(tenses)

    if aux == 1:
        the_aux = random.choice(auxiliaries)
        if the_aux == "have": # perfect
            the_verb = pconj(the_verb, "ppart")
            the_aux = pconj(the_aux, person = the_person, number = the_number, tense = the_tense)
        elif the_aux == "be": # imperfective # TODO: Verbs that don't take a progressive form, see research Q. Needs to be indicated in the vocabulary
            the_verb = pconj(the_verb, "part")
            the_aux = pconj(the_aux, person = the_person, number = the_number, tense = the_tense)
    elif aux == 4: # future
        the_verb = pconj(the_verb, "infinitive")
    elif aux == 0:
        the_verb = pconj(the_verb, person=the_person, number=the_number, tense=the_tense)
    # Alright, configured aux and tense, on to negation..
    if neg == 0:
        if aux == 1:
            verb[0] = the_aux + " " + the_verb
        else:
            verb[0] = the_verb
    if neg == 1:
        if aux == 1:
            verb[0] = the_aux + " not " + the_verb
        else:
            verb[0] = pconj("do", person = the_person, number = the_number, tense = the_tense) + " not " + pconj(the_verb, "infinitive") # do support


# Debug / Test
for i in range (0,150):
    subject = choice(get_all("category", "N"))
    someverb = choice(get_all("category", "(S\\NP)/NP"))
    conjugate2(someverb, subject)
    print(subject[0] + " " + someverb[0])