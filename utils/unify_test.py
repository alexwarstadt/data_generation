# Author: Alex Warstadt
# Script for analyzing jiant test outputs

import os
from utils.metadata_parse import *
import sklearn.metrics
import argparse
import sys



def handle_arguments(cl_arguments):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--test_name', '-tn', type=str, default="cola_test.tsv",
                        help="Name of the test output file")
    parser.add_argument('--experiment_type', '-x', type=str,
                        help="Name of experiment/dataset to choose kind of analysis to do")
    parser.add_argument('--test_path', '-t', type=str,
                        help="Path to the full four-column test file")


def process_experiment(experiment_dir, args):
    for run in os.listdir(experiment_dir):
        run_path = os.path.join(experiment_dir, run)
        if os.path.isdir(run_path):
            if args.test_name in os.listdir(run_path):
                if args.experiment_name is "reflexive":


def make_unified_table(experiment_directory):
    for output in os.listdir(experiment_directory):
        if os.path.isfile(os.path.join(experiment_directory, output)):
            old_table = read_data_tsv(os.path.join(experiment_directory, test_full))
            predictions = get_predictions(os.path.join(experiment_directory, output))
            table = unify_table(old_table, predictions)



test_full = "CoLA/test_full.tsv"

def get_predictions(prediction_path, missing_first_line=True):
    predictions = [line.split("\t")[1] for line in open(prediction_path)]
    if missing_first_line:
        predictions[0] = 1
    return predictions

def unify_table(old_table, predictions):
    new_dt = np.dtype(old_table.dtype.descr + [('prediction', 'i1')])
    table = np.zeros(old_table.shape, new_dt)
    for field in old_table.dtype.names:
        table[field] = old_table[field]
    table['prediction'] = predictions
    return table


def reflexives_scores(table):
    in_domain = get_all_conjunctive([("matrix_reflexive", "0")], table)
    out_of_domain = get_all_conjunctive([("matrix_reflexive", "1")], table)
    print("in_domain", sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"]))
    print("out_of_domain", sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"]))
    reflexives = ["himself", "herself", "itself", "themselves"]
    pairs = itertools.combinations(reflexives, 2)
    for pair in pairs:
        sentences = get_all_conjunctive([("refl1", pair[0]), ("refl2", pair[1])], table)
        print(pair[0], pair[1], sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
        sentences = get_all_conjunctive([("refl1", pair[1]), ("refl2", pair[0])], table)
        print(pair[1], pair[0], sklearn.metrics.accuracy_score(sentences["judgment"], sentences["prediction"]))
    print()


def process_reflexives(experiment_directory):
    for output in os.listdir(experiment_directory):
        if os.path.isfile(os.path.join(experiment_directory, output)):
            old_table = read_data_tsv(os.path.join(experiment_directory, test_full))
            predictions = get_predictions(os.path.join(experiment_directory, output))
            table = unify_table(old_table, predictions)
            reflexives_scores(table)




def npi_subsets_score(table, name):
    envs = set(table["env"])
    in_domain_envs = set(name.split("_"))
    in_domain = np.concatenate([get_all("env", env, table) for env in in_domain_envs])
    out_of_domain = np.concatenate([get_all("env", env, table) for env in envs - in_domain_envs])
    print(list(envs-in_domain_envs)[0])
    # out_of_domain = get_all_conjunctive([("env", env) for env in np.setdiff1d(envs, in_domain_envs)], table)
    print("in_domain", sklearn.metrics.accuracy_score(in_domain["judgment"], in_domain["prediction"]))
    print("out_of_domain", sklearn.metrics.accuracy_score(out_of_domain["judgment"], out_of_domain["prediction"]))
    out_of_domain_licensor_in_scope = get_all_conjunctive([("scope", "1"), ("npi_present", "1")], out_of_domain)
    print("NPI_in_scope", sklearn.metrics.accuracy_score(out_of_domain_licensor_in_scope["judgment"],
                                                                            out_of_domain_licensor_in_scope["prediction"]))
    out_of_domain_licensor_out_scope = get_all_conjunctive([("scope", "0"), ("npi_present", "1")], out_of_domain)
    print("NPI_out_scope", sklearn.metrics.accuracy_score(out_of_domain_licensor_out_scope["judgment"],
                                                                             out_of_domain_licensor_out_scope["prediction"]))
    no_npi = get_all_conjunctive([("npi_present", "0")], out_of_domain)
    print("No_NPI", sklearn.metrics.accuracy_score(no_npi["judgment"], no_npi["prediction"]))
    print()


def process_npi_subsets(experiment_directory, name):
    for output in os.listdir(experiment_directory):
        if os.path.isfile(os.path.join(experiment_directory, output)):
            print(output)
            old_table = read_data_tsv(os.path.join(experiment_directory, test_full))
            predictions = get_predictions(os.path.join(experiment_directory, output))
            table = unify_table(old_table, predictions)
            npi_subsets_score(table, name)


# directory = "../outputs/alexs_qp_structure_dependence/reflexive/1k"
# process_reflexives(directory)


directory = "../outputs/npi/subsets_6"
for dir_end in os.listdir("../outputs/npi/subsets_6"):
    print(dir_end)
    process_npi_subsets(os.path.join(directory, dir_end), dir_end)
    print("\n===============================\n")



pass
