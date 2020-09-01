import sqlite3, csv

conn = sqlite3.connect('./../lexicon.db')

c = conn.cursor()

with open('./../vocabulary.csv', 'r') as file:
    for row in file:
        pass