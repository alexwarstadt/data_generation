import jsonlines
import os.path
import itertools
from utils.vocab_table import *
import numpy as np

project_root = "/".join(os.getcwd().split("/")[:-2])
presuppositions_dir = os.path.join(project_root, "results/IMPPRES/presuppositions/")
results_files = [list(filter(lambda file_name: model_name in file_name, os.listdir(presuppositions_dir)))
                 for model_name in ["bert", "bow", "infersent"]]
for x in results_files:
    x.sort()
data_dir = os.path.join(project_root, "outputs/IMPPRES/presupposition")
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
    "test_unembedded_negated": lambda x: "control_item" not in x.keys() and x["trigger"] == "unembedded" and x["presupposition"] == "negated",
    "test_unembedded_neutral": lambda x: "control_item" not in x.keys() and x["trigger"] == "unembedded" and x["presupposition"] == "neutral",

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

def aggregate_data(results_files, data_files):
    data_sets = [unify_results(results_file, data_file) for results_file, data_file in zip(results_files, data_files)]
    return list(itertools.chain(*data_sets))

right_answers = {
    "test_unembedded_positive": "entailment",
    "test_unembedded_negated": "contradiction",
    "test_unembedded_neutral": "neutral",

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

def finely_summarize_data_to_table(data, trigger, model, filtered):
    results_table = []
    for pair_type_key in right_answers.keys():
        pair_type = get_by_filter(data, pair_type_key)
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

        entry = np.zeros(1, dtype=data_type)
        entry["model"] = model
        entry["filtered"] = filtered
        entry["trigger_type"] = trigger
        entry["condition"] = pair_type_key
        if pair_type_key.startswith("control"):
            entry["control"] = True
            entry["trigger_condition"] = pair_type_key.split("_")[1]
            entry["presupposition_condition"] = ""
        else:
            entry["control"] = False
            entry["trigger_condition"] = pair_type_key.split("_")[1]
            entry["presupposition_condition"] = pair_type_key.split("_")[2]
        entry["entailment"] = entail_n
        entry["neutral"] = neutral_n
        entry["contradiction"] = contra_n
        entry["n_examples"] = len(pair_type)
        if right_answers[pair_type_key] == "entailment":
            entry["accuracy"] = entail_n
        elif right_answers[pair_type_key] == "neutral":
            entry["accuracy"] = neutral_n
        elif right_answers[pair_type_key] == "contradiction":
            entry["accuracy"] = contra_n
        results_table.append(entry)
    return results_table

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

# PUT SUMMARY OF RESULTS IN NUMPY ARRAY
data_type = [
            ("model", "U100000"),
            ("filtered", "?"),
            ("trigger_type", "U100000"),
            ("condition", "U100000"),
            ("control", "?"),
            ("trigger_condition", "U100000"),
            ("presupposition_condition", "U100000"),
            ("accuracy", "f8"),
            ("entailment", "f8"),
            ("neutral", "f8"),
            ("contradiction", "f8"),
            ("n_examples", "i4")
             ]

results_table = []
for model, i in zip(["BERT", "BOW", "InferSent"], [0, 1, 2]):
    all_data = aggregate_data(results_files[i], data_files)
    all_data_filtered = filter_entire_dataset(all_data)
    results_table.extend(finely_summarize_data_to_table(all_data, "all", model=model, filtered=False))
    results_table.extend(finely_summarize_data_to_table(all_data_filtered, "all", model=model, filtered=True))
    for results_file, data_file in zip(results_files[i], data_files):
        data = unify_results(results_file, data_file)
        filtered_data = filter_entire_dataset(data)
        results_table.extend(finely_summarize_data_to_table(data, trigger=data_file.split(".")[0], model=model, filtered=False))
        results_table.extend(finely_summarize_data_to_table(filtered_data, trigger=data_file.split(".")[0], model=model, filtered=True))
results_table = np.array(results_table)

# WRITE SUMMARY TO OUTPUT
def save_csv(results_table, path):
    file = open(path, "w")
    file.write(",".join(results_table.dtype.names) + "\n")
    for line in results_table:
        file.write(",".join([str(x) for x in line[0]]) + "\n")
    file.close()

output_path = os.path.join(project_root, "results/IMPPRES/presupposition_results_summary.csv")
save_csv(results_table, output_path)