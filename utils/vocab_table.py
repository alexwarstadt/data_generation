import numpy as np


data_type = [("expression", "U20"),
             ("category", "U20"),
             ("category_2", "U20"),
             ("animate", "U1"),
             ("occupation", "U1"),
             ("clothing", "U1"),
             ("appearance", "U1"),
             ("thing", "U1"),
             ("sg", "U1"),
             ("pl", "U1"),
             ("mass", "U1"),
             ("finite", "U1"),
             ("bare", "U1"),
             ("pres", "U1"),
             ("ing", "U1"),
             ("en", "U1"),
             ("3sg", "U1"),
             ("subj", "U20"),
             ("obj", "U20"),
             ("inflection", "U20"),
             ("root", "U20"),
             ("adjs", "U100"),
             ("restrictor_N", "U100"),
             ("restrictor_DE", "U100"),
             ("scope_DE", "U100")
            ]


vocab = np.genfromtxt("../vocabulary.csv", delimiter=",", names=True, dtype=data_type)

# def get_all(label, value):
#     return np.array(list(filter(lambda x: x[label]==value, vocab)), dtype=data_type)

def get_all(label, value, table=vocab):
    return np.array(list(filter(lambda x: x[label]==value, table)), dtype=data_type)

def get_all_conjunctive(labels_values, table=vocab):
    """
    :param labels_values: list of (l,v) pairs: [(l1, v1), (l2, v2), (l3, v3)]
    :return: vocab items with the given value for each label
    """
    to_return = table
    for label, value in labels_values:
        to_return = np.array(list(filter(lambda x: x[label] == value, to_return)), dtype=data_type)
    return to_return


def get_matches_of(row, label, table=vocab):
    """
    
    :param row: 
    :param label: 
    :param table: 
    :return: 
    """
    value = str(np.array(row, dtype=data_type)[label])
    if value == "":
        pass
    else:
        matches = []
        values = str(value).split(";")
        for disjunct in values:
            k_vs = conj_list(disjunct)
            matches.extend(list(get_all_conjunctive(k_vs, table)))
        return np.array(matches, dtype=data_type)


def get_matched_by(row, label, table=vocab):
    """
    :param row: 
    :param label: 
    :param table: 
    :return: 
    """
    matches = []
    for entry in table:
        value = str(np.array(entry, dtype=data_type)[label])
        if is_match_disj(row, value):
            matches.append(entry)
    return np.array(matches)


def conj_list(conjunction):
    """
    :param disjunct: a string corresponding to a conjunction of selectional restrictions
    :return: a list of k, v pairs 
    """
    try:
        to_return = [(v.split("=")[0], v.split("=")[1]) for v in conjunction.split("^")]
        return to_return
    except IndexError:
        pass

def is_match_disj(row, disjunction):
    """
    :param row: a vocab item
    :param disjunction: a string corresponding to a disjunction of selectional restrictions
    :return: true if the row matches one of the disjuncts, false otherwise
    """
    disjuncts = disjunction.split(";")
    match = False
    for d in disjuncts:
        match = match or is_match_conj(row, d)
    return match

def is_match_conj(row, conjunction):
    """
    :param row: a vocab item
    :param conjunction: a string corresponding to a conjunction of selectional restrictions
    :return: true if the row matches the conjunction, false otherwise
    """
    conjuncts = conj_list(conjunction)
    match = True
    for k, v in conjuncts:
        try:
            match = match and row[k] == v
        except TypeError:
            pass
    return match


def get_one(row, label):
    return str(np.array(row, dtype=data_type)[label])

pass
