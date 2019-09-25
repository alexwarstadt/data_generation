import numpy as np
import jsonlines
import os
import itertools
from utils.vocab_table import get_all
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


presuppositions_dir = "/Users/alexwarstadt/Workspace/data_generation/results/nli/presuppositions/"

results_files = [list(filter(lambda file_name: model_name in file_name, os.listdir(presuppositions_dir)))
                 for model_name in ["bert", "bow", "infersent"]]
for x in results_files:
    x.sort()
data_dir = "/Users/alexwarstadt/Workspace/data_generation/outputs/nli/"
data_files = list(filter(lambda x: "jsonl" in x and "scalar" not in x, os.listdir(data_dir)))
data_files.sort()


def unify_results(results_file, data_file):
    results = np.load(os.path.join(presuppositions_dir, results_file))
    data = [l for l in jsonlines.Reader(open(os.path.join(data_dir, data_file))).iter()]
    for r, d in zip(results, data):
        d["pred_entailment"] = r[0]
        d["pred_neutral"] = r[1]
        d["pred_contradiction"] = r[2]
    return data





def correct_prediction(datum):
    if datum["gold_label"] == "entailment":
        correct = True if datum["pred_entailment"] > datum["pred_contradiction"] \
                          and datum["pred_entailment"] > datum["pred_neutral"] else False
    if datum["gold_label"] == "neutral":
        correct = True if datum["pred_neutral"] > datum["pred_contradiction"] \
                          and datum["pred_neutral"] > datum["pred_entailment"] else False
    if datum["gold_label"] == "contradiction":
        correct = True if datum["pred_contradiction"] > datum["pred_entailment"] \
                          and datum["pred_contradiction"] > datum["pred_neutral"] else False
    return correct

def accuracy(data):
    n_correct = 0
    n_total = 0
    for d in data:
        d["correct"] = correct_prediction(d)
        if correct_prediction(d):
            n_correct += 1
        n_total += 1
    return n_correct / n_total

            

def get_controls(data):
    control_data = list(filter(lambda x: "control_item" in x.keys(), data))
    return control_data

def get_controls_contradictions(data):
    control_data = list(filter(lambda x: "control_item" in x.keys() and x["trigger1"] == "negated", data))
    return control_data

def get_basic_prsp(data):
    control_data = list(filter(lambda x: "trigger" in x.keys() and x["trigger"] == "unembedded" and x["presupposition"] == "positive", data))
    return control_data

filters = {
    "all": lambda x: True,
    "test_item": lambda x: "control_item" not in x.keys(),
    "control": lambda x: "control_item" in x.keys(),

    "test_unembedded_*": lambda x: "control_item" not in x.keys() and x["trigger"] == "unembedded",
    "test_negated_*": lambda x: "control_item" not in x.keys() and x["trigger"] == "negated",
    "test_interrogative_*": lambda x: "control_item" not in x.keys() and x["trigger"] == "interrogative",
    "test_modal_*": lambda x: "control_item" not in x.keys() and x["trigger"] == "modal",
    "test_conditional_*": lambda x: "control_item" not in x.keys() and x["trigger"] == "conditional",

    "test_*_positive": lambda x: "control_item" not in x.keys() and x["presupposition"] == "positive",
    "test_*_negated": lambda x: "control_item" not in x.keys() and x["presupposition"] == "negated",
    "test_*_neutral": lambda x: "control_item" not in x.keys() and x["presupposition"] == "neutral",

    "test_unembedded_positive": lambda x: "control_item" not in x.keys() and x["trigger"] == "unembedded" and x["presupposition"] == "positive",
    "test_unumbedded_negated": lambda x: "control_item" not in x.keys() and x["trigger"] == "unembedded" and x["presupposition"] == "negated",
    "test_unumbedded_neutral": lambda x: "control_item" not in x.keys() and x["trigger"] == "unembedded" and x["presupposition"] == "neutral",

    "test_negated_positive": lambda x: "control_item" not in x.keys() and x["trigger"] == "negated" and x["presupposition"] == "positive",
    "test_negated_negated": lambda x: "control_item" not in x.keys() and x["trigger"] == "negated" and x["presupposition"] == "negated",
    "test_negated_neutral": lambda x: "control_item" not in x.keys() and x["trigger"] == "negated" and x["presupposition"] == "neutral",

    "test_interrogative_positive": lambda x: "control_item" not in x.keys() and x["trigger"] == "interrogative" and x["presupposition"] == "positive",
    "test_interrogative_negated": lambda x: "control_item" not in x.keys() and x["trigger"] == "interrogative" and x["presupposition"] == "negated",
    "test_interrogative_neutral": lambda x: "control_item" not in x.keys() and x["trigger"] == "interrogative" and x["presupposition"] == "neutral",

    "test_modal_positive": lambda x: "control_item" not in x.keys() and x["trigger"] == "modal" and x["presupposition"] == "positive",
    "test_modal_negated": lambda x: "control_item" not in x.keys() and x["trigger"] == "modal" and x["presupposition"] == "negated",
    "test_modal_neutral": lambda x: "control_item" not in x.keys() and x["trigger"] == "modal" and x["presupposition"] == "neutral",

    "test_conditional_positive": lambda x: "control_item" not in x.keys() and x["trigger"] == "conditional" and x["presupposition"] == "positive",
    "test_conditional_negated": lambda x: "control_item" not in x.keys() and x["trigger"] == "conditional" and x["presupposition"] == "negated",
    "test_conditional_neutral": lambda x: "control_item" not in x.keys() and x["trigger"] == "conditional" and x["presupposition"] == "neutral",

    "control_negated": lambda x: "control_item" in x.keys() and x["trigger1"] == "negated",
    "control_modal": lambda x: "control_item" in x.keys() and x["trigger1"] == "modal",
    "control_interrogative": lambda x: "control_item" in x.keys() and x["trigger1"] == "interrogative",
    "control_conditional": lambda x: "control_item" in x.keys() and x["trigger1"] == "conditional",
}

def get_by_filter(data, filter_key, one=False):
    if one:
        return list(filter(filters[filter_key], data))[0]
    else:
        return list(filter(filters[filter_key], data))


def get_different_negations(data):
    negations = ["it's not the case that",
                 "it's false that",
                 "it's not true that",
                 "it's incorrect to say that",
                 "it's a lie that",
                 "is mistaken that",
                 "is wrong that",
                 "lied that",
                 "falsely believes that"]
    for neg in negations:
        neg_data = list(filter(lambda x: neg in x["sentence1"] or neg.capitalize() in x["sentence1"], data))
        print("Contradictions\tneg=%s\tn=%d\taccuracy=%f" % (neg, len(neg_data), accuracy(neg_data)))



def get_bare_form_str(verb_str):
    words = verb_str.split(" ")
    words[0] = lemmatizer.lemmatize(words[0], "v")
    return " ".join(words)


def get_different_interrogatives(data):
    rogatives = list(set([get_bare_form_str(verb[0]) for verb in get_all("category", "(S\\NP)/Q")]))
    for rog in rogatives:
        rog_data = list(filter(lambda x: rog in x["sentence1"] or rog.capitalize() in x["sentence1"], data))
        print("rog=%s\tn=%d\taccuracy=%f" % (rog, len(rog_data), accuracy(rog_data)))


def get_different_modals(data):
    modals = ["it's possible that",
              "it might be true that",
              "it's conceivable that",
              "it's unlikely that",
              "it's likely that",
              "it might turn out that",
              "might be right that",
              "believes that",
              "is under the impression that",
              "is probably correct that",
              ]
    for modal in modals:
        modal_data = list(filter(lambda x: modal in x["sentence1"] or modal.capitalize() in x["sentence1"], data))
        print("modal=%s\tn=%d\taccuracy=%f" % (modal, len(modal_data), accuracy(modal_data)))


def get_different_conditionals(data):
    conditionals = ["if",
                    "no matter if",
                    "whether or not",
                    "assuming that",
                    "on the condition that",
                    "under the circumstances that",
                    "should it be true that",
                    "supposing that"]
    for conditional in conditionals:
        conditional_data = list(filter(lambda x: conditional in x["sentence1"] or conditional.capitalize() in x["sentence1"], data))
        print("modal=%s\tn=%d\taccuracy=%f" % (conditional, len(conditional_data), accuracy(conditional_data)))



def aggregate_data(results_files, data_files):
    data_sets = [unify_results(results_file, data_file) for results_file, data_file in zip(results_files, data_files)]
    return list(itertools.chain(*data_sets))

def summarize_data_file(results_file, data_file, label=None):
    data_set = unify_results(results_file, data_file)
    summarize_data(data_set, label)

def finely_summarize_data_file(results_file, data_file, label=None):
    data_set = unify_results(results_file, data_file)
    finely_summarize_data(data_set, label)


def summarize_data(data, label=None):
    if label is not None:
        print("============================")
        print(label)
    for filter_key in filters.keys():
        data_subset = get_by_filter(data, filter_key)
        if len(data_subset) == 0:
           print("%s\t%f\t%d" % (filter_key, 0, 0))
        else:
           print("%s\t%f\t%d" % (filter_key, accuracy(data_subset), len(data_subset)))
    print()


right_answers = {
    "test_unembedded_positive": "entailment",
    "test_unumbedded_negated": "contradiction",
    "test_unumbedded_neutral": "neutral",

    "test_negated_positive": "entailment",
    "test_negated_negated": "contradiction",
    "test_negated_neutral": "neutral",

    "test_interrogative_positive": "entailment",
    "test_interrogative_negated": "contradiction",
    "test_interrogative_neutral": "neutral",

    "test_modal_positive": "entailment",
    "test_modal_negated": "contradiction",
    "test_modal_neutral": "neutral",

    "test_conditional_positive": "entailment",
    "test_conditional_negated": "contradiction",
    "test_conditional_neutral": "neutral",

    "test_*_positive": "entailment",
    "test_*_negated": "contradiction",
    "test_*_neutral": "neutral",

    "control_negated": "contradiction",
    "control_modal": "neutral",
    "control_interrogative": "neutral",
    "control_conditional": "neutral",
}

def finely_summarize_data(data, label=None):
    if label is not None:
        print("============================")
        print(label)
    for pair_type_key in right_answers.keys():
        pair_type = get_by_filter(data, pair_type_key)
        # entail_avg = sum([d["pred_entailment"] for d in pair_type]) / len(pair_type)
        # neutral_avg = sum([d["pred_neutral"] for d in pair_type]) / len(pair_type)
        # contra_avg = sum([d["pred_contradiction"] for d in pair_type]) / len(pair_type)
        try:
            entail_n = sum([1 if d["pred_entailment"] > d["pred_neutral"] and d["pred_entailment"] > d["pred_contradiction"]
                            else 0 for d in pair_type]) / len(pair_type)
            neutral_n = sum([1 if d["pred_neutral"] > d["pred_entailment"] and d["pred_neutral"] > d["pred_contradiction"]
                            else 0 for d in pair_type]) / len(pair_type)
            contra_n = sum([1 if d["pred_contradiction"] > d["pred_neutral"] and d["pred_contradiction"] > d["pred_entailment"]
                            else 0 for d in pair_type]) / len(pair_type)
        except ZeroDivisionError:
            entail_n = 0
            neutral_n = 0
            contra_n = 0
        if right_answers[pair_type_key] == "entailment":
            print("%s\t*%.3f*\t%.3f\t%.3f\t%d" % (pair_type_key, entail_n, neutral_n, contra_n, len(pair_type)))
        elif right_answers[pair_type_key] == "neutral":
            print("%s\t%.3f\t*%.3f*\t%.3f\t%d" % (pair_type_key, entail_n, neutral_n, contra_n, len(pair_type)))
        elif right_answers[pair_type_key] == "contradiction":
            print("%s\t%.3f\t%.3f\t*%.3f*\t%d" % (pair_type_key, entail_n, neutral_n, contra_n, len(pair_type)))

        # if right_answers[pair_type_key] == "entailment":
        #     print("%s\t*%f*\t%f\t%f\t|\t*%f*\t%f\t%f" % (pair_type_key, entail_avg, neutral_avg, contra_avg, entail_n, neutral_n, contra_n))
        # elif right_answers[pair_type_key] == "neutral":
        #     print("%s\t%f\t*%f*\t%f\t|\t%f\t*%f*\t%f" % (pair_type_key, entail_avg, neutral_avg, contra_avg, entail_n, neutral_n, contra_n))
        # elif right_answers[pair_type_key] == "contradiction":
        #     print("%s\t%f\t%f\t*%f*\t|\t%f\t%f\t*%f*" % (pair_type_key, entail_avg, neutral_avg, contra_avg, entail_n, neutral_n, contra_n))



def split_into_paradigms(data):
    paradigms = []
    n_curr_paradigm = -1
    l_curr_paradigm = []
    for d in data:
        if n_curr_paradigm != d["paradigmID"]:
            n_curr_paradigm = d["paradigmID"]
            if len(l_curr_paradigm) > 0:
                paradigms.append(l_curr_paradigm)
                l_curr_paradigm = []
        l_curr_paradigm.append(d)
    paradigms.append(l_curr_paradigm)
    return paradigms


def filter_paradigm(paradigm):
    filtered = []
    if not correct_prediction(get_by_filter(paradigm, "test_unembedded_positive", one=True)):
        return filtered
    else:
        filtered.extend(get_by_filter(paradigm, "test_unembedded_*"))
    if correct_prediction(get_by_filter(paradigm, "control_negated", one=True)):
        filtered.extend(get_by_filter(paradigm, "test_negated_*"))
    if correct_prediction(get_by_filter(paradigm, "control_modal", one=True)):
        filtered.extend(get_by_filter(paradigm, "test_modal_*"))
    if correct_prediction(get_by_filter(paradigm, "control_interrogative", one=True)):
        filtered.extend(get_by_filter(paradigm, "test_interrogative_*"))
    if correct_prediction(get_by_filter(paradigm, "control_conditional", one=True)):
        filtered.extend(get_by_filter(paradigm, "test_conditional_*"))
    return filtered


def filter_entire_dataset(dataset):
    paradigms = split_into_paradigms(dataset)
    filtered_paradigms = [filter_paradigm(p) for p in paradigms]
    filtered_paradigms = filter(lambda x: x != [], filtered_paradigms)
    return list(itertools.chain(*filtered_paradigms))



###### MAIN ######

for x in [0, 1, 2]:
    print(results_files[x][0])
    all_data = aggregate_data(results_files[x], data_files)
    all_data_filtered = filter_entire_dataset(all_data)
    finely_summarize_data(all_data, "all")
    # summarize_data(all_data, "all")
    finely_summarize_data(all_data_filtered, "all")
    for results_file, data_file in zip(results_files[x], data_files):
        data = unify_results(results_file, data_file)
        # summarize_data(data, label=data_file)
        filtered_data = filter_entire_dataset(data)
        finely_summarize_data(data, label=data_file + " unfiltered")
        finely_summarize_data(filtered_data, label=data_file + " filtered")
        print()





# summarize_data(all_data, label="all")

# get_different_negations(list(filter(filters["control_negated"], all_data)))
# get_different_interrogatives(list(filter(filters["control_interrogative"], all_data)))
# get_different_modals(list(filter(filters["control_modal"], all_data)))
# get_different_conditionals(list(filter(filters["control_conditional"], all_data)))






pass