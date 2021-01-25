import sqlite3
import csv

from os import path

basepath = path.dirname(__file__)
db_filepath = path.abspath(path.join(basepath, '..', 'lexicon.db'))
connection = sqlite3.connect(db_filepath)

cursor = connection.cursor()
cursor.execute('DELETE FROM vocabulary')

num_records = 0

# Open up vocabulary file and read the headers to find value
vocab_filepath = path.abspath(path.join(basepath, '..', 'vocabulary_db.csv'))
with open(vocab_filepath, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

    for row in file:
        insert_str = "INSERT INTO vocabulary VALUES (" + (len(headers) * "?,").rstrip(',') + ")"
        cursor.execute(insert_str, row.split(','))
        connection.commit()
        num_records += 1

connection.close()
print("\n{} Records added to databases successfully.\n".format(num_records))
