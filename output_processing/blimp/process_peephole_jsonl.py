import os.path
import jsonlines

project_root = "/Users/alexwarstadt/Workspace/data_generation"
results_dir = os.path.join(project_root, "results/blimp")
file = os.path.join(results_dir, "blimp_ngram_simplelm_peephole.jsonl")


def fix_ngram():
    with jsonlines.open(file) as reader:
        for obj in reader:
            with jsonlines.Writer(open(os.path.join(results_dir, "blimp_ngram_simplelm_peephole.jsonl"), "w")) as writer:
                writer.write_all(obj)


paradigms = set()
with jsonlines.open(file) as reader:
    for obj in reader:
        paradigms.add(obj["UID"])


def sentence_length(good, bad, paradigm=""):
    try:
        good_length = sum([len(obj["sentence_good"].split()) for obj in good]) / len(good)
        bad_length = sum([len(obj["sentence_good"].split()) for obj in bad]) / len(bad)
        print("%s\t%f\t%f" % (paradigm, good_length - bad_length, good_length / bad_length))
    except ZeroDivisionError:
        print(paradigm + "\t" + "All classified same.")


def print_all_sentence_length():
    for paradigm in paradigms:
        good = []
        bad = []
        with jsonlines.open(file) as reader:
            for obj in reader:
                if obj["UID"] == paradigm:
                    if obj["lm_prob1"] < obj["lm_prob2"]:
                        good.append(obj)
                    else:
                        bad.append(obj)
        sentence_length(good, bad, paradigm)


def separate_good_bad(paradigm):
    good = []
    bad = []
    with jsonlines.open(file) as reader:
        for obj in reader:
            if obj["UID"] == paradigm:
                if obj["lm_prob1"] < obj["lm_prob2"]:
                    good.append(obj)
                else:
                    bad.append(obj)
    return good, bad

def separate_good_bad_ngram(paradigm):
    good = []
    bad = []
    with jsonlines.open(file) as reader:
        for obj in reader:
            if obj["UID"] == paradigm:
                if obj["p_good"] > obj["p_bad"]:
                    good.append(obj)
                else:
                    bad.append(obj)
    return good, bad

good, bad = separate_good_bad_ngram("principle_A_c_command")

pass






