# Author: Alex Warstadt
# Script for parsing the metadata column in generated datasets

import numpy as np
from utils.vocab_table import *
import os
import itertools

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

def read_data_tsv(data_file_path):
    """
    :param data_file_path: path to a four-column tsv with metadata in first column
    :return: an ndarray with all metadata as columns
    """
    data_file = open(data_file_path)
    line0 = peek_line(data_file)
    metadata = line0.split("\t")[0].split("-")
    keys = [kv.split("=")[0] for kv in metadata]
    data_type = [(k, "U100") for k in keys] + [("judgment", "i1"), ("sentence", "U10000"), ("original_metadata", "U10000")]
    data_table = []
    for line in data_file:
        columns = line.split("\t")
        metadata = columns[0].split("-")
        values = [kv.split("=")[1] for kv in metadata]
        array_entry = np.array(values + [columns[1], columns[3], columns[0]])
        data_table.append(tuple(array_entry))
    data_table = np.array(data_table, data_type)
    return data_table


def make_subsets(in_domain_size):
    """
    Function that makes datasets for all subsets of the environments, of a certain size
    :param in_domain_size: number of environments to be in-domain
    :return: none. writes to output
    """

    large_table = []
    npi_path = "../data/npi/"
    for file in os.listdir(npi_path):
        if file[-4:] == ".tsv":
            large_table.append(read_data_tsv(os.path.join(npi_path, file)))

    stack = np.concatenate(large_table)
    environments = set(stack["env"])
    output_dir = "../data/npi/subsets_6"
    subsets = list(itertools.combinations(environments, in_domain_size))
    for in_domain in subsets:
        out_domain = np.setdiff1d(list(environments), in_domain)
        in_domain_dir_name = "_".join(in_domain)
        os.mkdir(os.path.join(output_dir, in_domain_dir_name))
        train = open(os.path.join(output_dir, in_domain_dir_name, "train.tsv"), "w")
        test = open(os.path.join(output_dir, in_domain_dir_name, "test_full.tsv"), "w")
        test2 = open(os.path.join(output_dir, in_domain_dir_name, "test.tsv"), "w")
        dev = open(os.path.join(output_dir, in_domain_dir_name, "dev.tsv"), "w")
        test_counter = 0
        for e in in_domain:
            for line in list(filter(lambda x: x["env"] == e, stack)):
                writer = np.random.choice([train, test, dev])
                writer.write("%s\t%s\t\t%s" % (line["original_metadata"], line["judgment"], line["sentence"]))
                if writer == test:
                    test2.write("%d\t%s" % (test_counter, line["sentence"]))
                    test_counter += 1

        for e in out_domain:
            for line in list(filter(lambda x: x["env"] == e, stack)):
                test.write("%s\t%s\t\t%s" % (line["original_metadata"], line["judgment"], line["sentence"]))
                test2.write("%d\t%s" % (test_counter, line["sentence"]))
                test_counter += 1


# make_subsets(6)



