import numpy as np
import sqlite3
from os import path

basepath = path.dirname(__file__)
db_filepath = path.abspath(path.join(basepath, '..', 'lexicon.db'))
connection = sqlite3.connect(db_filepath)

cursor = connection.cursor()

def get_all(label, value):
    query = "SELECT * FROM vocabulary WHERE " + label + " = ?;"
    rows = cursor.execute(query, (value,))
    return np.array([row for row in rows])

def get_all_conj(labels_values):
    select_substr = ''.join(["{} = ? and ".format(pair[0]) for pair in labels_values]).rstrip("and ")
    values = [pair[1] for pair in labels_values]
    query = "SELECT * FROM vocabulary WHERE " + select_substr
    rows = cursor.execute(query, values)
    return np.array([row for row in rows])

def get_matches_of():
    pass

def get_matched_by():
    pass
