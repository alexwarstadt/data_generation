# extract acceptablity minimal pairs from tsv
# and export pairs into a single tsv
# data split is currently not supported
# most part of this code is almost self-documented, in some sense, I guess?
import sys, argparse
import os
import csv
import numpy
import IPython
from collections import OrderedDict
from pytorch_pretrained_bert import BertTokenizer


# register unpaired data tsv files in data_config
# file: file path and name
# label_id: column index of label
# sent_id: column index of sentence text
data_config = OrderedDict()
# add NPI datasets
NPI_envs = ['adverbs', 'conditionals', 'determiner_negation_biclausal', 'only', \
    'quantifiers', 'questions', 'sentential_negation_biclausal', 'simplequestions', 'superlative']
for key in NPI_envs:
    data_config['NPI-%s' % key] = {
        'file': os.path.join('npi/environments', 'environment=%s.tsv' % key),
        'meta_id': 0,
        'label_id': 1,
        'sent_id': 3}

bert_tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

def meta2tag(meta_0, meta_1):

    condition_variables = ['env', 'licensor', 'scope', 'npi_present']

    def get_condition(meta_str):
        tmp = dict([item.split('=') for item in meta_str.split('-')])
        ans = [tmp[key] for key in condition_variables]
        return ans
    
    meta_0 = get_condition(meta_0)
    meta_1 = get_condition(meta_1)
    condition = "_".join(["%s=%s" % (key, meta_0[i]) \
        if meta_0[i] == meta_1[i] else "%s=%s-%s" % (key, meta_0[i], meta_1[i]) \
            for i, key in enumerate(condition_variables)])
    return condition

def diff(seq_0, seq_1):
    return len([0 for i, j in zip(seq_0, seq_1) if i != j]) == 1  

def extract_pairs(src, config, args):
    file_in = os.path.join(args.data_dir, config['file'])
    print('\nload data from %s' % file_in)
    sents = []
    att2id_dict = {}
    pairs = []
    outputs_by_case = {}
    
    with open(file_in, 'r') as tsv_in:
        tsv_in = csv.reader(tsv_in, delimiter='\t')
        for sent_id, line in enumerate(tsv_in):
            sent_meta = line[config['meta_id']]
            sent_txt = line[config['sent_id']]
            sent_label = int(line[config['label_id']])
            sent_bert = bert_tokenizer.tokenize(sent_txt)
            sents.append({ 'meta': sent_meta, 'txt': sent_txt, 'lable': sent_label, 'bert': sent_bert})
            att = (len(sent_bert), sent_label)
            if att not in att2id_dict:
                att2id_dict[att] = []
            att2id_dict[att].append(sent_id)
    
    for key_0 in att2id_dict.keys():
        s0_bert, s0_label = key_0
        key_1 = (s0_bert, 1 - s0_label)
        if s0_label or (key_1 not in att2id_dict):
            continue
        list_0 = att2id_dict[key_0]
        list_1 = att2id_dict[key_1]
        for sid_0 in list_0:
            for sid_1 in list_1:
                if diff(sents[sid_0]['bert'], sents[sid_1]['bert']):
                    pairs.append((sid_0, sid_1))
    
    numpy.random.shuffle(pairs)
    for (sid_0, sid_1) in pairs:

        s0_txt = sents[sid_0]['txt']
        s1_txt = sents[sid_1]['txt']
        pair_case = meta2tag(sents[sid_0]['meta'], sents[sid_1]['meta'])
        inv = numpy.random.randint(0, 2)
        if pair_case not in outputs_by_case:
            outputs_by_case[pair_case] = []
        if len(outputs_by_case[pair_case]) >= args.max_size:
            continue
        if inv:
            outputs_by_case[pair_case].append([src, s1_txt, s0_txt, 1, pair_case])
        else:
            outputs_by_case[pair_case].append([src, s0_txt, s1_txt, 0, pair_case])

    outputs = []
    for pair_case, outputs_of_case in outputs_by_case.items():
        if len(outputs_of_case) < args.min_size:
            print('\n\ndropped %d pairs from %s' % (len(outputs_of_case), pair_case))            
        else:
            print('\n\ncollected %d pairs from %s' % (len(outputs_of_case), pair_case))
            print('e.g.')
            print(outputs_of_case[:10])
            outputs = outputs + outputs_of_case

    print('\ncollected %d / %d pairs from %s' % (len(outputs), len(pairs), src))
    return outputs

# output format
# acceptability_minimal_pairs.tsv
# column0: src, source tsv file of each pair
# column1: sent1, first sentence in each pair 
# column2: sent2, second sentence in each pair
# column3: label, whether the first sentence is acceptable
# column4: case, which case this pair fall into
# note that, every pair is made of one positive and one negative sentence

def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--data_dir',
        help='directory to save data to',
        type=str,
        default='../outputs')
    parser.add_argument(
        '-M',
        '--max_size',
        help='number of pairs in each unit',
        type=int,
        default='1000'
    )
    parser.add_argument(
        '-m',
        '--min_size',
        help='number of pairs in each unit',
        type=int,
        default='100'
    )
    args = parser.parse_args(arguments)
    outputs = []
    for src, config in data_config.items():
        outputs = outputs + extract_pairs(src, config, args)
    print('collected %d pairs in total' % len(outputs))
    file_out = os.path.join(args.data_dir, 'acceptability_minimal_pairs.tsv')
    with open(file_out, 'w', newline='') as tsv_out:
        tsv_out = csv.writer(tsv_out, delimiter='\t')
        tsv_out.writerows(outputs)
    return

if __name__ == '__main__':
    main(sys.argv[1:])
