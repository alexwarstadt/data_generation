# The purpose of this script is to dynamically go through each column of database and
# change any instances of NULL to the empty string, ""

import sqlite3
import csv

from os import path

basepath = path.dirname(__file__)
db_filepath = path.abspath(path.join(basepath, '..', 'lexicon.db'))
connection = sqlite3.connect(db_filepath)

cursor = connection.cursor()

headers = []

# Open up vocabulary file and read the headers to find value
vocab_filepath = path.abspath(path.join(basepath, '..', 'vocabulary.csv'))
with open(vocab_filepath, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

for header in headers:
    query = "UPDATE vocabulary SET {} = '' WHERE {} IS NULL".format(header, header)
    cursor.execute(query)

connection.commit()
connection.close()
