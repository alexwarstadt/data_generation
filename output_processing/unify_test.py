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
    results_summary_output = open(args.results_summary_output, "w")
    for exp_dir in os.listdir(args.main_experiment_dir):
        sub_experiment_dir = os.path.join(args.main_experiment_dir, exp_dir)
        process_experiment(sub_experiment_dir, results_summary_output, args)


def process_experiment(experiment_dir, results_summary_output, args):
    """
    Processes test results for a given experiment.
    :param experiment_dir: the directory that jiant creates for an experiment with "results.tsv"
    :param args: 
    :return: 
    """
    for run in os.listdir(experiment_dir):
        run_dir = os.path.join(experiment_dir, run)
        if os.path.isdir(run_dir):
            test_outputs_path = os.path.join(run_dir, args.test_outputs_name)
            if not os.path.isfile(test_outputs_path):
                continue
            if args.is_experiment_set:
                full_test_path = os.path.join(args.datasets_dir, experiment_dir.split("/")[-1], "CoLA", "test_full.tsv")              # TODO: -2????
            else:
                full_test_path = args.full_test_path
            table = make_unified_table(test_outputs_path, full_test_path)
            if args.experiment_type is "reflexive":
                reflexives_scores(table, results_summary_output)
            if args.experiment_type is "polar_q":
                polar_q_scores(table)
            if args.experiment_type is "npi_scope":
                npi_scope_scores(table)
            if args.experiment_type is "npi_subsets":
                npi_subsets_score(table, experiment_dir)


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



def reflexives_scores(table, results_summary_output):
    in_domain = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "0")], table)
    out_of_domain = utils.vocab_table.get_all_conjunctive([("matrix_reflexive", "1")], table)
    results_summary_output.write("\t".join(["in_domain", sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"])]))
    results_summary_output.write("\t".join(["out_of_domain", sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"])]))
    reflexives = ["himself", "herself", "itself", "themselves"]
    pairs = itertools.combinations(reflexives, 2)
    for pair in pairs:
        sentences = utils.vocab_table.get_all_conjunctive([("refl1", pair[0]), ("refl2", pair[1])], table)
        results_summary_output.write("\t".join([pair[0], pair[1], sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"])]))
        sentences = utils.vocab_table.get_all_conjunctive([("refl1", pair[1]), ("refl2", pair[0])], table)
        results_summary_output.write("\t".join([pair[1], pair[0], sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"])]))
    results_summary_output.write("\n")


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


def polar_q_scores(table):
    pass


def npi_scope_scores(table):
    pass



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
