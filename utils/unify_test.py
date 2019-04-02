# Author: Alex Warstadt
# Script for analyzing jiant test outputs

import os
from utils.metadata_parse import *
import sklearn.metrics

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


directory = "../outputs/alexs_qp_structure_dependence/reflexive/1k"
process_reflexives(directory)


pass
