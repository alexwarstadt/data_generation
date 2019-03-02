from utils.vocab_table import *
from random import choice

all_auxiliaries = get_all("category", "(S\\NP)/(S[bare]\\NP)")

def conjugate(verb, subj):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :return: none, side effects only. Modifies string of verb to include
    """
    # if verb["finite"] == "1":
    #     return
    # else:
    subj_agree_auxiliaries = get_matched_by(subj, "arg_2", all_auxiliaries)
    verb_agree_auxiliaries = get_matched_by(verb, "arg_1", subj_agree_auxiliaries)
    aux = choice(verb_agree_auxiliaries)
    verb[0] = aux[0] + " " + verb[0]


def return_aux(verb, subj):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :return: auxiliary that agrees with verb, or none if no auxiliary is needed.
    """
    # if verb["finite"] == "1":
    #     return None
    # else:
    subj_agree_auxiliaries = get_matched_by(subj, "arg_2", all_auxiliaries)
    verb_agree_auxiliaries = get_matched_by(verb, "arg_1", subj_agree_auxiliaries)
    aux = choice(verb_agree_auxiliaries)
    return aux
