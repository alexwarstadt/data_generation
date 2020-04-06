# Author: Alex Warstadt
# Script for parsing the metadata column in generated datasets in the NPI dataset

import numpy as np
from utils.vocab_table import *
import os
import itertools
import random
import shutil
import re

random.seed(1)

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
    npi_path = "../outputs/npi/environments/"
    for file in os.listdir(npi_path):
        if file[-4:] == ".tsv":
            large_table.append(read_data_tsv(os.path.join(npi_path, file)))

    stack = np.concatenate(large_table)
    environments = set(stack["env"])
    output_dir = "../outputs/npi/subsets_6"
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


def make_splits(test_size=1000, dev_size=1000, train_size=10000):
    """
    Function that makes train/dev/test splits for each enviroment
    :param test_size: number of paradigms in the test set
    :param dev_size: number of paradigms in the test set
    :param train_size: number of environments to be in-domain
    :return: none. writes to output
    """

    npi_path = "../outputs/npi/environments"
    output_dir = "../outputs/npi/environments/splits/"
    for file in os.listdir(npi_path):
        if file[-4:] == ".tsv":
            print("check")
            read_file = read_data_tsv(os.path.join(npi_path, file))
            read_file = np.union1d(get_all("npi", "ever", read_file), get_all("npi", "any", read_file))
            dir_name = file[12:-4]
            if not os.path.isdir(os.path.join(output_dir, dir_name)):
                os.mkdir(os.path.join(output_dir, dir_name))
                
            train = open(os.path.join(output_dir, dir_name, "train.tsv"), "w")
            test = open(os.path.join(output_dir, dir_name, "test_full.tsv"), "w")
            test2 = open(os.path.join(output_dir, dir_name, "test.tsv"), "w")
            test2.write("index\tsentence\n")
            dev = open(os.path.join(output_dir, dir_name, "dev.tsv"), "w")
            test_counter = 0

            paradigm_size = len(list(filter(lambda x: x["paradigm"] == "1", read_file)))

            train_iters = int(train_size / paradigm_size)
            dev_iters = int(dev_size / paradigm_size)
            test_iters = int(test_size / paradigm_size)
    
            paradigms = list(set(read_file["paradigm"]))
            for p in paradigms[:test_iters]:
                for line in list(filter(lambda x: x["paradigm"] == p, read_file)):
                    test.write("%s\t%s\t\t%s" % (line["original_metadata"], line["judgment"], line["sentence"]))
                    test2.write("%d\t%s" % (test_counter, line["sentence"]))
                    test_counter += 1

            for p in paradigms[test_iters:test_iters+dev_iters]:
                for line in list(filter(lambda x: x["paradigm"] == p, read_file)):
                    dev.write("%s\t%s\t\t%s" % (line["original_metadata"], line["judgment"], line["sentence"]))
     
            for p in paradigms[test_iters+dev_iters:test_iters+dev_iters+train_iters]:
                for line in list(filter(lambda x: x["paradigm"] == p, read_file)):
                    train.write("%s\t%s\t\t%s" % (line["original_metadata"], line["judgment"], line["sentence"]))

            train.close()
            test.close()
            test2.close()
            dev.close()


def make_probing_data():
    """
    Function that creates probing datasets for each environment (after splits have been created)
    :return: none. writes to output
    """
    metadata_labels = ['licensor', 'scope', 'npi_present', 'scope_with_licensor']
    npi_path = "../outputs/npi/environments/"
    splits_path = os.path.join(npi_path, 'splits')
    probing_path = os.path.join(npi_path, 'probing')
    split_folders = os.listdir(splits_path)

    if not os.path.isdir(probing_path):
        os.mkdir(probing_path)  

    for split_folder in split_folders:
        if not os.path.isdir(os.path.join(probing_path, split_folder)):
            os.mkdir(os.path.join(probing_path, split_folder))  

        for metadata_label in metadata_labels:      
            if not os.path.isdir(os.path.join(probing_path, split_folder, metadata_label)):
                os.mkdir(os.path.join(probing_path, split_folder, metadata_label))

            split_folder_files = ['train.tsv', 'dev.tsv', 'test_full.tsv']

            for file in split_folder_files:
                infile = open(os.path.join(splits_path, split_folder, file), 'r')
                lines = infile.read().split('\n')
                if metadata_label != 'scope_with_licensor':
                    lines = [re.sub('\t[0-9]\t\t', '\t'+x.split(metadata_label+'=')[1][0]+'\t\t', x) for x in lines if len(x) != 0]
                else:
                    lines = [re.sub('\t[0-9]\t\t', '\t'+x.split('scope=')[1][0]+'\t\t', x) for x in lines if len(x) != 0 and 'licensor=1' in x]
                outfile = open(os.path.join(probing_path, split_folder, metadata_label, file), 'w')
                for line in lines:
                    outfile.write(line+'\n')
                infile.close()
                outfile.close()

            test_full = open(os.path.join(probing_path, split_folder, metadata_label, 'test_full.tsv'), 'r')
            test_full_sentences = test_full.readlines()
            outfile = open(os.path.join(probing_path, split_folder, metadata_label, 'test.tsv'), 'w')
            outfile.write("index\tsentence\n")
            count = 0
            for i in test_full_sentences:
                outfile.write(str(count)+'\t'+i.split('\t')[-1])
                count += 1            

            infile.close()
            outfile.close()
   
def make_combines():
    """
    Function that creates 10 combines for the npi data: 9 all-but-one datasets, 1 all-in-one dataset
    :return: none. writes to output
    """
    npi_path = "../../outputs/npi/environments"
    splits_path = "../../outputs/npi/environments/splits"
    split_folders = os.listdir(splits_path)

    if not os.path.isdir(os.path.join(npi_path, "combs")):
                os.mkdir(os.path.join(npi_path, "combs")) 

    for folder in split_folders + ['all_env']:
        targets = [x for x in split_folders if x != folder]

        if folder == 'all_env':
            folder_tag = 'all_env'
        else:
            folder_tag = "minus_"+folder

        if not os.path.isdir(os.path.join(npi_path, "combs", folder_tag)):
            os.mkdir(os.path.join(npi_path, "combs", folder_tag))


        test = open(os.path.join(npi_path, "combs", folder_tag, 'test.tsv'), 'w')
        test_full = open(os.path.join(npi_path, "combs", folder_tag, 'test_full.tsv'), 'w')
        train = open(os.path.join(npi_path, "combs", folder_tag, 'train.tsv'), 'w')
        dev = open(os.path.join(npi_path, "combs", folder_tag, 'dev.tsv'), 'w')
    
        for x in targets:
            temp = open(os.path.join(splits_path, x, 'test.tsv'), 'r')
            test.write(temp.read().split("index\tsentence\n")[1])
            temp = open(os.path.join(splits_path, x, 'test_full.tsv'), 'r')
            test_full.write(temp.read())   
            temp = open(os.path.join(splits_path, x, 'train.tsv'), 'r')
            train.write(temp.read())   
            temp = open(os.path.join(splits_path, x, 'dev.tsv'), 'r')
            dev.write(temp.read())  

        test = open(os.path.join(npi_path, "combs", folder_tag, 'test.tsv'), 'r')
        test_read = test.readlines()
        test = open(os.path.join(npi_path, "combs", folder_tag, 'test.tsv'), 'w')
        test.write("index\tsentence\n")
        index_count = 0
        for i in test_read:
            test.write(str(index_count)+'\t'+i.split('\t')[1])
            index_count += 1 
        

# add a scope data where licensor is always there
    
# make_subsets(6)
                   
# make_splits(test_size=1000, dev_size=1000, train_size=10000)

# make_probing_data()

make_combines()

     

        
        
        




