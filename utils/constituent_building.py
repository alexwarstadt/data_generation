# Authors: Alex Warstadt
# Script for generating NPI sentences with quantifiers as licensors

# TODO: document metadata

from utils.vocab_table import *
from utils.conjugate import *
from utils.data_type import data_type
from random import choice
from utils.string_utils import remove_extra_whitespace
import numpy as np
import random



def verb_phrase_from_subj(subject):
    # x = random.random()
    # if x < 1/3:

    # transitive VP
    V = choice(get_matched_by(subject, "arg_1", get_all("category", "(S\\NP)/NP")))
    object = choice(get_matches_of(V, "arg_2", get_all("category", "N")))
    D = choice(get_matched_by(object, "arg_1", get_all_conjunctive([("category", "(S/(S\\NP))/N"), ("frequent", '1')])))
    conjugate(V, subject)
    V["expression"] = "%s %s %s" % (V[0], D[0], object[0])
    V["category"] = "S\\NP"
    V["category_2"] = "VP"
    V["arg_2"] = ""

    # TODO: intransitive VP
    # TODO: ditransitive VP

    return V

def verb_args_from_verb(verb, frequent=True):
    """
    :param verb: 
    :param frequent: 
    :return: dict of all arguments of verb: {subject:x1, auxiliary:x2, ...]
    """
    # all verbs have a subject
    if frequent:
        try:
            subj = choice(get_matches_of(verb, "arg_1", get_all_conjunctive([("category", "N"), ("frequent", "1")])))
        except IndexError:
            pass
    else:
        subj = choice(get_matches_of(verb, "arg_1", get_all("category", "N")))
    N_to_DP_mutate(subj)

    # all verbs have an auxiliary (or null)
    aux = return_aux(verb, subj)

    # transitive verbs
    if verb["category"] == "(S\\NP)/NP":
        if frequent:
            obj = choice(get_matches_of(verb, "arg_2", get_all_conjunctive([("category", "N"), ("frequent", "1")])))
        else:
            obj = choice(get_matches_of(verb, "arg_1", get_all("category", "N")))
        N_to_DP_mutate(obj)
        return {"subject": subj, "auxiliary": aux, "object": obj}



def N_to_DP(noun, frequent=True):
    """
    :param noun: noun to turn into DP
    :param frequent: restrict to frequent determiners only?
    :return: matching determiner, without noun
    """
    if frequent:
        D = choice(get_matched_by(noun, "arg_1", get_all_conjunctive([("category", "(S/(S\\NP))/N"), ("frequent", '1')])))
    else:
        D = choice(get_matched_by(noun, "arg_1", get_all_conjunctive([("category", "(S/(S\\NP))/N"), ("frequent", '1')])))
    return D

def N_to_DP_mutate(noun, frequent=True):
    """
    :param noun: noun to turn into DP
    :param frequent: restrict to frequent determiners only?
    :return: NONE. mutates string of noun.
    """
    D = N_to_DP(noun, frequent)
    noun[0] = D[0] + " " + noun[0]
    return noun





def subject_relative_clause(noun):
    """
    :param noun: noun to be modified (subject of RC)
    :return: relative clause (without modified noun)
    """
    # boy who ate the apple
    # N   rel V1  D1  N2
    rel = choice(get_matched_by(noun, "arg_1", get_all("category_2", "rel")))
    VP = verb_phrase_from_subj(noun)
    VP[0] = remove_extra_whitespace("%s %s" % (rel[0], VP[0]))
    #TODO: properties of VP might not be correct for RC
    return VP


def get_reflexive(noun):
    themselves = get_all("expression", "themselves")[0]
    matches = get_matched_by(noun, "arg_1", get_all("category_2", "refl"))
    while True:
        reflexive = choice(matches)
        if reflexive is not themselves:
            return reflexive
        elif noun["pl"] == "1":
            return reflexive
        else:
            pass    # if singular "themselves" was chosen try again


# test

# tvs = get_all("category", "(S\\NP)/NP")
#
# for tv in tvs:
#     args = verb_args_from_verb(tv)
#     print(" ".join([args["subject"][0], args["auxiliary"][0], tv[0], args["object"][0]]))

# for i in range(1000):
#     N = choice(get_all("animate", "1", get_all("category", "N")))
#     rc = subject_relative_clause(N)
#     print(N[0], rc[0])

pass