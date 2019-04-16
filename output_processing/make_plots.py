import numpy as np
import output_processing.unify_test
import utils.vocab_table
import matplotlib.pyplot as plt
import random



def separate_failed_runs(results_table):
    good = np.array(list(filter(lambda x: x["in_domain_accuracy"] >= 0.9, results_table)), results_table.dtype)
    bad = np.array(list(filter(lambda x: x["in_domain_accuracy"] < 0.9, results_table)), results_table.dtype)
    return good, bad
#
#
# def make_10k_plot():
#     polar_q_summary_path = "../results/structure_dependent_experiments/polar_q_experiment_summary.tsv"
#     polar_q_data_type = output_processing.unify_test.get_results_dtype(True, "polar_q")
#     polar_q_results = np.genfromtxt(polar_q_summary_path, delimiter="\t", names=True, dtype=polar_q_data_type)
#     polar_q_results_10k = utils.vocab_table.get_all("experiment_name", "/scratch/asw462/jiant/structure_dependence/polar_q_experiment/polar_q_10k_sweep", polar_q_results)
#     polar_q_good, polar_q_bad = separate_failed_runs(polar_q_results_10k)
#     polar_q_good_correct = polar_q_good["10"]
#     polar_q_bad_correct = polar_q_bad["10"]
#
#     npi_scope_summary_path = "../results/structure_dependent_experiments/npi_scope_experiment_summary.tsv"
#     npi_scope_data_type = output_processing.unify_test.get_results_dtype(True, "npi_scope")
#     npi_scope_results = np.genfromtxt(npi_scope_summary_path, delimiter="\t", names=True, dtype=npi_scope_data_type)
#     npi_scope_results_10k = utils.vocab_table.get_all("experiment_name", "/scratch/asw462/jiant/structure_dependence/npi_scope_experiment/npi_scope_10k_sweep", npi_scope_results)
#     npi_scope_good, npi_scope_bad = separate_failed_runs(npi_scope_results_10k)
#     npi_scope_good_correct = npi_scope_good["01"]
#     npi_scope_bad_correct = npi_scope_bad["01"]
#
#     reflexive_summary_path = "../results/structure_dependent_experiments/reflexive_experiment_summary.tsv"
#     reflexive_data_type = output_processing.unify_test.get_results_dtype(True, "reflexive")
#     reflexive_results = np.genfromtxt(reflexive_summary_path, delimiter="\t", names=True, dtype=reflexive_data_type)
#     reflexive_results_10k = utils.vocab_table.get_all("experiment_name", "/scratch/asw462/jiant/structure_dependence/reflexive_experiment/reflexive_10k_sweep", reflexive_results)
#     reflexive_good, reflexive_bad = separate_failed_runs(reflexive_results_10k)
#     reflexive_good_correct = reflexive_good["10"]
#     reflexive_bad_correct = reflexive_bad["10"]
#
#     fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
#     ax1.set_ylim([0, 1])
#     ax2.set_ylim([0, 1])
#     ax3.set_ylim([0, 1])
#
#     parts = ax1.violinplot(npi_scope_good_correct, showmeans=False, showextrema=False)
#     parts["bodies"][0].set_facecolor("yellow")
#     ax1.plot([random.uniform(0.95, 1.05) for _ in range(len(npi_scope_good_correct))], npi_scope_good_correct, "or", color="blue")
#     ax1.plot([random.uniform(0.95, 1.05) for _ in range(len(npi_scope_bad_correct))], npi_scope_bad_correct, "or", color="red")
#
#     parts = ax2.violinplot(polar_q_good_correct, showmeans=False, showextrema=False)
#     parts["bodies"][0].set_facecolor("yellow")
#     ax2.plot([random.uniform(0.95, 1.05) for _ in range(len(polar_q_good_correct))], polar_q_good_correct, "or", color="blue")
#     ax2.plot([random.uniform(0.95, 1.05) for _ in range(len(polar_q_bad_correct))], polar_q_bad_correct, "or", color="red")
#
#     parts = ax3.violinplot(reflexive_good_correct, showmeans=False, showextrema=False)
#     parts["bodies"][0].set_facecolor("yellow")
#     ax3.plot([random.uniform(0.95, 1.05) for _ in range(len(reflexive_good_correct))], reflexive_good_correct, "or", color="blue")
#     ax3.plot([random.uniform(0.95, 1.05) for _ in range(len(reflexive_bad_correct))], reflexive_bad_correct, "or", color="red")
#     # ax.set_title('basic plot')
#
#     plt.show()



def set_axis_style(ax, labels, xlabel):
    ax.get_xaxis().set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel(xlabel, fontsize=16)


def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def make_five_sizes_plot(ax, correct_column, experiment_type, ylabel, summary_path, experiment_template):
    sizes = ["100", "300", "1k", "3k", "10k"]
    data_type = output_processing.unify_test.get_results_dtype(True, experiment_type)
    results_table = np.genfromtxt(summary_path, delimiter="\t", names=True, dtype=data_type)
    good_five_sizes = []
    bad_five_sizes = []
    for size in sizes:
        experiment_name = experiment_template % size
        results = utils.vocab_table.get_all("experiment_name", experiment_name, results_table)
        good, bad = separate_failed_runs(results)
        good_five_sizes.append(good[correct_column])
        bad_five_sizes.append(bad[correct_column])
    # fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_ylim([-5, 105])
    set_axis_style(ax, ["100", "300", "1000", "3000", "10000"], "Training Size")
    nans = [float('nan'), float('nan')]
    good_five_sizes = [nans if len(x) == 0 else 100 * x for x in good_five_sizes]
    bad_five_sizes = [nans if len(x) == 0 else 100 * x for x in bad_five_sizes]
    vp = ax.violinplot(good_five_sizes, showmeans=True)
    good_x = [i + random.uniform(0.9, 1.1) for i, exp in enumerate(good_five_sizes) for _ in range(len(exp))]
    good_y = [y for list in good_five_sizes for y in list]
    bad_x = [i + random.uniform(0.9, 1.1) for i, exp in enumerate(bad_five_sizes) for _ in range(len(exp))]
    bad_y = [y for list in bad_five_sizes for y in list]
    ax.plot(good_x, good_y, "x", color="k")
    ax.plot(bad_x, bad_y, "x", color="lightgray")
    ax.set_ylabel(ylabel, fontsize=16)
    for body in vp["bodies"]:
        body.set_facecolor("blue")
    for partname in ['cbars', 'cmins', 'cmaxes', 'cmeans']:
        part = vp[partname]
        part.set_color('k')
        part.set_linewidth(1)
    for partname in ['cmeans']:
        part = vp[partname]
        part.set_color('r')
        part.set_linewidth(1)
    # plt.show()


def make_10k_plot(ax, correct_column, experiment_type, ylabel, summary_path, experiment_template):
    sizes = ["10k"]
    data_type = output_processing.unify_test.get_results_dtype(True, experiment_type)
    results_table = np.genfromtxt(summary_path, delimiter="\t", names=True, dtype=data_type)
    good_five_sizes = []
    bad_five_sizes = []
    for size in sizes:
        experiment_name = experiment_template % size
        results = utils.vocab_table.get_all("experiment_name", experiment_name, results_table)
        good, bad = separate_failed_runs(results)
        good_five_sizes.append(good[correct_column])
        bad_five_sizes.append(bad[correct_column])
    # fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_ylim([-5, 105])
    set_axis_style(ax, [""], "")
    nans = [float('nan'), float('nan')]
    good_five_sizes = [nans if len(x) == 0 else 100 * x for x in good_five_sizes]
    bad_five_sizes = [nans if len(x) == 0 else 100 * x for x in bad_five_sizes]
    vp = ax.violinplot(good_five_sizes, showmeans=True)
    good_x = [i + random.uniform(0.9, 1.1) for i, exp in enumerate(good_five_sizes) for _ in range(len(exp))]
    good_y = [y for list in good_five_sizes for y in list]
    bad_x = [i + random.uniform(0.9, 1.1) for i, exp in enumerate(bad_five_sizes) for _ in range(len(exp))]
    bad_y = [y for list in bad_five_sizes for y in list]
    ax.plot(good_x, good_y, "x", color="k")
    ax.plot(bad_x, bad_y, "x", color="lightgray")
    ax.set_ylabel(ylabel, fontsize=16)
    for body in vp["bodies"]:
        body.set_facecolor("blue")
    for partname in ['cbars', 'cmins', 'cmaxes']:
        part = vp[partname]
        part.set_color('k')
        part.set_linewidth(1)
    for partname in ['cmeans']:
        part = vp[partname]
        part.set_color('r')
        part.set_linewidth(1)


# fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4)
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
ax1.set_title("Reflexive", fontsize=16)
ax2.set_title("Polar Question", fontsize=16)
ax3.set_title("NPI", fontsize=16)
# ax4.set_title("Tense", fontsize=16)


# ========= 5 SIZES PLOTS ==========
# make_five_sizes_plot(ax1, "10", "reflexive", "% OOD Pairs Correct",
#                      "../results/structure_dependent_experiments/reflexive_experiment_summary.tsv",
#                      "/scratch/asw462/jiant/structure_dependence/reflexive_experiment/reflexive_%s_sweep")
#
#
# make_five_sizes_plot(ax2, "10", "polar_q", "",
#                      "../results/structure_dependent_experiments/polar_q_experiment_summary.tsv",
#                      "/scratch/asw462/jiant/structure_dependence/polar_q_experiment/polar_q_%s_sweep")
#
#
# make_five_sizes_plot(ax3, "01", "npi_scope", "",
#                      "../results/structure_dependent_experiments/npi_scope_experiment_summary.tsv",
#                      "/scratch/asw462/jiant/structure_dependence/npi_scope_experiment/npi_scope_%s_sweep")
#
# make_five_sizes_plot(ax4, "10", "embedded_tense", "",
#                      "../results/structure_dependent_experiments/embedded_tense_summary.tsv",
#                      "/scratch/asw462/jiant/structure_dependence/embedded_tense/embedded_tense_%s")
# plt.show()



# ========= 10K PLOTS ==========
# make_10k_plot(ax1, "10", "reflexive", "% OOD Pairs Correct",
#                      "../results/structure_dependent_experiments/reflexive_experiment_summary.tsv",
#                      "/scratch/asw462/jiant/structure_dependence/reflexive_experiment/reflexive_%s_sweep")
#
# make_10k_plot(ax2, "10", "polar_q", "",
#                      "../results/structure_dependent_experiments/polar_q_experiment_summary.tsv",
#                      "/scratch/asw462/jiant/structure_dependence/polar_q_experiment/polar_q_%s_sweep")
#
# make_10k_plot(ax3, "01", "npi_scope", "",
#                      "../results/structure_dependent_experiments/npi_scope_experiment_summary.tsv",
#                      "/scratch/asw462/jiant/structure_dependence/npi_scope_experiment/npi_scope_%s_sweep")
# plt.show()



# ========= EMBEDDED TENSE PLOTS ==========
fig, ax = plt.subplots(nrows=1, ncols=1)
ax.set_title("Tense", fontsize=16)
make_10k_plot(ax, "10", "embedded_tense", "% OOD Pairs Correct",
                     "../results/structure_dependent_experiments/embedded_tense_summary.tsv",
                     "/scratch/asw462/jiant/structure_dependence/embedded_tense/embedded_tense_%s")
plt.show()