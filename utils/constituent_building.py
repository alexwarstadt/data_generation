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
from utils.vocab_sets import *
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def verb_phrase_from_subj(subject, frequent=True, allow_negated=True):
    verb = choice(get_matched_by(subject, "arg_1", all_verbs))
    args = verb_args_from_verb(verb=verb, frequent=frequent, subj=subject, allow_negated=allow_negated)
    VP = V_to_VP_mutate(verb, frequent=frequent, args=args)
    return VP

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
        freq_vocab = get_all("frequent", "1")
    else:
        freq_vocab = vocab

    # all verbs have a subject
    if subj is None:
        args["subj"] = N_to_DP_mutate(choice(get_matches_of(verb, "arg_1", get_all("category", "N", freq_vocab))), allow_quantifiers=allow_quantifiers)
    else:
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
        args["args"] = [N_to_DP_mutate(choice(get_matches_of(verb, "arg_2", get_all("category", "N", freq_vocab))), allow_quantifiers=allow_quantifiers)]

    # FROM-ING EMBEDDING
    if verb["category"] == "(S\\NP)/(S[from]\\NP)":
        obj = N_to_DP_mutate(choice(get_matches_of(verb, "arg_2", freq_vocab)), allow_quantifiers=allow_quantifiers)
        if allow_recursion:
            VP = V_to_VP_mutate(choice(get_matched_by(obj, "arg_1", all_ing_verbs)), frequent=frequent, aux=False)
        else:
            safe_verbs = np.intersect1d(all_ing_verbs, all_non_recursive_verbs)
            VP = V_to_VP_mutate(choice(get_matched_by(obj, "arg_1", safe_verbs)), frequent=frequent, aux=False)
        VP[0] = "from " + VP[0]
        args["args"] = [obj, VP]

    # RAISING TO OBJECT
    if verb["category_2"] == "V_raising_object":
        if allow_recursion:
            v_emb = choice(all_bare_verbs)
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
        if verb["arg_2"] == "expression_that":
            emb_clause[0] = "that " + emb_clause
        if verb["arg_2"] == "expression_wh":
            emb_clause[0] = "whether " + emb_clause
        args["args"] = [emb_clause]

    # QUESTION EMBEDDING
    if verb["category"] == "(S\\NP)/Q":
        args["args"] = [make_emb_subj_question(frequent)]
        # TODO: implement other kinds of questions

    # SUBJECT CONTROL
    if verb["category"] == "(S\\NP)/(S[to]\\NP)":
        if allow_recursion:
            v_emb = choice(get_matched_by(args["subj"], "arg_1", all_bare_verbs))
        else:
            safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
            v_emb = choice(get_matched_by(args["subj"], "arg_1", safe_verbs))
        VP = V_to_VP_mutate(v_emb, frequent=frequent, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [VP]

    # RAISING TO SUBJECT
    if verb["category_2"] == "V_raising_subj":
        if allow_recursion:
            v_emb = choice(all_bare_verbs)
        else:
            safe_verbs = np.intersect1d(all_bare_verbs, all_non_recursive_verbs)
            v_emb = choice(safe_verbs)
        args_emb = verb_args_from_verb(v_emb, frequent, subj=False)
        VP = V_to_VP_mutate(v_emb, frequent=frequent, args=args_emb, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [VP]

    return args


def pred_args_from_pred(pred, frequent=True, subj=None, allow_negated=True):
    """
    :param pred: the vocab entry of a non-verbal predicate
    :param frequent: should only frequent vocab be generated?
    :param subj: if supplied, the value of the subject in the returned dict. If None, a subject will be generated.
    :param allow_negated: should negated auxiliaries (e.g. has't) be generated?
    :return: dict of all arguments of verb: {subject:x1, auxiliary:x2, copula:x3, pred:x4, args:[arg_1, arg_2, ..., arg_n]}
    """
    args = {"pred": pred}
    if frequent:
        freq_vocab = get_all("frequent", "1")
    else:
        freq_vocab = vocab

    # all verbs have a subject
    if subj is None:
        args["subj"] = N_to_DP_mutate(choice(get_matches_of(pred, "arg_1", get_all("category", "N", freq_vocab))))
    else:
        args["subj"] = subj

    copula = choice(get_matched_by(subj, "arg_1", all_copulas))
    args["copula"] = copula

    # all verbs have an auxiliary (or null)
    args["aux"] = return_aux(copula, args["subj"], allow_negated=allow_negated)

    # ADJECTIVE PHRASE
    if pred["category"] == "N/N":
        args["args"] = []

    # PREPOSITIONAL PHRASE
    if pred["category"] == "PP":
        args["args"] = []

    # PREPOSITION
    if pred["category"] == "PP/NP":
        NP = N_to_DP_mutate(choice(get_matches_of(pred, "arg_2", all_nominals)))
        args["args"] = [NP]

    else:
        args["args"] = []

    return args


def join_args(args):
    """
    :param args: a list of argument for a predicate/verb
    :return: the string made from joining the arguments with spaces
    """
    return " ".join(x[0] for x in args)


def make_sentence_from_verb(verb, frequent=True):
    """
    :param verb: vocab entry for a verb
    :param frequent: should only frequent vocab items be generated?
    :return: the string for a sentence headed by the input verb.
    """
    args = verb_args_from_verb(verb, frequent)
    return " ".join([args["subj"][0],
                     args["aux"][0],
                     verb[0]] +
                    [x[0] for x in args["args"]])


def V_to_VP_mutate(verb, aux=True, frequent=True, args=None):
    """
    :param verb: vocab entry for a verb
    :param frequent: should only frequent vocab be generated?
    :param aux: if supplied, the value of the auxiliary in the returned dict. If None, an auxiliary will be generated.
    :param args: if supplied, the dictionary corresponding to the arguments of the verb
    :return: a vocab entry with the expression containing the string of the full VP
    """
    VP = verb.copy()
    if args is None:
        args = verb_args_from_verb(verb, frequent)
    if aux:
        phrases = [args["aux"][0], verb[0]] + [x[0] for x in args["args"]]
    else:
        phrases = [verb[0]] + [x[0] for x in args["args"]]
    VP[0] = " ".join(phrases)
    return VP


def make_sentence(frequent=True):
    """
    :param frequent: should only frequent vocab be generated?
    :return: a vocab entry with the expression containing the string of the full sentence
    """
    verb = choice(all_verbs)
    verb[0] = make_sentence_from_verb(verb, frequent)
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
    verb = choice(all_possibly_singular_verbs)
    args = verb_args_from_verb(verb)
    wh = choice(get_matched_by(args["subj"], "arg_1", all_wh_words))
    args["subj"] = wh
    verb[0] = make_sentence_from_args(args)
    return verb

def noun_args_from_noun(noun, frequent=True, allow_recursion=False, allow_quantifiers=True):
    """
    :param noun: the vocab entry of a noun
    :param frequent: should only frequent vocab be generated?
    :param allow_recursion: for nouns that take other nouns as arguments, should other noun-embedding nouns be generated in the embedded position?
    :param allow_quantifiers: should quantifiers (e.g. most, every) be generated as determiners for DPs?
    :return: a dict containing all the arguments of the noun: {det: x1, args: [arg_1, ..., arg_n]}
    """
    args = {}
    if frequent:
        freq_vocab = all_frequent
    else:
        freq_vocab = vocab
    if allow_quantifiers:
        args["det"] = choice(get_matched_by(noun, "arg_1", get_all("category", "(S/(S\\NP))/N", freq_vocab)))
    else:
        args["det"] = choice(get_matched_by(noun, "arg_1", get_all("quantifier", "0", get_all("category", "(S/(S\\NP))/N", freq_vocab))))
    if noun["category"] == "N":
        args["args"] = []
    if noun["category"] == "NP":
        args["det"] = []
        args["args"] = []
    if noun["category"] == "N/NP":
        if allow_recursion:
            obj = N_to_DP_mutate(choice(get_matches_of(noun, "arg_1", np.intersect1d(all_nominals, freq_vocab))))
        else:
            obj = N_to_DP_mutate(choice(get_matches_of(noun, "arg_1", np.intersect1d(all_nouns, freq_vocab))))
        args["args"] = [obj]
    if noun["category"] == "N\\NP[poss]":
        if allow_recursion:
            poss = make_possessive(N_to_DP_mutate(choice(get_matches_of(noun, "arg_1", np.intersect1d(all_nominals, freq_vocab)))))
        else:
            poss = make_possessive(N_to_DP_mutate(choice(get_matches_of(noun, "arg_1", np.intersect1d(all_nouns, freq_vocab)))))
        args["det"] = poss
        args["args"] = []
    return args


def N_to_DP_mutate(noun, frequent=True, determiner=True, allow_quantifiers=True):
    """
    :param noun: noun to turn into DP
    :param frequent: restrict to frequent determiners only?
    :return: NONE. mutates string of noun.
    """
    args = noun_args_from_noun(noun, frequent, allow_quantifiers=allow_quantifiers)
    if determiner and args["det"] is not []:
        noun[0] = " ".join([args["det"][0],
                            noun[0]] +
                           [x[0] for x in args["args"]])
    else:
        noun[0] = " ".join([noun[0]] +
                           [x[0] for x in args["args"]])
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
    """
    :param noun: the vocab entry of a noun
    :return: a reflexive pronoun agreeing with the noun
    """
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


def make_possessive(DP):
    """
    :param DP: a vocab entry for a full DP (expression of type e)
    :return: the DP with expression containing the string with 's appended
    """
    poss_str = "'" if DP["pl"] == "1" and DP[0][-1] == "s" else "'s"
    DP[0] = DP[0] + poss_str
    return DP


def get_bare_form_str(verb_str):
    """
    :param verb_str: the string of a verb
    :return: the string of the bare form of the verb
    """
    words = verb_str.split(" ")
    words[0] = lemmatizer.lemmatize(words[0], "v")
    return " ".join(words)


def get_bare_form(verb):
    """
    :param verb: the vocab entry of a verb
    :return: the vocab entry of the bare form of the verb
    """
    bare_verb = verb.copy()
    bare_verb["expression"] = get_bare_form_str(verb["expression"])
    bare_verb["finite"] = "0"
    bare_verb["bare"] = "1"
    bare_verb["pres"] = "0"
    bare_verb["past"] = "0"
    bare_verb["ing"] = "0"
    bare_verb["en"] = "0"
    bare_verb["3sg"] = "0"
    return bare_verb


def negate_VP(verb, aux):
    """
    :param verb: vocab entry for a verb
    :param aux: vocab entry for an auxiliary
    :return: the verb form and auxiliary form necessary for the corresponding negated VP
    """
    if aux["expression"] == "":
        aux_neg = get_all("expression", "didn't")[0] if verb["past"] == "1" \
            else get_all("expression", "doesn't")[0] if verb["3sg"] == "1" \
            else get_all("expression", "don't")[0]
        verb_neg = get_bare_form(verb)
    else:
        aux_neg = negate_aux(aux)
        verb_neg = verb
    return verb_neg, aux_neg


def negate_V_args(V_args):
    """
    :param V_args: a dict containing the arguments of a verb
    :return: the dict with additional entries for the verb form and auxiliary form necessary for the corresponding negated VP
    """
    verb_neg, aux_neg = negate_VP(V_args["verb"], V_args["aux"])
    V_args["aux_neg"] = aux_neg
    V_args["verb_neg"] = verb_neg
    return V_args

def negate_aux(aux):
    """
    :param aux: an auxiliary vocab entry
    :return: the form of the auxiliary necessary for the corresponding negated VP
    """
    if aux["expression"] == "might":
        aux_neg = get_all("expression", "might")[0]
        aux_neg[0] = "might not"
        return aux_neg
    if aux["expression"] == "would":
        return get_all("expression", "wouldn't")[0]
    if aux["expression"] == "could":
        return get_all("expression", "couldn't")[0]
    if aux["expression"] == "should":
        return get_all("expression", "shouldn't")[0]
    if aux["expression"] == "will":
        return get_all("expression", "won't")[0]
    if aux["expression"] == "can":
        return get_all("expression", "can't")[0]
    if aux["expression"] == "do":
        return get_all("expression", "don't")[0]
    if aux["expression"] == "does":
        return get_all("expression", "doesn't")[0]
    if aux["expression"] == "did":
        return get_all("expression", "didn't")[0]
    if aux["expression"] == "is":
        return get_all("expression", "isn't")[0]
    if aux["expression"] == "are":
        return get_all("expression", "aren't")[0]
    if aux["expression"] == "was":
        return get_all("expression", "wasn't")[0]
    if aux["expression"] == "were":
        return get_all("expression", "weren't")[0]
    if aux["expression"] == "has":
        return get_all("expression", "hasn't")[0]
    if aux["expression"] == "have":
        return get_all("expression", "haven't")[0]
    if aux["expression"] == "had":
        return get_all("expression", "hadn't")[0]


def embed_V_args_under_modal(V_args):
    """ 
    This is used to embed `John was sleeping' under might as `John might have been sleeping'. 
    If the aux doesn't need to change, return None.
    """
    aux_under_modal, verb_under_modal = get_VP_under_modal_form(V_args["aux"], V_args["verb"])
    V_args["aux_under_modal"] = aux_under_modal
    V_args["verb_under_modal"] = verb_under_modal
    return V_args


def get_VP_under_modal_form(aux, verb):
    """ 
    This is used to embed `John was sleeping' under might as `John might have been sleeping'. 
    If the aux doesn't need to change, return None.
    """
    if aux["expression"] == "might":
        return None, verb
    if aux["expression"] == "would":
        return None, verb
    if aux["expression"] == "could":
        return None, verb
    if aux["expression"] == "should":
        return None, verb
    if aux["expression"] == "will":
        return None, verb
    if aux["expression"] == "can":
        return None, verb
    if aux["expression"] == "do":
        return None, verb
    if aux["expression"] == "does":
        return None, verb
    if aux["expression"] == "did":
        return get_all("expression", "have", all_auxs)[0], get_en_form(verb)
    if aux["expression"] == "is":
        bare_aux = aux.copy()
        bare_aux["expression"] = "be"
        return bare_aux, verb
    if aux["expression"] == "are":
        bare_aux = aux.copy()
        bare_aux["expression"] = "be"
        return bare_aux, verb
    if aux["expression"] == "was":
        bare_aux = aux.copy()
        bare_aux["expression"] = "have been"
        return bare_aux, verb
    if aux["expression"] == "were":
        bare_aux = aux.copy()
        bare_aux["expression"] = "have been"
        return bare_aux, verb
    if aux["expression"] == "has":
        bare_aux = aux.copy()
        bare_aux["expression"] = "have"
        return bare_aux, verb
    if aux["expression"] == "have":
        return get_all("expression", "have", all_auxs)[0], verb
    if aux["expression"] == "had":
        return get_all("expression", "have", all_auxs)[0], verb
    if aux["expression"] == "":
        if verb["pres"] == "1":
            return aux, get_bare_form(verb)
        else:
            return get_all("expression", "have", all_auxs)[0], get_en_form(verb)


def get_en_form(verb):
    """
    :param verb: a verb vocab item
    :return: the past participle form with the same root
    """
    return get_all("root", verb["root"], all_en_verbs)[0]

def get_do_form(verb):
    """
    :param verb: a verb vocab item
    :return: the form of "do" necessary for "do"-support in question formation
    """
    do = get_all("expression", "do", all_auxs)[0]
    does = get_all("expression", "does", all_auxs)[0]
    did = get_all("expression", "did", all_auxs)[0]
    if verb["past"] == "1":
        return did
    if verb["pres"] == "1":
        if verb["3sg"] == "1":
            return does
        else:
            return do
