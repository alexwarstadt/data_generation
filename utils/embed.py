from random import choice
from utils.vocab_sets import *
from utils.constituent_building import *


def embed_in_question(sentence):
    V = choice(all_rogatives)
    N = N_to_DP_mutate(choice(get_matches_of(V, "arg_1", all_nouns)))
    aux = return_aux(V, N, allow_negated=False)
    return "%s %s %s whether %s" % (N[0], aux[0], V[0], sentence)


def embed_in_negation(sentence, neutral=True):
    if neutral:
        negations = ["it's not the case that",
                     "it's false that",
                     "it's not true that",
                     "it's incorrect to say that"]
    else:
        N = choice(all_proper_names)
        negations = ["it's not the case that",
                     "it's false that",
                     "it's not true that",
                     "it's incorrect to say that",
                     "it's a lie that",
                     "%s is mistaken that" % N[0],
                     "%s is wrong that" % N[0],
                     "%s lied that" % N[0],
                     "%s falsely believes that" % N[0]]
    neg = np.random.choice(negations)
    return "%s %s" % (neg, sentence)


def embed_in_modal(sentence):
    N = choice(all_proper_names)
    modals = ["it's possible that",
              "it might be true that",
              "it's conceivable that",
              "it's unlikely that",
              "it's likely that",
              "it might turn out that",
              "%s might be right that" % N[0],
              "%s believes that" % N[0],
              "%s is under the impression that" % N[0],
              "%s is probably correct that" % N[0],
              ]
    modal = np.random.choice(modals)
    return "%s %s" % (modal, sentence)


def embed_in_conditional(sentence):
    conditionals = ["if",
                    "no matter if",
                    "whether or not",
                    "assuming that",
                    "on the condition that",
                    "under the circumstances that",
                    "should it be true that",
                    "supposing that"]
    consequents = ["it is OK",
                   "it will be OK",
                   "it isn't OK",
                   "it won't be OK",
                   "we'll be fine",
                   "we won't be fine",
                   "we are fine",
                   "we aren't fine"]
    conditional = choice(conditionals)
    consequent = choice(consequents)
    if sentence.endswith("."):
        sentence = sentence[:-1]
    if random.choice([True, False]):
        return "%s %s, %s." % (conditional, sentence, consequent)
    else:
        return "%s %s %s." % (consequent, conditional, sentence)


