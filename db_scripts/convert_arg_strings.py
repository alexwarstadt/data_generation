import pandas as pd
from os import path

def convert_disj(disj):
    disjuncts = disj.split(";")
    new_disjuncts_list = []
    for d in disjuncts:
        conjuncts = d.split("^")
        new_conj_string = " AND ".join(conjuncts)
        if len(conjuncts) > 1 and len(disjuncts) > 1:
            new_conj_string = "(" + new_conj_string + ")"
        new_disjuncts_list.append(new_conj_string)
    return " OR ".join(new_disjuncts_list)


basepath = path.dirname(__file__)
vocab_filepath = path.abspath(path.join(basepath, '..', 'vocabulary.csv'))

vocab_filepath = path.abspath(path.join(basepath, '..', 'vocabulary.csv'))
vocab_db_filepath = path.abspath(path.join(basepath, '..', 'vocabulary_db.csv'))
with open(vocab_filepath, 'r') as file:
    df = pd.read_csv(file, keep_default_na=False)
    df["arg_1"] = df["arg_1"].apply(convert_disj)
    df["arg_2"] = df["arg_2"].apply(convert_disj)
    df["arg_3"] = df["arg_3"].apply(convert_disj)
    df.to_csv(vocab_db_filepath, index_label="id")
    pass
    # reader = csv.reader(file)
    # headers = next(reader)
