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
    D = choice(get_matched_by(object, "arg_1", get_all_conjunctive([("category", "(S/(S\\NP))/N"), ("common", '1')])))
    conjugate(V, subject)
    V["expression"] = "%s %s %s" % (V[0], D[0], object[0])
    V["category"] = "S\\NP"
    V["category_2"] = "VP"
    V["arg_2"] = ""

    # TODO: intransitive VP
    # TODO: ditransitive VP

    return V



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


# test

for i in range(1000):
    N = choice(get_all("animate", "1"))
    rc = subject_relative_clause(N)
    print(N[0], rc[0])

pass