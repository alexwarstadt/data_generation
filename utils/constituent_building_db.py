# Authors: Alex Warstadt
# Script for generating NPI sentences with quantifiers as licensors

# TODO: document metadata
import random
import numpy as np
import utils.vocab_table_db as db
import utils.vocab_sets_db as vocab

from utils.conjugate_db import *
from random import choice
from utils.string_utils import remove_extra_whitespace
from nltk.stem import WordNetLemmatizer
from utils.exceptions import *

lemmatizer = WordNetLemmatizer()


def verb_args_from_verb(verb, frequent=True, subj=None, aux=None, allow_negated=True, allow_modal=True, allow_recursion=False, allow_quantifiers=True):
    """
    :param verb: a vocab entry for a verb
    :param frequent: should only frequent vocab be generated?
    :param subj: if supplied, the value of the subject in the returned dict. If None, a subject will be generated.
    :param aux: if supplied, the value of the auxiliary in the returned dict. If None, an auxiliary will be generated.
    :param allow_negated: should negated auxiliaries (e.g. has't) be generated?
    :param allow_modal: should modal auxiliaries (e.g. might) be generated?
    :param allow_recursion: for verbs that select for a clause or VP, should other clause/VP embedding verbs be generated in the embedded position?
    :param allow_quantifiers: should quantifiers (e.g. most, every) be generated as determiners for DPs?
    :return: dict of all arguments of verb: {subject:x1, auxiliary:x2, verb:x3, args:[arg_1, arg_2, ..., arg_n]}
    """
    args = {"verb": verb}
    if frequent:
        freq_vocab = db.get_all("frequent", "1")
    else:
        freq_vocab = db.get_table()

    # all verbs have a subject
    if subj is None:
        subj = N_to_DP_mutate(choice(db.get_matches_of(verb, "arg_1", db.get_all("category", "N", freq_vocab))), allow_quantifiers=allow_quantifiers)
    args["subj"] = subj

    # all verbs have an auxiliary (or null)
    if aux is None:
        args["aux"] = return_aux(verb, args["subj"], allow_negated=allow_negated, allow_modal=allow_modal)
    else:
        args["aux"] = aux

    # INTRANSITIVE
    if verb["category"] == "S\\NP":
        args["args"] = []

    # TRANSITIVE
    if verb["category"] == "(S\\NP)/NP":
        args["args"] = [N_to_DP_mutate(choice(db.get_matches_of(verb, "arg_2", db.get_all("category", "N", freq_vocab))), allow_quantifiers=allow_quantifiers)]

    # FROM-ING EMBEDDING
    if verb["category"] == "(S\\NP)/(S[from]\\NP)":
        obj = N_to_DP_mutate(choice(db.get_matches_of(verb, "arg_2", freq_vocab)), allow_quantifiers=allow_quantifiers)
        if allow_recursion:
            VP = V_to_VP_mutate(choice(db.get_matched_by(obj, "arg_1", all_ing_verbs)), frequent=frequent, aux=False)
        else:
            safe_verbs = np.intersect1d(all_ing_verbs, all_non_recursive_verbs)
            VP = V_to_VP_mutate(choice(get_matched_by(obj, "arg_1", safe_verbs)), frequent=frequent, aux=False)
        VP[0] = "from " + VP[0]
        args["args"] = [obj, VP]

    # RAISING TO OBJECT
    if verb["category_2"] == "V_raising_object":
        if allow_recursion:
            v_emb = choice(db.get_all_conjunctive(vocab.all_bare_verbs))
        else:
            safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
            v_emb = choice(safe_verbs)
        args_emb = verb_args_from_verb(v_emb, frequent)
        VP = V_to_VP_mutate(v_emb, frequent=frequent, args=args_emb, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [args_emb["subj"], VP]

    # OBJECT CONTROL
    if verb["category_2"] == "V_control_object":
        obj = N_to_DP_mutate(choice(get_matches_of(verb, "arg_2")), allow_quantifiers=allow_quantifiers)
        if allow_recursion:
            v_emb = choice(get_matched_by(obj, "arg_1", all_bare_verbs))
        else:
            safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
            v_emb = choice(get_matched_by(obj, "arg_1", safe_verbs))
        VP = V_to_VP_mutate(v_emb, frequent=frequent, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [obj, VP]

    # CLAUSE EMBEDDING
    if verb["category"] == "(S\\NP)/S":
        emb_clause = make_sentence(frequent)
        if "that" in verb["arg_2"]:
            emb_clause[0] = "that " + emb_clause[0]
        if "wh" in verb["arg_2"]:
            emb_clause[0] = "whether " + emb_clause[0]
        args["args"] = [emb_clause]

    # QUESTION EMBEDDING
    if verb["category"] == "(S\\NP)/Q":
        args["args"] = [make_emb_subj_question(frequent)]
        # TODO: implement other kinds of questions

    # SUBJECT CONTROL
    if verb["category"] == "(S\\NP)/(S[to]\\NP)":
        if allow_recursion:
            v_emb = choice(get_matched_by(subj, "arg_1", all_bare_verbs))
        else:
            safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
            v_emb = choice(get_matched_by(subj, "arg_1", safe_verbs))
        VP = V_to_VP_mutate(v_emb, frequent=frequent, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [VP]

    # RAISING TO SUBJECT
    if verb["category_2"] == "V_raising_subj":
        if allow_recursion:
            v_emb = choice(all_bare_verbs)
        else:
            safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
            v_emb = choice(get_matched_by(subj, "arg_1", safe_verbs))
        args_emb = verb_args_from_verb(v_emb, frequent, subj=False)
        VP = V_to_VP_mutate(v_emb, frequent=frequent, args=args_emb, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [VP]

    return args


def join_args(args):
    """
    :param args: a list of argument for a predicate/verb
    :return: the string made from joining the arguments with spaces
    """
    return " ".join(x[0] for x in args)


def make_sentence_from_verb(verb, frequent=True, allow_recursion=False):
    """
    :param verb: vocab entry for a verb
    :param frequent: should only frequent vocab items be generated?
    :return: the string for a sentence headed by the input verb.
    """
    args = verb_args_from_verb(verb, frequent=frequent, allow_recursion=False)
    return " ".join([args["subj"][0],
                     args["aux"][0],
                     verb[0]] +
                    [x[0] for x in args["args"]])


def V_to_VP_mutate(verb, aux=True, frequent=True, args=None, allow_recursion=False):
    """
    :param verb: vocab entry for a verb
    :param frequent: should only frequent vocab be generated?
    :param aux: if supplied, the value of the auxiliary in the returned dict. If None, an auxiliary will be generated.
    :param args: if supplied, the dictionary corresponding to the arguments of the verb
    :return: a vocab entry with the expression containing the string of the full VP
    """
    VP = verb.copy()
    if args is None:
        args = verb_args_from_verb(verb, frequent=frequent, allow_recursion=allow_recursion)
    if aux:
        phrases = [args["aux"][0], verb[0]] + [x[0] for x in args["args"]]
    else:
        phrases = [verb[0]] + [x[0] for x in args["args"]]
    VP[0] = " ".join(phrases)
    return VP


def make_sentence(frequent=True, allow_recursion=False):
    """
    :param frequent: should only frequent vocab be generated?
    :return: a vocab entry with the expression containing the string of the full sentence
    """
    all_verbs = db.get_all_conjunctive(vocab.all_verbs)
    verb = choice(all_verbs)
    verb[0] = make_sentence_from_verb(verb, frequent=frequent, allow_recursion=allow_recursion)
    return verb


def make_sentence_from_args(args):
    """
    :param args: the argument dictionary for a verb
    :return: the string corresponding to the sentence containing the verb and all its arguments
    """
    return " ".join([args["subj"][0],
                     args["aux"][0],
                     args["verb"][0]] +
                    [x[0] for x in args["args"]])


def make_emb_subj_question(frequent=True):
    """
    :param frequent: should only frequent vocab be generated?
    :return: a vocab entry with the expression corresponding to the string of an entire embedded question with a wh-subject
    """
    verb = choice(db.get_all_conjunctive(vocab.all_possibly_singular_verbs))
    args = verb_args_from_verb(verb)
    wh = choice(db.get_matched_by(args["subj"], "arg_1", vocab.all_wh_words))
    args["subj"] = wh
    verb[0] = make_sentence_from_args(args)
    return verb


def noun_args_from_noun(noun, frequent=True, allow_recursion=False, allow_quantifiers=True, avoid=None):
    """
    :param noun: the vocab entry of a noun
    :param frequent: should only frequent vocab be generated?
    :param allow_recursion: for nouns that take other nouns as arguments, should other noun-embedding nouns be generated in the embedded position?
    :param allow_quantifiers: should quantifiers (e.g. most, every) be generated as determiners for DPs?
    :return: a dict containing all the arguments of the noun: {det: x1, args: [arg_1, ..., arg_n]}
    """
    args = {}
    if frequent:
        sample_space = db.get_all_conjunctive(vocab.all_frequent)
    else:
        sample_space = vocab
    if avoid is not None:
        sample_space = np.setdiff1d(sample_space, avoid)
    if allow_quantifiers:
        all_determiners = db.get_all_conjunctive(vocab.all_determiners)
        sample_space_determiners = np.intersect1d(all_determiners, sample_space)
        args["det"] = choice(db.get_matched_by(noun, "arg_1", sample_space_determiners, subtable=True))
    else:
        all_determiners = db.get_all_conjunctive(vocab.all_determiners)
        sample_space_determiners = np.intersect1d(all_determiners, sample_space)
        quantifiers = db.get_all_from([("quantifier", "0")], sample_space_determiners)
        args["det"] = choice(db.get_matched_by(noun, "arg_1", quantifiers, subtable=True))
    if noun["category"] == "N":
        args["args"] = []
    if noun["category"] == "NP":
        args["det"] = []
        args["args"] = []
    if noun["category"] == "N/NP":
        if allow_recursion:
            all_nominals = db.get_all_conjunctive(vocab.all_nominals)
            obj = N_to_DP_mutate(choice(db.get_matches_of(noun, "arg_1", np.intersect1d(all_nominals, sample_space))))
        else:
            all_nouns = db.get_all_conjunctive(vocab.all_nouns)
            obj = N_to_DP_mutate(choice(db.get_matches_of(noun, "arg_1", np.intersect1d(all_nouns, sample_space))))
        args["args"] = [obj]
    if noun["category"] == "N\\NP[poss]":
        if allow_recursion:
            all_nominals = db.get_all_conjunctive(vocab.all_nominals)
            poss = make_possessive(N_to_DP_mutate(choice(db.get_matches_of(noun, "arg_1", np.intersect1d(all_nominals, sample_space)))))
        else:
            all_nouns = db.get_all_conjunctive(vocab.all_nouns)
            poss = make_possessive(N_to_DP_mutate(choice(db.get_matches_of(noun, "arg_1", np.intersect1d(all_nouns, sample_space)))))
        args["det"] = poss
        args["args"] = []
    if noun["category"] == "N/S":
        S = make_sentence(frequent=frequent, allow_recursion=allow_recursion)
        S[0] = "that " + S[0]
        args["args"] = [S]
    return args


def N_to_DP_mutate(noun, frequent=True, determiner=True, allow_quantifiers=True, avoid=None):
    """
    :param noun: noun to turn into DP
    :param frequent: restrict to frequent determiners only?
    :return: NONE. mutates string of noun.
    """
    args = noun_args_from_noun(noun, frequent, allow_quantifiers=allow_quantifiers, avoid=avoid)
    if determiner and args["det"] is not []:
        noun[0] = " ".join([args["det"][0],
                            noun[0]] +
                           [x[0] for x in args["args"]])
    else:
        noun[0] = " ".join([noun[0]] +
                           [x[0] for x in args["args"]])
    return noun


def make_possessive(DP):
    """
    :param DP: a vocab entry for a full DP (expression of type e)
    :return: the DP with expression containing the string with 's appended
    """
    poss_str = "'" if DP["pl"] == "1" and DP[0][-1] == "s" else "'s"
    DP[0] = DP[0] + poss_str
    return DP

