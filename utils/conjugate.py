from utils.vocab_table import *
from random import choice
from utils.vocab_sets import *

def conjugate(verb, subj, allow_negated=True, require_negated=False):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: should negated auxiliaries (e.g. shouldn't) ever be generated?
    :param require_negated: should negated auxiliaries always be generated?
    :return: copy of verb with modified string to include auxiliary
    """
    if allow_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_modals_auxs)
    else:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_non_negated_modals_auxs)

    if require_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_negated_modals_auxs)

    verb_agree_auxiliaries = get_matched_by(verb, "arg_2", subj_agree_auxiliaries)
    aux = choice(verb_agree_auxiliaries)
    verb = verb.copy()
    verb[0] = aux[0] + " " + verb[0]
    return verb


def return_aux(verb, subj, allow_negated=True, require_negated=False, allow_modal=True):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: should negated auxiliaries (e.g. shouldn't) ever be generated?
    :param require_negated: should negated auxiliaries always be generated?
    :return: auxiliary that agrees with verb, or none if no auxiliary is needed.
    """
    if allow_negated and allow_modal:
        safe_auxs = all_modals_auxs
    if allow_negated and not allow_modal:
        safe_auxs = all_auxs
    if not allow_negated and allow_modal:
        safe_auxs = all_non_negated_modals_auxs
    if not allow_negated and not allow_modal:
        safe_auxs = all_non_negated_auxs
    if require_negated and allow_modal:
        safe_auxs = all_negated_modals_auxs
    if require_negated and not allow_modal:
        safe_auxs = all_negated_auxs
    aux = choice(get_matched_by(verb, "arg_2", get_matched_by(subj, "arg_1", safe_auxs)))
    return aux

def return_copula(subj, allow_negated=True, require_negated=False):
    """
    :param subj: vocab entry
    :param allow_negated: should negated auxiliaries (e.g. shouldn't) ever be generated?
    :param require_negated: should negated auxiliaries always be generated?
    :return: copula that agrees with the subject
    """
    if allow_negated:
        subj_agree_auxiliaries = get_matched_by(subj, "arg_1", all_finite_copulas)
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
    if verb["finite"] == "1":
        aux_agree = choice(get_all("expression", "", all_modals_auxs))
        aux_nonagree = choice(get_all("expression", "", all_modals_auxs))
    else:
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

def get_mismatch_verb(verb):
    """
    :param verb: a present tense verb vocab entry
    :return: the verb with opposite agreement
    """
    if verb["pres"] == "1":
        verb_root = get_all("root", verb["root"])
        if verb["3sg"] == "1":
            return choice(get_all("pres", "1", get_all("3sg", "0", verb_root)))
        else:
            return choice(get_all("pres", "1", get_all("3sg", "1", verb_root)))
    else:
        raise ValueError("Verb should be present tense.")

def get_same_aux_verbs(verb):
    """
    :param verb: a verb vocab entry
    :return: the set of all verbs with the same auxiliary agreement properties
    """
    if verb["finite"] == "1":
        return all_finite_verbs
    elif verb["bare"] == "1":
        return all_bare_verbs
    elif verb["en"] == "1":
        return all_en_verbs
    elif verb["ing"] == "1":
        return all_ing_verbs
