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
from utils.pattern.text import en



def verb_phrase_from_subj(subject, frequent=True, allow_negated=True):
    verb = choice(get_matched_by(subject, "arg_1", all_verbs))
    args = verb_args_from_verb(verb=verb, frequent=frequent, subj=subject, allow_negated=allow_negated)
    VP = V_to_VP_mutate(verb, frequent=frequent, args=args)
    return VP

def verb_args_from_verb(verb, frequent=True, subj=None, allow_negated=True):
    """
    :param verb: 
    :param frequent: 
    :return: dict of all arguments of verb: {subject:x1, auxiliary:x2, ...]
    """
    args = {"verb": verb}
    if frequent:
        freq_vocab = get_all("frequent", "1")
    else:
        freq_vocab = vocab

    # all verbs have a subject
    if subj is None:
        try:
            args["subj"] = N_to_DP_mutate(choice(get_matches_of(verb, "arg_1", get_all("category", "N", freq_vocab))))
        except TypeError:
            pass
    else:
        args["subj"] = subj

    # all verbs have an auxiliary (or null)
    args["aux"] = return_aux(verb, args["subj"], allow_negated=allow_negated)

    # INTRANSITIVE
    if verb["category"] == "S\\NP":
        args["args"] = []

    # TRANSITIVE
    if verb["category"] == "(S\\NP)/NP":
        args["args"] = [N_to_DP_mutate(choice(get_matches_of(verb, "arg_2", get_all("category", "N", freq_vocab))))]

    # FROM-ING EMBEDDING
    if verb["category"] == "(S\\NP)/(S[from]\\NP)":
        obj = N_to_DP_mutate(choice(get_matches_of(verb, "arg_2", freq_vocab)))
        VP = V_to_VP_mutate(choice(get_matched_by(obj, "arg_1", all_ing_verbs)), frequent=frequent, aux=False)
        VP[0] = "from " + VP[0]
        args["args"] = [obj, VP]

    # RAISING TO OBJECT
    if verb["category_2"] == "V_raising_object":
        v_emb = choice(all_bare_verbs)
        args_emb = verb_args_from_verb(v_emb, frequent)
        VP = V_to_VP_mutate(v_emb, frequent=frequent, args=args_emb, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [args_emb["subj"], VP]

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
        v_emb = choice(get_matched_by(args["subj"], "arg_1", all_bare_verbs))
        VP = V_to_VP_mutate(v_emb, frequent=frequent, aux=False)
        VP[0] = "to " + VP[0]
        args["args"] = [VP]

    # TODO:DITRANSITIVE

    return args


def pred_args_from_pred(pred, frequent=True, subj=None, allow_negated=True):
    """
        :param verb: 
        :param frequent: 
        :return: dict of all arguments of verb: {subject:x1, auxiliary:x2, ...]
        """
    args = {"pred": pred}
    if frequent:
        freq_vocab = get_all("frequent", "1")
    else:
        freq_vocab = vocab

    # all verbs have a subject
    if subj is None:
        try:
            args["subj"] = N_to_DP_mutate(choice(get_matches_of(pred, "arg_1", get_all("category", "N", freq_vocab))))
        except TypeError:
            pass
    else:
        args["subj"] = subj

    copula = choice(get_matched_by(subj, "arg_1", all_copulas))
    args["copula"] = copula

    # all verbs have an auxiliary (or null)
    args["aux"] = return_aux(copula, args["subj"], allow_negated=allow_negated)

    if pred["category"] == "N/N":
        args["args"] = []

    if pred["category"] == "PP":
        args["args"] = []

    if pred["category"] == "PP/NP":
        NP = N_to_DP_mutate(choice(get_matches_of(pred, "arg_2", all_nominals)))
        args["args"] = [NP]

    else:
        args["args"] = []

    return args

def pred_to_predp_mutate(pred, frequent=True, copula=True, aux=True, args=None):
    if args is None:
        args = pred_args_from_pred(pred, frequent)
    try:
        phrases = []
        if aux:
            phrases = phrases + [args["aux"][0]]
        if copula:
            phrases = phrases + [args["copula"][0]]
        phrases = phrases + [pred[0]] + [x[0] for x in args["args"]]
    except IndexError:
        pass
    except KeyError:
        pass
    pred[0] = " ".join(phrases)
    return pred


def make_sentence_from_verb(verb, frequent=True):
    args = verb_args_from_verb(verb, frequent)
    return " ".join([args["subj"][0],
                     args["aux"][0],
                     verb[0]] +
                    [x[0] for x in args["args"]])


def V_to_VP_mutate(verb, aux=True, frequent=True, args=None):
    if args is None:
        args = verb_args_from_verb(verb, frequent)
    try:
        if aux:
            phrases = [args["aux"][0], verb[0]] + [x[0] for x in args["args"]]
        else:
            phrases = [verb[0]] + [x[0] for x in args["args"]]
    except IndexError:
        pass
    except KeyError:
        pass
    verb[0] = " ".join(phrases)
    return verb

def make_sentence(frequent=True):
    verb = choice(all_verbs)
    verb[0] = make_sentence_from_verb(verb, frequent)
    return verb

def make_sentence_from_args(args):
    return " ".join([args["subj"][0],
                     args["aux"][0],
                     args["verb"][0]] +
                    [x[0] for x in args["args"]])


def make_emb_subj_question(frequent=True):
    verb = choice(all_verbs)
    args = verb_args_from_verb(verb)
    wh = choice(get_matched_by(args["subj"], "arg_1", all_wh_words))
    args["subj"] = wh
    verb[0] = make_sentence_from_args(args)
    return verb

def noun_args_from_noun(noun, frequent=True):
    """
    
    :param noun: 
    :param frequent: 
    :return: 
    """
    args = {}
    if frequent:
        freq_vocab = get_all("frequent", "1")
    else:
        freq_vocab = vocab
    try:
        args["det"] = choice(get_matched_by(noun, "arg_1", get_all("category", "(S/(S\\NP))/N", freq_vocab)))
    except IndexError:
        pass
    if noun["category"] == "N":
        args["args"] = []
    if noun["category"] == "NP":
        args["det"] = []
        args["args"] = []
    if noun["category"] == "N/NP":
        try:
            obj = N_to_DP_mutate(choice(get_matches_of(noun, "arg_1", np.intersect1d(all_nominals, freq_vocab))))
        except IndexError:
            pass
        args["args"] = [obj]
    if noun["category"] == "N\\NP[poss]":
        poss = make_possessive(N_to_DP_mutate(choice(get_matches_of(noun, "arg_1", np.intersect1d(all_nominals, freq_vocab)))))
        args["det"] = poss
        args["args"] = []
    else:
        pass
    return args


def N_to_DP(noun, frequent=True):
    """
    :param noun: noun to turn into DP
    :param frequent: restrict to frequent determiners only?
    :return: matching determiner, without noun
    """
    if frequent:
        D = choice(get_matched_by(noun, "arg_1", get_all_conjunctive([("category", "(S/(S\\NP))/N"), ("frequent", '1')])))
    else:
        D = choice(get_matched_by(noun, "arg_1", get_all_conjunctive([("category", "(S/(S\\NP))/N"), ("frequent", '0')])))
    return D


def N_to_DP_mutate(noun, frequent=True, determiner=True):
    """
    :param noun: noun to turn into DP
    :param frequent: restrict to frequent determiners only?
    :return: NONE. mutates string of noun.
    """
    args = noun_args_from_noun(noun, frequent)
    try:
        if determiner and args["det"] is not []:
            noun[0] = " ".join([args["det"][0],
                                noun[0]] +
                               [x[0] for x in args["args"]])
        else:
            noun[0] = " ".join([noun[0]] +
                               [x[0] for x in args["args"]])
    except KeyError:
        pass
    except IndexError:
        pass
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


def make_possessive(DP):
    poss_str = "'" if DP["pl"] == "1" and DP[0][-1] == "s" else "'s"
    DP[0] = DP[0] + poss_str
    return DP

def get_bare_form(V):
    bare_str = en.lemma(V[0])

def get_bare_form(verb):
    words = verb["expression"].split(" ")
    words[0] = en.lemma(words[0])
    bare_verb = verb.copy()
    bare_verb["expression"] = " ".join(words)
    bare_verb["finite"] = "0"
    bare_verb["bare"] = "1"
    bare_verb["pres"] = "0"
    bare_verb["past"] = "0"
    bare_verb["ing"] = "0"
    bare_verb["en"] = "0"
    bare_verb["3sg"] = "0"
    return bare_verb



def negate_V_args(V_args):
    # TODO: this is a hack
    if V_args["aux"]["expression"] == "":
        V_args["aux_neg"] = get_all("expression", "didn't")[0] if V_args["verb"]["past"] == "1" \
            else get_all("expression", "doesn't")[0] if V_args["verb"]["3sg"] == "1" \
            else get_all("expression", "don't")[0]
        V_args["verb_neg"] = get_bare_form(V_args["verb"])
    else:
        V_args["aux_neg"] = negate_aux(V_args["aux"])
        V_args["verb_neg"] = V_args["verb"]
    return V_args

def negate_aux(aux):
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