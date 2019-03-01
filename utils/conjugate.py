



def conjugate(verb, subj):
    if verb["finite"] == "1":
        verb_str = verb[0]
    else:
        if verb["ing"] == "1":
            if subj["pl"] == "0":
                verb_str = "is " + verb[0]
            else:
                verb_str = "are " + verb[0]
        elif verb["en"] == "1":
            if subj["pl"] == "0":
                verb_str = "has " + verb[0]
            else:
                verb_str = "have " + verb[0]
        else:
           verb_str = "might " + verb[0]
    verb[0] = verb_str
    return verb