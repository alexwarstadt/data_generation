import matplotlib.pyplot as plt
from sklearn.metrics import matthews_corrcoef
import numpy as np
import math
import pandas as pd
import os
import seaborn as sns

def get_matthews(examples):
    if type(examples) is pd.core.frame.DataFrame:
        preds = examples["prediction"]
        labels = examples["linguistic_feature_label"]
    else:
        preds = [e["prediction"] for e in examples]
        labels = [e["linguistic_feature_label"] for e in examples]
    return matthews_corrcoef(preds, labels)


def get_accuracy(examples):
    n_total = len(examples)
    if type(examples) is pd.core.frame.DataFrame:
        n_correct = sum(examples["prediction"] == examples["linguistic_feature_label"])
    else:
        n_correct = sum([int(e["prediction"] == e["linguistic_feature_label"]) for e in examples])
    return n_correct / n_total



def get_metrics(result, data):
    templates = list(set(data["template1"]))
    templates.append("overall")
    results = []
    for template in templates:
        template_data = data if template == "overall" else data[data["template1"] == template]
        for domain in ["in", "out"]:
            this_result = result.copy()
            this_result["template"] = template
            this_result["ambiguous"] = domain == "in"
            this_data = template_data[template_data["domain"] == domain]
            if len(this_data) == 0:
                this_result["mcc"] = float("nan")
                this_result["accuracy"] = float("nan")
            else:
                this_result["mcc"] = get_matthews(this_data)
                this_result["accuracy"] = get_accuracy(this_data)
            results.append(this_result)
    return results



def get_roberta_base_results():
    test_set_dir = "../outputs/structure"
    results_dir = "../results/robert_base_results"
    experiments = ["main_verb", "subject_aux_inversion", "reflexive"]

    # Iterate through all experiments, reverse and non-reverse

    all_results = []
    for exp in experiments:
        exp_test_set = pd.read_json(os.path.join(test_set_dir, exp, "test.jsonl"), orient="records", lines=True)
        for rev in ["reverse", "non_reverse"]:

            # add results for each sub-experiment in experiment to dataframe
            exp_results_dir = os.path.join(results_dir, exp, rev)
            for training_set in os.listdir(exp_results_dir):
                if training_set.startswith("."):    # skip hidden files
                    continue
                # f_results = os.path.join(exp_results_dir, training_set, "all_outputs.jsonl")
                results = pd.read_json(os.path.join(exp_results_dir, training_set, "all_outputs.jsonl"), orient="records", lines=True)
                results = pd.concat([results, exp_test_set], axis=1)
                results["template1"] = results["template"].apply(lambda x: x.split(",")[0])
                results["template2"] = results["template"].apply(lambda x: x.split(",")[1:])
                results = results.rename({"pred": "prediction"}, axis=1)
                # print(results.head().to_string())
                # data = get_one_experiment_result(exp_test_set, f_results)
                result = pd.DataFrame([{"training": training_set,
                                        "reverse": rev == "reverse",
                                        "experiment": exp
                                        }])
                # result_df = get_metrics(result, results)
                all_results.extend(get_metrics(result, results))

    all_results = pd.concat(all_results)
    all_results.to_json(os.path.join(results_dir, "all_metrics.jsonl"), orient="records", lines=True)


def get_miniberta_results():
    test_set_dir = "../outputs/structure"
    results_dir = "../results/miniberta_results"
    experiments = ["main_verb", "subject_aux_inversion", "reflexive"]

    # Iterate through all experiments, reverse and non-reverse

    all_results = []
    for exp in experiments:
        exp_test_set = pd.read_json(os.path.join(test_set_dir, exp, "test.jsonl"), orient="records", lines=True)
        for rev in ["reverse", "non_reverse"]:

            # add results for each sub-experiment in experiment to dataframe
            exp_results_dir = os.path.join(results_dir, exp, rev)
            for training_set in os.listdir(exp_results_dir):
                if training_set.startswith("."):  # skip hidden files
                    continue
                training_set_dir = os.path.join(exp_results_dir, training_set)
                for run in os.listdir(training_set_dir):
                    if run.startswith("."):  # skip hidden files
                        continue
                    # f_results = os.path.join(exp_results_dir, training_set, "all_outputs.jsonl")
                    results = pd.read_json(os.path.join(training_set_dir, run, "all_outputs.jsonl"),
                                           orient="records", lines=True)
                    results = pd.concat([results, exp_test_set], axis=1)
                    results["template1"] = results["template"].apply(lambda x: x.split(",")[0])
                    results["template2"] = results["template"].apply(lambda x: x.split(",")[1:])
                    results = results.rename({"pred": "prediction"}, axis=1)
                    # print(results.head().to_string())
                    # data = get_one_experiment_result(exp_test_set, f_results)
                    result = pd.DataFrame([{"training": training_set,
                                            "reverse": rev == "reverse",
                                            "experiment": exp,
                                            "model_id": run.split("_")[1],
                                            "model_size": run.split("_")[0],
                                            }])
                    # result_df = get_metrics(result, results)
                    all_results.extend(get_metrics(result, results))

    all_results = pd.concat(all_results)
    all_results.to_json(os.path.join(results_dir, "all_metrics.jsonl"), orient="records", lines=True)

get_miniberta_results()