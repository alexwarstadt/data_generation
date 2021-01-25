import numpy as np
import csv
import sqlite3
from os import path
from utils.data_type import data_type, index_to_column, column_to_index

basepath = path.dirname(__file__)
db_filepath = path.abspath(path.join(basepath, '..', 'lexicon.db'))
vocab_filepath = path.abspath(path.join(basepath, '..', 'vocabulary.csv'))
connection = sqlite3.connect(db_filepath)
cursor = connection.cursor()


def get_table():
    query = "SELECT * FROM vocabulary"
    rows = cursor.execute(query)
    return np.array([row for row in rows], dtype=data_type)


def get_all(label, value):
    """
    :param label: string. field name.
    :param value: string. label.
    :return: table restricted to all entries with "value" in field "label"
    """
    query = "SELECT * FROM vocabulary WHERE " + label + " = ?;"
    rows = cursor.execute(query, (value,))
    return np.array([row for row in rows], dtype=data_type)


def get_all_conjunctive(labels_values):
    """
    :param labels_values: list of (l,v) pairs: [(l1, v1), (l2, v2), (l3, v3)]
    :return: vocab items with the given value for each label
    """
    select_substr = ''.join(["{} = ? and ".format(pair[0]) for pair in labels_values]).rstrip("and ")
    values = [pair[1] for pair in labels_values]
    query = "SELECT * FROM vocabulary WHERE " + select_substr
    rows = cursor.execute(query, values)
    return np.array([row for row in rows], dtype=data_type)


def get_union(label_value_disjunct):
    """
    :param label_value_disjunct: tuple of ((l1, v1), (l2, v2) )pair
    :return: vocab items that satisfy both sides of disjunction
    """
    (l1, v1), (l2, v2) = label_value_disjunct
    query = "SELECT * FROM vocabulary WHERE {} = ? or {} = ?".format(l1, l2)
    rows = cursor.execute(query, [v1, v2])
    return np.array([row for row in rows], dtype=data_type)


def get_union_conjunctive(labels_values1, labels_values2):
    """
    :param labels_values1: list of (l, v) pairs: [(l1, v1), (l2, v2), (l3, v3)].
    :param labels_values2: list of (l, v) pairs: [(l1, v1), (l2, v2), (l3, v3)].
    :return: vocab items that satisfy specifications of both sides of disjunction
    """
    pass


def get_all_from(labels_values, table):
    """
    :param labels_values: list (l, v) of pairs: [(l1, v1), (l2, v2), (l3, v3)].
    :param table: vocabulary table to select items from.
    :return: vocab items from a subset table that satisfy the requirements from the set of labels
    """
    to_return = table
    for label, value in labels_values:
        to_return = np.array(list(filter(lambda x: x[label] == value, to_return)), dtype=table.dtype)
    return to_return


def get_all_except(packed_values):
    """
    :param packed_values: tuple (p_v, n_v) containing positive selection values p_v and negative selection values
        n_v
    :return: vocab items that fulfill the feature requirements of the first tuple element, but not the second.
    """
    labels_values, neg_labels_values = packed_values
    select_substr = ''.join(["{} = ? and ".format(pair[0]) for pair in labels_values])
    exclude_substr = ''.join("{} != ? and ".format(pair[0]) for pair in neg_labels_values).rstrip("and ")
    values = [pair[1] for pair in labels_values] + [pair[1] for pair in neg_labels_values]
    query = "SELECT * FROM vocabulary WHERE " + select_substr + exclude_substr
    rows = cursor.execute(query, values)
    return np.array([row for row in rows], dtype=data_type)


def get_all_unlike(packed_values):
    """
    :param packed_values: tuple (p_v, n_v) containing positive selection values p_v and negative selection values
        n_v
        [("arg_1", "sg=0"), ("arg_1", "pl=1")]
    :return: vocab items that fulfill the feature requirements of the first tuple element, but do not contain
        any string elements found in the second pair.
    """
    labels_values, neg_labels_values = packed_values
    select_substr = ''.join(["{} = ? and ".format(pair[0]) for pair in labels_values])
    exclude_substr = ''.join("{} not like ? and ".format(pair[0]) for pair in neg_labels_values).rstrip("and ")
    values = [pair[1] for pair in labels_values] + ["%" + pair[1] + "%" for pair in neg_labels_values]
    query = "SELECT * FROM vocabulary WHERE " + select_substr + exclude_substr
    rows = cursor.execute(query, values)
    return np.array([row for row in rows], dtype=data_type)


def get_matches_of(row, label, restrictors=None, sample_space=None):
    """
    :param row: ndarray row. functor vocab item.
    :param label: string. field containing selectional restrictions.
    :param restrictors: vocab_set_db object. a list of tuples providing labels and values
    :param sample_space: a list of ndarray rows to restrict the matches to
    :return: all entries in table that match the selectional restrictions of row as given in label.
    """
    value = str(row[column_to_index[label]])
    if value == "":
        pass
    else:
        query = "SELECT * FROM vocabulary WHERE " + value
        if restrictors is not None:
            query += " AND " + restrictors  # TODO
        rows = np.array(list(cursor.execute(query)), dtype=data_type)
        if sample_space is not None:
            rows = np.intersect1d(rows, sample_space)
        return np.array([row for row in rows], dtype=data_type)

def random_sample(where):
    query = f"SELECT * FROM vocabulary WHERE id IN (SELECT id FROM vocabulary where {where} ORDER BY RANDOM() LIMIT 1)"
    rows = cursor.execute(query)
    return np.array(list(rows), dtype=data_type)


def get_matched_by(row, label, table=None, subtable=False):
    """
    :param row: ndarray row. selected vocab item.
    :param label: string. field containing selectional restrictions.
    :param table: either a list of tuples specifying a vocabulary table to be drawn from db or a list of vocabulary
        items
    :return: all entries in table whose selectional restrictions in label are matched by row.
    """
    if subtable:
        subset = table
    elif table is None:
        subset = get_table()
    else:
        subset = get_all_conjunctive(table)

    matches = []

    for entry in subset:
        value = str(np.array(entry, dtype=data_type)[label])

        if is_match_disj(row, value):
            matches.append(entry)

    return np.array(matches, dtype=data_type)


def conj_list(conjunction):
    """
    :param conjunction: a string corresponding to a conjunction of selectional restrictions
    :return: a list of k, v pairs
    """
    try:
        to_return = [(v.split("=")[0], v.split("=")[1]) for v in conjunction.strip("()").split(" AND ")]
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
        disjuncts = disjunction.split(" OR ")
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
