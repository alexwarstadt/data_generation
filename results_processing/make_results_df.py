import matplotlib.pyplot as plt
from sklearn.metrics import matthews_corrcoef
import numpy as np
import math
import pandas as pd
import os
import seaborn as sns


def unify_jsonl_files(f_original, f_output):
    examples = []
    for line_original, line_output in zip(open(f_original), open(f_output)):
        ex_original, ex_output = eval(line_original), eval(line_output)
        assert(ex_original["sentence_transform"] == ex_output["sentence_transform"])
        ex_original["prediction"] = ex_output["pred"]
        examples.append(ex_original)
    return examples


def parse_template(examples):
    for e in examples:
        vals = e["template"].split(",")
        e["template1"] = vals[0]
        e["template2"] = ",".join(vals[1:])
        # assert(
        #     "1_1" in vals and e["linguistic_feature_label"] == 1 and e["surface_feature_label"] == 1
        #     or "1_0" in vals and e["linguistic_feature_label"] == 1 and e["surface_feature_label"] == 0
        #     or "0_1" in vals and e["linguistic_feature_label"] == 0 and e["surface_feature_label"] == 1
        #     or "0_0" in vals and e["linguistic_feature_label"] == 0 and e["surface_feature_label"] == 0
        # )


def get_one_experiment_result(f_original, f_output):
    examples = unify_jsonl_files(f_original, f_output)
    parse_template(examples)
    return pd.DataFrame(examples)



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
    templates = list(set(data["template"]))
    templates.append("overall")
    results = []
    for template in templates:
        template_data = data if template == "overall" else data[data["template"] == template]
        for domain in ["in", "out"]:
            this_result = result.copy()
            this_result["ambiguous"] = domain == "in"
            this_data = template_data[template_data["domain"] == domain]
            if len(this_data) == 0:
                this_result["mcc"] = float("nan")
                this_result["accuracy"] = float("nan")
            else:
                this_result["mcc"] = get_matthews(this_data)
                this_result["accuracy"] = get_accuracy(this_data)
            results.append(result)
    return pd.concat(results)



test_set_dir = "../outputs/structure"
results_dir = "../results/exps_20jan21"
experiments = ["main_verb", "subject_aux_inversion", "reflexive"]

# Iterate through all experiments, reverse and non-reverse

all_results = []
for exp in experiments:
    exp_test_set = os.path.join(test_set_dir, exp, "test.jsonl")
    for rev in ["reverse", "non_reverse"]:

        # add results for each sub-experiment in experiment to dataframe
        exp_results_dir = os.path.join(results_dir, exp, rev)
        for training_set in os.listdir(exp_results_dir):
            if training_set.startswith("."):    # skip hidden files
                continue
            f_results = os.path.join(exp_results_dir, training_set, "all_outputs.jsonl")
            data = get_one_experiment_result(exp_test_set, f_results)
            result = pd.DataFrame([{"training": training_set,
                                    "reverse": rev == "reverse",
                                    "experiment": exp
                                    }])
            all_results.extend(get_metrics(result, data))

all_results = pd.concat(all_results)
all_results.to_json("../results/exps_20jan21/all_metrics.jsonl", orient="records", lines=True)

pass



#
#
#
# def get_mccs_df(data):
#     mccs = []
#     for domain in ["in", "out"]:
#         this_data = data[data["domain"] == domain]
#         if len(this_data) == 0:
#             mcc = None
#         else:
#             mcc = get_matthews(this_data)
#         mccs.append({
#             "ambiguous": domain == "in",
#             "mcc": mcc,
#         })
#     return pd.DataFrame(mccs)
#
#
#
#
#
#
# def parse_condition(examples):
#     for e in examples:
#         e["condition"] = (e["linguistic_feature_label"], e["surface_feature_label"])
#         e["ambiguous"] = True if e["condition"][0] == e["condition"][1] else False
#
#
# def get_pair_accuracy(examples):
#     pairs = {}
#     for e in examples:
#         k = (e["paradigmID"], e["domain"])
#         if k not in pairs:
#             pairs[k] = []
#         pairs[k].append(e["prediction"] == e["linguistic_feature_label"])
#     n_pairs = len(pairs)
#     n_correct = sum([np.product(p) for p in pairs.values()])
#     return n_correct / n_pairs
#
# def get_template_domain(examples, templates, template_key="template"):
#     domains = {}
#     for t in templates:
#         in_domain = np.product([e["domain"] == "in" for e in examples if e[template_key] == t])
#         out_domain = np.product([e["domain"] == "out" for e in examples if e[template_key] == t])
#         domains[t] = (in_domain, out_domain)
#     return domains
#
#
#
#
#
# color_in = "lightskyblue"
# color_in2 = "lightcoral"
# color_out = "blue"
# color_out2 = "red"
#
# def get_accuracy_by_template(examples, templates, template_key="template1"):
#     accuracies_1 = []
#     accuracies_0 = []
#     for t in templates:
#         ex_t_1 = [e for e in examples if e[template_key] == t and e["linguistic_feature_label"] == 1]
#         ex_t_0 = [e for e in examples if e[template_key] == t and e["linguistic_feature_label"] == 0]
#         accuracies_1.append(get_accuracy(ex_t_1))
#         accuracies_0.append(get_accuracy(ex_t_0))
#     return accuracies_1, accuracies_0
#
# def get_pair_accuracy_by_template(examples, templates, template_key="template1"):
#     accuracies = []
#     for t in templates:
#         ex_t = [e for e in examples if e[template_key] == t]
#         accuracies.append(get_pair_accuracy(ex_t))
#     return accuracies
#
# def plot_accuracy_by_template(examples, title=None, axs=None):
#     all_template1 = set([e["template1"] for e in examples])
#     template_domains = get_template_domain(examples, all_template1, "template1")
#     in_templates = [t for t in all_template1 if template_domains[t][0]]
#     out_templates = [t for t in all_template1 if template_domains[t][1]]
#
#     accuracies_in_1, accuracies_in_0 = get_accuracy_by_template(examples, in_templates)
#     accuracies_out_1, accuracies_out_0 = get_accuracy_by_template(examples, out_templates)
#
#     x_in = np.arange(len(in_templates))  # the label locations
#     x_out = np.arange(len(out_templates))  # the label locations
#     width = 0.35  # the width of the bars
#     if axs is None:
#         fig, axs = plt.subplots(1, 2)
#         if title is not None:
#             fig.suptitle(title)
#
#     rects1 = axs[0].bar(x_in - width / 2, accuracies_in_1, width, label='1_1')
#     rects2 = axs[0].bar(x_in + width / 2, accuracies_in_0, width, label='0_0')
#     axs[0].set_xticks(x_in)
#     axs[0].set_xticklabels(in_templates, rotation=30, ha='right')
#     axs[0].legend()
#     axs[0].set_title("In domain")
#
#     rects3 = axs[1].bar(x_out - width / 2, accuracies_out_1, width, label='1_0')
#     rects4 = axs[1].bar(x_out + width / 2, accuracies_out_0, width, label='0_1')
#     axs[1].set_xticks(x_out)
#     axs[1].set_xticklabels(out_templates, rotation=30, ha='right')
#     axs[1].legend()
#     axs[1].set_title("out of domain")
#
#     axs[0].set_ylabel("Accuracy")
#
#
#
#
# def plot_pair_accuracy_by_template(examples, title=None, axs=None):
#     all_template1 = set([e["template1"] for e in examples])
#     template_domains = get_template_domain(examples, all_template1, "template1")
#     in_templates = [t for t in all_template1 if template_domains[t][0]]
#     out_templates = [t for t in all_template1 if template_domains[t][1]]
#
#     accuracies_in = get_pair_accuracy_by_template(examples, in_templates)
#     accuracies_out = get_pair_accuracy_by_template(examples, out_templates)
#
#     x_in = np.arange(len(in_templates))  # the label locations
#     x_out = np.arange(len(out_templates))  # the label locations
#     width = 0.7  # the width of the bars
#
#     if axs is None:
#         fig, axs = plt.subplots(1, 2)
#         if title is not None:
#             fig.suptitle(title)
#
#     rects1 = axs[0].bar(x_in, accuracies_in, width)
#     axs[0].set_xticks(x_in)
#     axs[0].set_xticklabels(in_templates, rotation=30, ha='right')
#     axs[0].legend()
#     axs[0].set_title("In domain")
#     axs[0].set_ylim(-0, 1.05)
#
#     rects2 = axs[1].bar(x_out, accuracies_out, width)
#     axs[1].set_xticks(x_out)
#     axs[1].set_xticklabels(out_templates, rotation=30, ha='right')
#     axs[1].legend()
#     axs[1].set_title("out of domain")
#     axs[1].set_ylim(-0, 1.05)
#
#     axs[0].set_ylabel("Accuracy")
#
#
#
#
# def plot_all_subtemplates(examples):
#     all_template1 = set([e["template1"] for e in examples])
#     all_template2 = {}
#     for t in all_template1:
#         all_template2[t] = set([e["template2"] for e in examples if e["template1"] == t])
#     width = 3
#     height = math.ceil(len(all_template1) / width)
#     fig, axs = plt.subplots(width, height)
#
#     template_domains = get_template_domain(examples, all_template1, "template1")
#     in_templates = [t for t in all_template1 if template_domains[t][0]]
#     out_templates = [t for t in all_template1 if template_domains[t][1]]
#
#     for ax, t in zip(axs.flatten(), all_template1):
#         accuracies = [get_accuracy([e for e in examples if e["template2"] == t2]) for t2 in all_template2[t]]
#         xs = np.arange(len(all_template2[t]))
#         width = 0.7
#
#         colors = []
#         for t2 in all_template2[t]:
#             if "1_1" in t2:
#                 colors.append(color_in)
#             if "0_0" in t2:
#                 colors.append(color_in2)
#             if "1_0" in t2:
#                 colors.append(color_out)
#             if "0_1" in t2:
#                 colors.append(color_out2)
#
#         _ = ax.bar(xs, accuracies, width, color=colors)
#         ax.set_xticks(xs)
#         ax.set_xticklabels(all_template2[t], rotation=30, ha='right', fontsize=8)
#         ax.legend(["1_1", "0_0", "1_0", "0_1"])
#         ax.set_title(t)
#         ax.set_ylim(-0, 1.05)
#
#
#
# def plot_all_subtemplates_1_plot(data):
#     data_1_1 = data[(data["linguistic_feature_label"] == 1) & (data["surface_feature_label"] == 1)]
#     data_0_0 = data[(data["linguistic_feature_label"] == 0) & (data["surface_feature_label"] == 0)]
#     data_1_0 = data[(data["linguistic_feature_label"] == 1) & (data["surface_feature_label"] == 0)]
#     data_0_1 = data[(data["linguistic_feature_label"] == 0) & (data["surface_feature_label"] == 1)]
#     data_by_condition = [data_1_1, data_0_0, data_1_0, data_0_1]
#     n_templates = [len(set(data["template1"])) for data in data_by_condition]
#     gs = {"width_ratios": [1], "height_ratios": n_templates}
#     fig, axs = plt.subplots(ncols=1, nrows=4, gridspec_kw=gs)
#
#
#     width = 0.7
#     for data, ax, condition in zip([data_1_1, data_0_0, data_1_0, data_0_1], axs.flatten(), ["1_1", "0_0", "1_0", "0_1"]):
#         all_template1 = set(data["template1"])
#
#         # accuracies = [get_accuracy([d for d in data if d["template2"] == t2]) for t2 in all_template2[t]]
#
#         accuracies = [get_accuracy(data[data["template1"] == t1]) for t1 in all_template1]
#         ys = np.arange(len(all_template1))
#         ax.barh(ys, accuracies, width)
#         ax.set_xlim(-0, 1.05)
#         # condition = (data["linguistic_feature_label"].iloc(0), data["surface_feature_label"].iloc(0))
#         ax.set_title(condition)
#         ax.set_yticks(ys)
#         ax.set_yticklabels(all_template1, ha='right', fontsize=8)
#     plt.tight_layout()
#     plt.subplots_adjust(hspace=0.2)
#
#
#
#
# def get_accuracies_df_by_template(data):
#     accuracies = []
#     all_template1 = set(data["template1"])
#     for linguistic_feature_label in [0, 1]:
#         for surface_feature_label in [0, 1]:
#             for template in all_template1:
#                 this_data = data[
#                     (data["linguistic_feature_label"] == linguistic_feature_label)
#                     & (data["surface_feature_label"] == surface_feature_label)
#                     & (data["template1"] == template)
#                 ]
#                 if len(this_data) == 0:
#                     acc = None
#                 else:
#                     acc = get_accuracy(this_data)
#                 accuracies.append({
#                     "template": template,
#                     "linguistic_feature_label": linguistic_feature_label,
#                     "surface_feature_label": surface_feature_label,
#                     "condition": str(linguistic_feature_label) + "_" + str(surface_feature_label),
#                     "ambiguous": linguistic_feature_label == surface_feature_label,
#                     "accuracy": acc,
#
#                 })
#     return pd.DataFrame(accuracies)
#
# def get_accuracies_df(data):
#     accuracies = []
#     for linguistic_feature_label in [0, 1]:
#         for surface_feature_label in [0, 1]:
#                 this_data = data[
#                     (data["linguistic_feature_label"] == linguistic_feature_label)
#                     & (data["surface_feature_label"] == surface_feature_label)
#                 ]
#                 if len(this_data) == 0:
#                     acc = None
#                 else:
#                     acc = get_accuracy(this_data)
#                 accuracies.append({
#                     "linguistic_feature_label": linguistic_feature_label,
#                     "surface_feature_label": surface_feature_label,
#                     "condition": str(linguistic_feature_label) + "_" + str(surface_feature_label),
#                     "ambiguous": linguistic_feature_label == surface_feature_label,
#                     "accuracy": acc,
#
#                 })
#     return pd.DataFrame(accuracies)
#
#
# def get_mccs_df_by_template(data):
#     mccs = []
#     all_template1 = set(data["template1"])
#     for domain in ["in", "out"]:
#         for template in all_template1:
#             this_data = data[
#                 (data["domain"] == domain)
#                 & (data["template1"] == template)
#                 ]
#             if len(this_data) == 0:
#                 mcc = None
#             else:
#                 mcc = get_matthews(this_data)
#             mccs.append({
#                 "template": template,
#                 "ambiguous": domain == "in",
#                 "mcc": mcc,
#
#             })
#     return pd.DataFrame(mccs)
#
#
# def get_mccs_df(data):
#     mccs = []
#     for domain in ["in", "out"]:
#         this_data = data[data["domain"] == domain]
#         if len(this_data) == 0:
#             mcc = None
#         else:
#             mcc = get_matthews(this_data)
#         mccs.append({
#             "ambiguous": domain == "in",
#             "mcc": mcc,
#         })
#     return pd.DataFrame(mccs)
#
#
#
#
# def join_all_training_sets(f_original, results_dir, function):
#     # f_original = "../outputs/structure/main_verb/test.jsonl"
#     # results_dir = "../results/exps_20jan21/main_verb/non_reverse/"
#     all_results = []
#     for training_set in os.listdir(results_dir):
#         if training_set.startswith("."):
#             continue
#         f_results = os.path.join(results_dir, training_set, "all_outputs.jsonl")
#         data = get_one_experiment_result(f_original, f_results)
#         results = function(data)
#         results["training"] = training_set
#         all_results.append(results)
#     all_results = pd.concat(all_results)
#     # print(all_results.to_string())
#     return all_results
#
#
#
#



