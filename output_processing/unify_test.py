# Author: Alex Warstadt
# Script for analyzing jiant test outputs

import os
import utils.metadata_parse
import utils.vocab_table
import sklearn.metrics
import argparse
import sys
import numpy as np
import itertools



def handle_arguments(cl_arguments):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--test_outputs_name', '-to', type=str, default="cola_test.tsv",
                        help="Name of the test output file")
    parser.add_argument('--experiment_type', '-x', type=str,
                        help="Name of experiment/dataset to choose kind of analysis to do")
    parser.add_argument('--full_test_path', '-t', type=str,
                        help="Path to the full four-column test file")
    parser.add_argument('--datasets_dir', '-d', type=str,
                        help="Path to all datasets for experiment set")
    parser.add_argument('--results_summary_output', '-r', type=str,
                        help="Path to write outputs of results summary.")
    parser.add_argument('--main_experiment_dir', '-e', type=str,
                        help="Directory containing experiment, or else directory containing set of experiments.")
    parser.add_argument('--is_experiment_set', '-s', type=bool, default=True,
                        help="Is the experiment dir a set of experiments (>1 results.tsv)?")
    return parser.parse_args(cl_arguments)


def process_experiment_set(args):
    results_summary = []
    results_summary_output = open(args.results_summary_output, "w")
    for exp_dir in os.listdir(args.main_experiment_dir):
        if not os.path.isdir(os.path.join(args.main_experiment_dir, exp_dir)):
            continue
        sub_experiment_dir = os.path.join(args.main_experiment_dir, exp_dir)
        results_summary.extend(process_experiment(sub_experiment_dir, args))
    dtype = get_results_dtype(args)
    results_summary = np.array(results_summary, dtype=dtype)
    header = "\t".join(results_summary.dtype.names)
    results_summary_output.write(header + "\n")
    for line in results_summary:
        results_summary_output.write("\t".join([str(x) for x in line]) + "\n")
    results_summary_output.close()

def get_results_dtype(args):
    dtype = []
    if args.is_experiment_set:
        dtype.append(("experiment name", "U100"))
    dtype.append(("run name", "U100"))
    if args.experiment_type == "reflexive":
        dtype.extend([("in domain accuracy", "f8"), ("out of domain accuracy", "f8")])
        dtype.extend([("1/1", "f8"), ("out of domain accuracy", "f8"), ("in domain accuracy", "f8"), ("out of domain accuracy", "f8")])
        # reflexives = ["himself", "herself", "itself", "themselves"]
        # pairs = itertools.combinations(reflexives, 2)
        # for pair in pairs:
        #     dtype.extend([("%s %s accuracy" % (pair[0], pair[1]), "f8"), ("%s %s accuracy" % (pair[1], pair[0]), "f8")])
    if args.experiment_type == "npi_scope":
        dtype.extend([("in domain accuracy", "f8"), ("out of domain accuracy", "f8")])
        dtype.extend([("cond_3_unacceptable", "f8"), ("cond_4_acceptable", "f8")])
        for npi in ["any", "ever", "yet"]:
            dtype.extend([("npi=%s" % npi, "f8"), ("npi=%s_cond_3_unacceptable" % npi, "f8"), ("npi=%s_cond_4_acceptable" % npi, "f8")])
    if args.experiment_type == "polar_q":
        dtype.extend([("in domain accuracy", "f8"), ("out of domain accuracy", "f8")])
        dtype.extend([("cond_3_acceptable", "f8"), ("cond_4_unacceptable", "f8")])
    return dtype

def process_experiment(experiment_dir, args):
    """
    Processes test results for a given experiment.
    :param experiment_dir: the directory that jiant creates for an experiment with "results.tsv"
    :param args: 
    :return: 
    """
    results_summary = []
    for run in os.listdir(experiment_dir):
        new_row = [experiment_dir, run]
        run_dir = os.path.join(experiment_dir, run)
        if os.path.isdir(run_dir):
            test_outputs_path = os.path.join(run_dir, args.test_outputs_name)
            if not os.path.isfile(test_outputs_path):
                continue
            if args.is_experiment_set:
                full_test_path = os.path.join(args.datasets_dir, experiment_dir.split("/")[-1], "CoLA", "test_full.tsv")
            else:
                full_test_path = args.full_test_path
            table = make_unified_table(test_outputs_path, full_test_path)
            if args.experiment_type == "reflexive":
                new_row.extend(reflexives_scores(table))
            if args.experiment_type == "polar_q":
                new_row.extend(polar_q_scores(table))
            if args.experiment_type == "npi_scope":
                new_row.extend(npi_scope_scores(table))
            if args.experiment_type == "npi_subsets":
                npi_subsets_score(table, experiment_dir)
            results_summary.append(tuple(new_row))
    return results_summary


def make_unified_table(test_outputs_path, full_test_path):
    """
    Makes a table with test predictions and test data/metadata combined.
    :param test_outputs_path: file containing the test predictions
    :param args: command-line arguments
    :return: table containing test data, metadata, and predictions
    """
    old_table = utils.metadata_parse.read_data_tsv(full_test_path)
    predictions = get_predictions(test_outputs_path)
    # table = unify_table(old_table, predictions)
    new_dt = np.dtype(old_table.dtype.descr + [('prediction', 'i1')])
    table = np.zeros(old_table.shape, new_dt)
    for field in old_table.dtype.names:
        table[field] = old_table[field]
    table['prediction'] = predictions
    return table


test_full = "CoLA/test_full.tsv"


def get_predictions(test_outputs_path, missing_first_line=True):
    """
    :param test_outputs_path: file containing the test predictions
    :param missing_first_line: 
    :return: 
    """
    predictions = [line.split("\t")[1] for line in open(test_outputs_path)]
    if missing_first_line:
        predictions[0] = 1
    return predictions


def four_outcomes(column_a, column_b):
    outcomes = [0, 0, 0, 0]
    for a, b in zip(column_a, column_b):
        if a == 1 and b == 1:
            outcomes[0] += 1
        if a == 1 and b == 0:
            outcomes[0] += 1
        if a == 0 and b == 1:
            outcomes[0] += 1
        if a == 0 and b == 0:
            outcomes[0] += 1
    return [x / len(column_a) for x in outcomes]


# def reflexives_scores(table):
#     in_domain = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "0")], table)
#     out_of_domain = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "1")], table)
#     in_domain_accuracy = sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"])
#     out_of_domain_accuracy = sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"])
#     results = [in_domain_accuracy, out_of_domain_accuracy]
#     reflexives = ["himself", "herself", "itself", "themselves"]
#     pairs = itertools.combinations(reflexives, 2)
#     for pair in pairs:
#         sentences = utils.vocab_table.get_all_conjunctive([("refl1", pair[0]), ("refl2", pair[1])], table)
#         results.append(sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
#         sentences = utils.vocab_table.get_all_conjunctive([("refl1", pair[1]), ("refl2", pair[0])], table)
#         results.append(sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
#     return results

def reflexives_scores(table):
    in_domain = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "0")], table)
    out_of_domain = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "1")], table)
    in_domain_accuracy = sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"])
    out_of_domain_accuracy = sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"])
    results = [in_domain_accuracy, out_of_domain_accuracy]
    sentences3 = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "1"), ("matrix_antecedent", "1")], table)
    sentences4 = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "1"), ("matrix_antecedent", "0")], table)
    results.extend(four_outcomes(sentences3["prediction"], sentences4["prediction"]))
    return results




# def npi_scope_scores(table):
#     in_domain = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "0")], table)
#     out_of_domain = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "1")], table)
#     in_domain_accuracy = sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"])
#     out_of_domain_accuracy = sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"])
#     results = [in_domain_accuracy, out_of_domain_accuracy]
#     sentences = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "1"), ("npi_embedded", "0")], table)
#     results.append(sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
#     sentences = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "1"), ("npi_embedded", "1")], table)
#     results.append(sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
#     npis = ["any", "ever", "yet"]
#     for npi in npis:
#         sentences = utils.vocab_table.get_all_conjunctive([("npi", npi)], table)
#         results.append(sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
#         sentences = utils.vocab_table.get_all_conjunctive([("npi", npi), ("licensor_embedded", "1"), ("npi_embedded", "0")], table)
#         results.append(sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
#         sentences = utils.vocab_table.get_all_conjunctive([("npi", npi), ("licensor_embedded", "1"), ("npi_embedded", "1")], table)
#         results.append(sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
#     return results

def npi_scope_scores(table):
    in_domain = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "0")], table)
    out_of_domain = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "1")], table)
    in_domain_accuracy = sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"])
    out_of_domain_accuracy = sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"])
    results = [in_domain_accuracy, out_of_domain_accuracy]
    results.extend(four_outcomes(out_of_domain["judgment"], out_of_domain["prediction"]))
    npis = ["any", "ever", "yet"]
    for npi in npis:
        sentences3 = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "1"), ("npi_embedded", "0"), ("npi", npi)], table)
        sentences4 = utils.vocab_table.get_all_conjunctive([("licensor_embedded", "1"), ("npi_embedded", "1"), ("npi", npi)], table)
        results.extend(four_outcomes(sentences3["prediction"], sentences4["prediction"]))
    return results


def polar_q_scores(table):
    in_domain = utils.vocab_table.get_all_conjunctive([("src", "1")], table)
    out_of_domain = utils.vocab_table.get_all_conjunctive([("src", "0")], table)
    in_domain_accuracy = sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"])
    out_of_domain_accuracy = sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"])
    results = [in_domain_accuracy, out_of_domain_accuracy]
    results.extend(four_outcomes(out_of_domain["judgment"], out_of_domain["prediction"]))
    sentences3 = utils.vocab_table.get_all_conjunctive([("src", "0"), ("highest", "1")], table)
    sentences4 = utils.vocab_table.get_all_conjunctive([("src", "0"), ("highest", "0")], table)
    results.extend(four_outcomes(sentences3["prediction"], sentences4["prediction"]))
    return results





def npi_subsets_score(table, name):
    envs = set(table["env"])
    in_domain_envs = set(name.split("_"))
    in_domain = np.concatenate([utils.vocab_table.get_all("env", env, table) for env in in_domain_envs])
    out_of_domain = np.concatenate([utils.vocab_table.get_all("env", env, table) for env in envs - in_domain_envs])
    print(list(envs-in_domain_envs)[0])
    # out_of_domain = get_all_conjunctive([("env", env) for env in np.setdiff1d(envs, in_domain_envs)], table)
    print("in_domain", sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"]))
    print("out_of_domain", sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"]))
    out_of_domain_licensor_in_scope = utils.vocab_table.get_all_conjunctive([("scope", "1"), ("npi_present", "1")], out_of_domain)
    print("NPI_in_scope", sklearn.metrics.accuracy_score(out_of_domain_licensor_in_scope["judgment"],
                                                                            out_of_domain_licensor_in_scope["prediction"]))
    out_of_domain_licensor_out_scope = utils.vocab_table.get_all_conjunctive([("scope", "0"), ("npi_present", "1")], out_of_domain)
    print("NPI_out_scope", sklearn.metrics.accuracy_score(out_of_domain_licensor_out_scope["judgment"],
                                                                             out_of_domain_licensor_out_scope["prediction"]))
    no_npi = utils.vocab_table.get_all_conjunctive([("npi_present", "0")], out_of_domain)
    print("No_NPI", sklearn.metrics.accuracy_score(no_npi["judgment"], no_npi["prediction"]))
    print()




if __name__ == '__main__':
    args = handle_arguments(sys.argv[1:])
    if args.is_experiment_set:
        process_experiment_set(args)
    else:
        process_experiment(args.main_experiment_dir, args)



# def process_npi_subsets(experiment_directory, name):
#     for output in os.listdir(experiment_directory):
#         if os.path.isfile(os.path.join(experiment_directory, output)):
#             print(output)
#             old_table = utils.metadata_parse.read_data_tsv(os.path.join(experiment_directory, test_full))
#             predictions = get_predictions(os.path.join(experiment_directory, output))
#             table = unify_table(old_table, predictions)
#             npi_subsets_score(table, name)
#
#
# def process_reflexives(experiment_directory):
#     for output in os.listdir(experiment_directory):
#         if os.path.isfile(os.path.join(experiment_directory, output)):
#             old_table = utils.metadata_parse.read_data_tsv(os.path.join(experiment_directory, test_full))
#             predictions = get_predictions(os.path.join(experiment_directory, output))
#             table = unify_table(old_table, predictions)
#             reflexives_scores(table)

# directory = "../outputs/alexs_qp_structure_dependence/reflexive/1k"
# process_reflexives(directory)


# directory = "../outputs/npi/subsets_6"
# for dir_end in os.listdir("../outputs/npi/subsets_6"):
#     print(dir_end)
#     process_npi_subsets(os.path.join(directory, dir_end), dir_end)
#     print("\n===============================\n")
#
#
#
# pass
