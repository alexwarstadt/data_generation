import utils.vocab_sets_db as vocab
import utils.vocab_table_db as db

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
        all_modals_auxs = db.get_all_conjunctive(vocab.all_modals_auxs)
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_modals_auxs)
    else:
        all_non_negated_modals_auxs = db.get_all_conjunctive(vocab.all_non_negated_modals_auxs)
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_non_negated_modals_auxs)
    if require_negated:
        all_negated_modals_auxs = db.get_all_conjunctive(vocab.all_negated_modals_auxs)
        subj_agree_auxiliaries = db.get_matched_by(subj, "arg_1", all_negated_modals_auxs)
    if change_v_form:
        root_verb = db.get_all("root", verb["root"])
        verb = choice(db.get_matched_by(subj, "arg_1", root_verb))

    verb_agree_auxiliaries = db.get_matched_by(verb, "arg_2", subj_agree_auxiliaries)
    aux = choice(verb_agree_auxiliaries)
    verb = verb.copy()
    verb[0] = aux[0] + " " + verb[0]
    return verb

