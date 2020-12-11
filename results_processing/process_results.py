import matplotlib.pyplot as plt
from sklearn.metrics import matthews_corrcoef
import numpy as np
import math

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
        # for v in vals:
        #     if v == "0_0" or v == "0_1" or v == "1_0" or v == "1_1":
        #         vals.remove(v)
        e["template2"] = ",".join(vals[1:])

def parse_condition(examples):
    for e in examples:
        e["condition"] = (e["linguistic_feature_label"], e["surface_feature_label"])
        e["ambiguous"] = True if e["condition"][0] == e["condition"][1] else False

def get_accuracy(examples):
    n_total = len(examples)
    n_correct = sum([int(e["prediction"] == e["linguistic_feature_label"]) for e in examples])
    return n_correct / n_total

def get_pair_accuracy(examples):
    pairs = {}
    for e in examples:
        k = (e["paradigmID"], e["domain"])
        if k not in pairs:
            pairs[k] = []
        pairs[k].append(e["prediction"] == e["linguistic_feature_label"])
    n_pairs = len(pairs)
    n_correct = sum([np.product(p) for p in pairs.values()])
    return n_correct / n_pairs

def get_template_domain(examples, templates, template_key="template"):
    domains = {}
    for t in templates:
        in_domain = np.product([e["domain"] == "in" for e in examples if e[template_key] == t])
        out_domain = np.product([e["domain"] == "out" for e in examples if e[template_key] == t])
        domains[t] = (in_domain, out_domain)
    return domains



def get_matthews(examples):
    preds = [e["prediction"] for e in examples]
    labels = [e["linguistic_feature_label"] for e in examples]
    return matthews_corrcoef(preds, labels)




color_in = "lightskyblue"
color_in2 = "lightcoral"
color_out = "blue"
color_out2 = "red"

def get_accuracy_by_template(examples, templates, template_key="template1"):
    accuracies_1 = []
    accuracies_0 = []
    for t in templates:
        ex_t_1 = [e for e in examples if e[template_key] == t and e["linguistic_feature_label"] == 1]
        ex_t_0 = [e for e in examples if e[template_key] == t and e["linguistic_feature_label"] == 0]
        accuracies_1.append(get_accuracy(ex_t_1))
        accuracies_0.append(get_accuracy(ex_t_0))
    return accuracies_1, accuracies_0

def get_pair_accuracy_by_template(examples, templates, template_key="template1"):
    accuracies = []
    for t in templates:
        ex_t = [e for e in examples if e[template_key] == t]
        accuracies.append(get_pair_accuracy(ex_t))
    return accuracies

def plot_accuracy_by_template(examples, title=None, axs=None):
    all_template1 = set([e["template1"] for e in examples])
    template_domains = get_template_domain(examples, all_template1, "template1")
    in_templates = [t for t in all_template1 if template_domains[t][0]]
    out_templates = [t for t in all_template1 if template_domains[t][1]]

    accuracies_in_1, accuracies_in_0 = get_accuracy_by_template(examples, in_templates)
    accuracies_out_1, accuracies_out_0 = get_accuracy_by_template(examples, out_templates)

    x_in = np.arange(len(in_templates))  # the label locations
    x_out = np.arange(len(out_templates))  # the label locations
    width = 0.35  # the width of the bars
    if axs is None:
        fig, axs = plt.subplots(1, 2)
        if title is not None:
            fig.suptitle(title)

    rects1 = axs[0].bar(x_in - width / 2, accuracies_in_1, width, label='1_1')
    rects2 = axs[0].bar(x_in + width / 2, accuracies_in_0, width, label='0_0')
    axs[0].set_xticks(x_in)
    axs[0].set_xticklabels(in_templates, rotation=30, ha='right')
    axs[0].legend()
    axs[0].set_title("In domain")

    rects3 = axs[1].bar(x_out - width / 2, accuracies_out_1, width, label='1_0')
    rects4 = axs[1].bar(x_out + width / 2, accuracies_out_0, width, label='0_1')
    axs[1].set_xticks(x_out)
    axs[1].set_xticklabels(out_templates, rotation=30, ha='right')
    axs[1].legend()
    axs[1].set_title("out of domain")

    axs[0].set_ylabel("Accuracy")




def plot_pair_accuracy_by_template(examples, title=None, axs=None):
    all_template1 = set([e["template1"] for e in examples])
    template_domains = get_template_domain(examples, all_template1, "template1")
    in_templates = [t for t in all_template1 if template_domains[t][0]]
    out_templates = [t for t in all_template1 if template_domains[t][1]]

    accuracies_in = get_pair_accuracy_by_template(examples, in_templates)
    accuracies_out = get_pair_accuracy_by_template(examples, out_templates)

    x_in = np.arange(len(in_templates))  # the label locations
    x_out = np.arange(len(out_templates))  # the label locations
    width = 0.7  # the width of the bars

    if axs is None:
        fig, axs = plt.subplots(1, 2)
        if title is not None:
            fig.suptitle(title)

    rects1 = axs[0].bar(x_in, accuracies_in, width)
    axs[0].set_xticks(x_in)
    axs[0].set_xticklabels(in_templates, rotation=30, ha='right')
    axs[0].legend()
    axs[0].set_title("In domain")
    axs[0].set_ylim(-0, 1.05)

    rects2 = axs[1].bar(x_out, accuracies_out, width)
    axs[1].set_xticks(x_out)
    axs[1].set_xticklabels(out_templates, rotation=30, ha='right')
    axs[1].legend()
    axs[1].set_title("out of domain")
    axs[1].set_ylim(-0, 1.05)

    axs[0].set_ylabel("Accuracy")




def plot_all_subtemplates(examples):
    all_template1 = set([e["template1"] for e in examples])
    all_template2 = {}
    for t in all_template1:
        all_template2[t] = set([e["template2"] for e in examples if e["template1"] == t])
    width = 3
    height = math.ceil(len(all_template1) / width)
    fig, axs = plt.subplots(width, height)

    template_domains = get_template_domain(examples, all_template1, "template1")
    in_templates = [t for t in all_template1 if template_domains[t][0]]
    out_templates = [t for t in all_template1 if template_domains[t][1]]

    for ax, t in zip(axs.flatten(), all_template1):
        accuracies = [get_accuracy([e for e in examples if e["template2"] == t2]) for t2 in all_template2[t]]
        xs = np.arange(len(all_template2[t]))
        width = 0.7

        colors = []
        for t2 in all_template2[t]:
            if "1_1" in t2:
                colors.append(color_in)
            if "0_0" in t2:
                colors.append(color_in2)
            if "1_0" in t2:
                colors.append(color_out)
            if "0_1" in t2:
                colors.append(color_out2)

        _ = ax.bar(xs, accuracies, width, color=colors)
        ax.set_xticks(xs)
        ax.set_xticklabels(all_template2[t], rotation=30, ha='right', fontsize=8)
        ax.legend()
        ax.set_title(t)
        ax.set_ylim(-0, 1.05)







f_original = "../outputs/structure/subject_aux_inversion/test.jsonl"
f_output = "../results/initial_exps_9dec20/subject_aux_inversion_all_outputs.jsonl"
examples = unify_jsonl_files(f_original, f_output)
parse_template(examples)
# plot_accuracy_by_template(examples, title="Subject Aux Inversion")
plot_all_subtemplates(examples)
plt.show()
pass




