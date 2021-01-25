import sqlite3
import csv

from os import path

basepath = path.dirname(__file__)
db_filepath = path.abspath(path.join(basepath, '..', 'lexicon.db'))
connection = sqlite3.connect(db_filepath)

cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS vocabulary")

headers = []

# Open up vocabulary file and read the headers to find value
vocab_filepath = path.abspath(path.join(basepath, '..', 'vocabulary_db.csv'))
with open(vocab_filepath, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)

execution_str = "CREATE TABLE vocabulary (\n"

for header in headers:
    execution_str += header + " text," + "\n"

execution_str = execution_str.rstrip('\n,') + ")"

# Execute Sql command that initializes the database with the table called "lexicon"
cursor.execute(execution_str)

connection.commit()
connection.close()