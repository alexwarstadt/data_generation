from artificial_generation.vocab_table import *
import random

#Template: animate V inanimate

stop_words = ["the",
              "is",
              "might",
              "has",
              "with",
              "who",
              "."]

def decision(probability):
    return random.random() < probability


def svo_write(subj, verb, obj, file):
    for pattern in [("1", subj, verb, obj),
                    ("0", subj, obj, verb),
                    ("0", verb, subj, obj),
                    ("0", verb, obj, subj),
                    ("0", obj, subj, verb),
                    ("0", obj, verb, subj)]:
        if decision(0.16):
            file.write("\t%s\t\t%s %s %s .\n" % pattern)


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



out = open("artificial_data/svo_length", "w")
animate = get_all("Animate", "1")
# inanimate = list(filter(lambda x: x["animate"]==0, vocab))
verbs = get_all("Category", "(S\\NP)/NP")

def write_sentences():
    for s in animate:
        for v in verbs:
            if decision(0.5):
                verb = conjugate(v)
                if verb == "":
                    continue
                objects = get_matches(v, "obj")
                for o in objects:
                    if decision(0.5):
                        subj = "the " + s[0]
                        obj = "the " + o[0]
                        svo_write(subj, verb, obj, out)
                        for mod_s in modify_subj_rc(subj):
                            if decision(0.1):
                                svo_write(mod_s, verb, obj, out)
                        for mod_s in modify_subj_ing(subj):
                            if decision(0.1):
                                svo_write(mod_s, verb, obj, out)
                        for mod_s in modify_subj_with(subj):
                            if decision(0.1):
                                svo_write(mod_s, verb, obj, out)


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


def modify_subj_ing(subj):
    subjs = []
    for v_row in verbs:
        if get_one(v_row, "ing") == "1":
            verb2 = v_row[0]
        else:
            continue
        objects = get_matches(v_row, "obj")
        for o_row in objects:
            obj2 = "the " + o_row[0]
            new_subj = "%s %s %s" % (subj, verb2, obj2)
            subjs.append(new_subj)
    return subjs


def modify_subj_with(subj):
    subjs = []
    appearance = get_all("Appearance", "1")
    # adjective = get_all("Category", "N/N")
    for app in appearance:
        for adj in get_one(app, "adjs").split(";"):
            # if decision(0.2):
                new_subj = "%s with the %s %s" % (subj, adj, app[0])
                subjs.append(new_subj)
    return subjs


def modify_obj_rc(obj):
    objs = []
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

# def write_modified_sentences(subj, verb, obj, out):
#     for v_row in verbs:
#         verb2 = conjugate(v_row)
#         if verb2 == "":
#             continue
#         objects = get_matches(v_row, "obj")
#         for o_row in objects:
#             obj2 = "the " + o_row[0]
#             new_subj = "%s who %s %s" % (subj, verb2, obj2)
#             svo_write(new_subj, verb, obj, out)

write_sentences()



out.close()
