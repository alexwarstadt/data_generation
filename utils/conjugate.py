from utils.vocab_table import *
from random import choice

all_auxiliaries = get_all("category", "(S\\NP)/(S[bare]\\NP)")
all_non_negative_auxiliaries = get_all("negated", "0", all_auxiliaries)
all_negative_auxiliaries = get_all("negated", "1", all_auxiliaries)

all_aux = get_all("category_2", "aux")
all_agreeing_aux = np.setdiff1d(all_aux, get_all("arg_1", "sg=1;sg=0"))
all_non_negative_agreeing_aux = get_all("negated", "0", all_agreeing_aux)
all_negative_agreeing_aux = get_all("negated", "1", all_agreeing_aux)

all_auxiliaries_no_null = np.setdiff1d(all_auxiliaries, get_all("expression", ""))
all_non_negative_auxiliaries_no_null = np.intersect1d(all_non_negative_auxiliaries, all_auxiliaries_no_null)
all_negative_auxiliaries_no_null = np.intersect1d(all_negative_auxiliaries, all_auxiliaries_no_null)

all_copulas =  get_all("category_2", "copula")
all_non_negative_copulas = get_all("negated", "0", all_copulas)
all_negative_copulas = get_all("negated", "1", all_copulas)

def conjugate(verb, subj, allow_negated=True, require_negated=False):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: are negated auxiliaries (e.g. shouldn't) allowed
    :return: copy of verb with modified string to include auxiliary
    """
    if allow_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_auxiliaries)
    else:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_non_negative_auxiliaries)

    if require_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_negative_auxiliaries)

    verb_agree_auxiliaries = get_matched_by(verb, "arg_2", subj_agree_auxiliaries)
    aux = choice(verb_agree_auxiliaries)
    verb = verb.copy()
    verb[0] = aux[0] + " " + verb[0]
    return verb


def return_aux(verb, subj, allow_negated=True, require_negated=False):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: are negated auxiliaries (e.g. shouldn't) allowed
    :return: auxiliary that agrees with verb, or none if no auxiliary is needed.
    """
    if allow_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_auxiliaries)
    else:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_non_negative_auxiliaries)

    if require_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_negative_auxiliaries)

    verb_agree_auxiliaries = get_matched_by(verb, "arg_2", subj_agree_auxiliaries)
    try:
        aux = choice(verb_agree_auxiliaries)
    except IndexError:
        pass
    return aux

def return_copula(subj, allow_negated=True, require_negated=False):
    if allow_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_copulas)
    else:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_non_negative_copulas)
    if require_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_negative_copulas)
    aux = choice(subj_agree_auxiliaries)
    return aux


def require_aux(verb, subj, allow_negated=True, require_negated=False):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: are negated auxiliaries (e.g. shouldn't) allowed
    :return: auxiliary that agrees with verb, or none if no auxiliary is needed.
    """
    if allow_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_auxiliaries_no_null)
    else:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_non_negative_auxiliaries_no_null)

    if require_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_negative_auxiliaries_no_null)

    verb_agree_auxiliaries = get_matched_by(verb, "arg_2", subj_agree_auxiliaries)
    aux = choice(verb_agree_auxiliaries)
    return aux

def require_aux_agree(verb, subj, allow_negated=True):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: are negated auxiliaries (e.g. shouldn't) allowed
    :return: auxiliary that agrees with verb
    """
    if allow_negated:
        if choice([True, False]):
            subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_non_negative_agreeing_aux)
            subj_nonagree_auxiliaries = np.setdiff1d(all_non_negative_agreeing_aux, subj_agree_auxiliaries)
        else:
            subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_negative_agreeing_aux)
            subj_nonagree_auxiliaries = np.setdiff1d(all_negative_agreeing_aux, subj_agree_auxiliaries)
    else:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_non_negative_agreeing_aux)
        subj_nonagree_auxiliaries = np.setdiff1d(all_non_negative_agreeing_aux, subj_agree_auxiliaries)

    verb_agree_auxiliaries = get_matched_by(verb, "arg_2", subj_agree_auxiliaries)
    verb_nonagree_auxiliaries = get_matched_by(verb, "arg_2", subj_nonagree_auxiliaries)

    aux_agree = choice(verb_agree_auxiliaries)
    aux_nonagree = choice(verb_nonagree_auxiliaries)
    return {'aux_agree':aux_agree[0], 'aux_nonagree':aux_nonagree[0]}
