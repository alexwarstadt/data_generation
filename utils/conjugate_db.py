import numpy as np
import utils.vocab_sets_db as vocab
import utils.vocab_table_db as db
from utils.vocab_table_db import attribute_lookup
from random import choice


def conjugate(verb, subj, allow_negated=True, require_negated=False, change_v_form=False):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: should negated auxiliaries (e.g. shouldn't) ever be generated?
    :param require_negated: should negated auxiliaries always be generated?
    :return: copy of verb with modified string to include auxiliary
    """
    if allow_negated:
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", vocab.all_modals_auxs)
    else:
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", vocab.all_non_negated_modals_auxs)
    if require_negated:
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", vocab.all_negated_modals_auxs)
    if change_v_form:
        root_verb = ("root", verb["root"])
        verb = choice(db.get_matched_by(subj, "arg_1", root_verb))

    verb_agree_auxiliaries = db.get_matched_by(verb, "arg_2", subj_agree_auxiliaries, subtable=True)
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
        safe_auxs = db.get_all_conjunctive(vocab.all_modals_auxs)
    if allow_negated and not allow_modal:
        safe_auxs = db.get_all_conjunctive(vocab.all_auxs)
    if not allow_negated and allow_modal:
        safe_auxs = db.get_all_conjunctive(vocab.all_non_negated_modals_auxs)
    if not allow_negated and not allow_modal:
        safe_auxs = db.get_all_conjunctive(vocab.all_non_negated_auxs)
    if require_negated and allow_modal:
        safe_auxs = db.get_all_conjunctive(vocab.all_negated_modals_auxs)
    if require_negated and not allow_modal:
        safe_auxs = db.get_all_conjunctive(vocab.all_negated_auxs)

    subj_auxs = db.get_matched_by(subj, "arg_1", safe_auxs, subtable=True)
    aux = choice(db.get_matched_by(verb, "arg_2", subj_auxs, subtable=True))

    return aux


def return_copula(subj, allow_negated=True, require_negated=False):
    """
    :param subj: vocab entry
    :param allow_negated: should negated auxiliaries (e.g. shouldn't) ever be generated?
    :param require_negated: should negated auxiliaries always be generated?
    :return: copula that agrees with the subject
    """
    if allow_negated:
        all_finite_copulas = db.get_all_except(vocab.all_finite_copulas)
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_finite_copulas, subtable=True)
    else:
        all_non_negative_copulas = db.get_all_except(vocab.all_non_negative_copulas)
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_non_negative_copulas, subtable=True)
    if require_negated:
        all_negative_copulas = db.get_all_except(vocab.all_negative_copulas)
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_negative_copulas, subtable=True)
    aux = choice(subj_agree_auxiliaries)
    return aux


def require_aux_agree(verb, subj, allow_negated=True):
    """
    :param verb: vocab entry
    :param subj: vocab entry
    :param allow_negated: are negated auxiliaries (e.g. shouldn't) allowed
    :return: auxiliary that agrees with verb
    """
    if verb[attribute_lookup["finite"]] == "1":
        aux_agree = choice(db.get_all_conjunctive([("expression", "")] + vocab.all_modals_auxs))
        aux_nonagree = choice(db.get_all_conjunctive([("expression", "")] + vocab.all_modals_auxs))
    else:
        if allow_negated:
            if choice([True, False]):
                all_non_negative_agreeing_aux = db.get_all_except(vocab.all_non_negative_agreeing_aux)
                subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_non_negative_agreeing_aux, subtable=True)
                # TODO Change return values from DB to be tuples instead of lists so we don't need this line.
                subj_agree_auxiliaries = [tuple(vocab_item) for vocab_item in subj_agree_auxiliaries]
                all_non_negative_agreeing_aux = [tuple(vocab_item) for vocab_item in all_non_negative_agreeing_aux]
                subj_nonagree_auxiliaries = set(all_non_negative_agreeing_aux) - set(subj_agree_auxiliaries)
            else:
                all_negative_agreeing_aux = db.get_all_except(vocab.all_negative_agreeing_aux)
                subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_negative_agreeing_aux, subtable=True)
                subj_agree_auxiliaries = [tuple(vocab_item) for vocab_item in subj_agree_auxiliaries]
                all_negative_agreeing_aux = [tuple(vocab_item) for vocab_item in all_negative_agreeing_aux]
                subj_nonagree_auxiliaries = set(all_negative_agreeing_aux) - set(subj_agree_auxiliaries)
        else:
            all_non_negative_agreeing_aux = db.get_all_conjunctive(vocab.all_non_negative_agreeing_aux)
            subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_non_negative_agreeing_aux, subtable=True)
            subj_nonagree_auxiliaries = np.setdiff1d(all_non_negative_agreeing_aux, subj_agree_auxiliaries)

        verb_agree_auxiliaries = db.get_matched_by(verb, "arg_2", subj_agree_auxiliaries, subtable=True)
        verb_nonagree_auxiliaries = db.get_matched_by(verb, "arg_2", subj_nonagree_auxiliaries, subtable=True)

        aux_agree = choice(verb_agree_auxiliaries)
        aux_nonagree = choice(verb_nonagree_auxiliaries)
    return {'aux_agree':aux_agree[0], 'aux_nonagree':aux_nonagree[0]}


def get_mismatch_verb(verb):
    """
    :param verb: a present tense verb vocab entry
    :return: the verb with opposite agreement
    """
    if verb[attribute_lookup["pres"]] == "1":    # TODO fix this so that you can look up things by: verb["pres"] == 1
        if verb[attribute_lookup["sg3"]] == "1":
            return db.get_all_conjunctive([("pres", "1"), ("sg3", "0"), ("root", verb[attribute_lookup["root"]])])[0]
        else:
            return db.get_all_conjunctive([("pres", "1"), ("sg3", "1"), ("root", verb[attribute_lookup["root"]])])[0]
    else:
        raise ValueError("Verb should be present tense.")


def get_same_aux_verbs(verb):
    """
    :param verb: a verb vocab entry
    :return: the set of all verbs with the same auxiliary agreement properties
    """
    if verb["finite"] == "1":
        return db.get_all_conjunctive(vocab.all_finite_verbs)
    elif verb["bare"] == "1":
        return db.get_all_conjunctive(vocab.all_bare_verbs)
    elif verb["en"] == "1":
        return db.get_all_conjunctive(vocab.all_en_verbs)
    elif verb["ing"] == "1":
        return db.get_all_conjunctive(vocab.all_ing_verbs)