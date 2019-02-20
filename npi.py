from artificial_generation.vocab_table import *
import random



quants = get_all("Category", "(S/(S\\NP))/N")
animate = get_all("Animate", "1")
verbs = get_all("Category", "(S\\NP)/NP")



def conjugate(verb_row):
    verb = ""
    if get_one(verb_row, "finite") == "1":
        if get_one(verb_row, "pres") == "0":
            verb = verb_row[0]
    else:
        if get_one(verb_row, "ing") == "1":
            verb = "is " + verb_row[0]
        elif get_one(verb_row, "en") == "1":
            verb = "has " + verb_row[0]
        else:
           verb = "might " + verb_row[0]
    return verb

def modify_subj_rc(subj):
    subjs = []
    for v_row in verbs:
        verb2 = conjugate(v_row)
        if verb2 == "":
            continue
        objects = get_matches(v_row, "obj")
        for o_row in objects:
            obj2 = "the " + o_row[0]
            new_subj = "%s who %s %s" % (subj, verb2, obj2)
            subjs.append(new_subj)
    return subjs


for a in animate:
    subjs = modify_subj_rc(a)
    for s in subjs:
        for v in verbs:
            objects = get_matches(v, "obj")
            for o in objects:
                print(s[0], v[0], o[0])






pass