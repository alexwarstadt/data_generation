import numpy as np


data_type = [("Expression", "U20"),
             ("Category", "U20"),
             ("Animate", "U1"),
             ("Occupation", "U1"),
             ("Clothing", "U1"),
             ("Appearance", "U1"),
             ("Thing", "U1"),
             ("Sg", "U1"),
             ("Pl", "U1"),
             ("Mass", "U1"),
             ("finite", "U1"),
             ("pres", "U1"),
             ("ing", "U1"),
             ("en", "U1"),
             ("3sg", "U1"),
             ("subj", "U20"),
             ("obj", "U20"),
             ("root", "U20"),
             ("adjs", "U100"),
             ("restrictor_N", "U100"),
             ("restrictor_DE", "U100"),
             ("scope_DE", "U100")
            ]


vocab = np.genfromtxt("vocabulary.csv", delimiter=",", names=True, dtype=data_type)

def get_all(label, value):
    return np.array(list(filter(lambda x: x[label]==value, vocab)), dtype=data_type)

def get_all_from(label, value, table):
    return np.array(list(filter(lambda x: x[label]==value, table)), dtype=data_type)

def get_matches(row, label):
    value = str(np.array(row, dtype=data_type)[label])
    if value == "":
        pass
    else:
        matches = []
        values = str(value).split("|")
        for v in values:
            v = v.split("=")
            matches.extend(list(get_all(v[0], str(v[1]))))
        return np.array(matches, dtype=data_type)


def get_one(row, label):
    return str(np.array(row, dtype=data_type)[label])

pass
