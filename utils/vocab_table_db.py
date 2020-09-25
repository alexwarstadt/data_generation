import numpy as np
import csv
import sqlite3
from os import path

basepath = path.dirname(__file__)
db_filepath = path.abspath(path.join(basepath, '..', 'lexicon.db'))
vocab_filepath = path.abspath(path.join(basepath, '..', 'vocabulary.csv'))
connection = sqlite3.connect(db_filepath)
cursor = connection.cursor()

headers = []

with open(vocab_filepath, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

attribute_lookup = dict([(j, i) for i, j in enumerate(headers)])


def get_all(label, value):
    """
    :param label: string. field name.
    :param value: string. label.
    :return: table restricted to all entries with "value" in field "label"
    """
    query = "SELECT * FROM vocabulary WHERE " + label + " = ?;"
    rows = cursor.execute(query, (value,))
    return np.array([row for row in rows])


def get_all_conjunctive(labels_values):
    """
    :param labels_values: list of (l,v) pairs: [(l1, v1), (l2, v2), (l3, v3)]
    :return: vocab items with the given value for each label
    """
    select_substr = ''.join(["{} = ? and ".format(pair[0]) for pair in labels_values]).rstrip("and ")
    values = [pair[1] for pair in labels_values]
    query = "SELECT * FROM vocabulary WHERE " + select_substr
    rows = cursor.execute(query, values)
    return np.array([row for row in rows])


def get_union(label_value_disjunct):
    """
    :param label_value_disjunct: tuple of ((l1, v1), (l2, v2) )pair
    :return: vocab items that satisfy both sides of disjunction
    """
    (l1, v1), (l2, v2) = label_value_disjunct
    query = "SELECT * FROM vocabulary WHERE {} = ? or {} = ?".format(l1, l2)
    rows = cursor.execute(query, [v1, v2])
    return np.array([row for row in rows])


def get_union_conjunctive(labels_values1, labels_values2):
    """
    :param labels_values1: list of (l, v) pairs: [(l1, v1), (l2, v2), (l3, v3)].
    :param labels_values2: list of (l, v) pairs: [(l1, v1), (l2, v2), (l3, v3)].
    :return: vocab items that satisfy specifications of both sides of disjunction
    """
    pass


def get_all_except(packed_values):
    """
    :param labels_values: list of (l, v) pairs for selection
    :param neg_labels_values: list of (l, v) pairs for exclusion
    """
    labels_values, neg_labels_values = packed_values
    select_substr = ''.join(["{} = ? and ".format(pair[0]) for pair in labels_values])
    exclude_substr = ''.join("{} != ? and ".format(pair[0]) for pair in neg_labels_values).rstrip("and ")
    values = [pair[1] for pair in labels_values] + [pair[1] for pair in neg_labels_values]
    query = "SELECT * FROM vocabulary WHERE " + select_substr + exclude_substr
    rows = cursor.execute(query, values)
    return np.array([row for row in rows])


def get_matches_of(row, label):
    """
    :param row: ndarray row. functor vocab item.
    :param label: string. field containing selectional restrictions.
    :return: all entries in table that match the selectional restrictions of row as given in label.
    """
    value = row[attribute_lookup[label]]

    if value is None:
        pass
    else:
        values = str(value).split(";")
        matches = []

        for disjunct in values:
            conjuncts = conj_list(disjunct)
            results = get_all_conjunctive(conjuncts)
            matches.extend(results)

        return np.array(matches)


def get_matched_by(row, label, table):
    """
    :param row: ndarray row. selected vocab item.
    :param label: string. field containing selectional restrictions.
    :param table: ndarray of vocab items.
    :return: all entries in table whose selectional restrictions in label are matched by row.
    """
    subset = get_all_conjunctive(table)

    matches = []

    for entry in subset:
        value = row[attribute_lookup[label]]

        if is_match_disj(row, value):
            matches.append(entry)

    return np.array(matches)


def conj_list(conjunction):
    """
    :param conjunction: a string corresponding to a conjunction of selectional restrictions
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
    if disjunction == "":
        return True
    else:
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