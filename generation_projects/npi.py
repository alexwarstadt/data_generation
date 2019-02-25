from utils.vocab_table import *
from utils.randomize import *


def conjugate(verb_row, subj):
    if verb_row["finite"] == "1":
        # if get_one(verb_row, "pres") == "0":
        verb = verb_row[0]
    else:
        if verb_row["ing"] == "1":
            if subj["pl"] == "0":
                verb = "is " + verb_row[0]
            else:
                verb = "are " + verb_row[0]
        elif verb_row["en"] == "1":
            if subj["pl"] == "0":
                verb = "has " + verb_row[0]
            else:
                verb = "have " + verb_row[0]
        else:
           verb = "might " + verb_row[0]
    return verb

def modify_subj_rc(subj):
    subjs = []
    vs = get_matched_by(a, "subj", all_verbs)
    vs = subset(vs, 0.1)
    for v_row in vs:
        verb2 = conjugate(v_row, a)
        if verb2 == "":
            continue
        non_singular = np.append(get_all("pl", "1"), get_all("mass", "1"))
        objects = get_matches_of(v_row, "obj", non_singular)
        objects = subset(objects, 0.5)
        for o_row in objects:
            new_subj_the = "%s who %s the %s" % (subj, verb2, o_row[0])
            new_subj_any = "%s who %s any %s" % (subj, verb2, o_row[0])
            subjs.extend([new_subj_the, new_subj_any])
    return subjs

def quant_N(n):
    return get_matched_by(n, "restrictor_N", all_quants)


all_animate = get_all("animate", "1")
all_quants = get_all("category", "(S/(S\\NP))/N")
all_verbs = get_all("category", "(S\\NP)/NP")
for a in all_animate:
    vs = get_matched_by(a, "subj", all_verbs)
    vs = subset(vs, 0.1)
    qs = quant_N(a)
    qs = subset(qs, 0.5)
    for q in qs:
        subjs = modify_subj_rc(q[0] + " " + a[0])
        subjs = subset(subjs, 0.05)
        for s in subjs:
            for v in vs:
                verb2 = conjugate(v, a)
                if verb2 == "":
                    continue
                objects = get_matches_of(v, "obj")
                objects = subset(objects, 0.5)
                for o in objects:
                    print(s, verb2, "the", o[0])








pass