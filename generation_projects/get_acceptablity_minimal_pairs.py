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
from pytorch_pretrained_bert import BertTokenizer, OpenAIGPTTokenizer


# register data tsv files in data_config
# file: file path and name
# label_id: column index of label
# sent_id: column index of sentence text
# units: maximum number of units of sentence pairs to extract from this tsv
data_config = OrderedDict()
# add 7 NPI datasets
for key in ['adverbs', 'conditionals', 'negation', 'only', \
    'quantifiers', 'questions', 'superlative']:
    data_config['NPI-%s' % key] = {
        'file': os.path.join('npi', 'environment=%s.tsv' % key),
        'label_id': 1,
        'sent_id': 3,
        'units': 0.5}
# add 1 plurals dataset
data_config['plurals'] = {
    'file': os.path.join('plurals', 'environment=collectivepredicates.tsv'),
    'label_id': 1,
    'sent_id': 3,
    'units': 1}
# add 1 long_distance dataset
data_config['long_distance'] = {
    'file': os.path.join('long_distance/aux_agreement', 'dev.tsv'),
    'label_id': 1,
    'sent_id': 3,
    'units': 1}
# add 3 qp_structure_dependence datasets
data_config['npi_scope'] = {
    'file': os.path.join('alexs_qp_structure_dependence/npi_scope/10k/CoLA', 'dev.tsv'),
    'label_id': 1,
    'sent_id': 3,
    'units': 1}
data_config['npi_scope'] = {
    'file': os.path.join('alexs_qp_structure_dependence/polar_q/10k', 'dev.tsv'),
    'label_id': 1,
    'sent_id': 3,
    'units': 1}
data_config['reflexive'] = {
    'file': os.path.join('alexs_qp_structure_dependence/reflexive/10k/CoLA', 'dev.tsv'),
    'label_id': 1,
    'sent_id': 3,
    'units': 1}


gpt_tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def diff(seq_0, seq_1):
    return len([0 for i, j in zip(seq_0, seq_1) if i != j]) == 1  

def extract_pairs(src, config, args):
    file_in = os.path.join(args.data_dir, config['file'])
    print('load data from %s' % file_in)
    sents = []
    att2id_dict = {}
    pairs = []
    
    with open(file_in, 'r') as tsv_in:
        tsv_in = csv.reader(tsv_in, delimiter='\t')
        for sent_id, line in enumerate(tsv_in):
            sent_txt = line[config['sent_id']]
            sent_label = int(line[config['label_id']])
            sent_gpt = gpt_tokenizer.tokenize(sent_txt)
            sent_bert = bert_tokenizer.tokenize(sent_txt)
            sents.append({'txt': sent_txt, 'lable': sent_label, \
                'gpt': sent_gpt, 'bert': sent_bert})
            att = (len(sent_gpt), len(sent_bert), sent_label)
            if att not in att2id_dict:
                att2id_dict[att] = []
            att2id_dict[att].append(sent_id)
    
    for key_0 in att2id_dict.keys():
        s0_gpt, s0_bert, s0_label = key_0
        key_1 = (s0_gpt, s0_bert, 1 - s0_label)
        if s0_label or (key_1 not in att2id_dict):
            continue
        list_0 = att2id_dict[key_0]
        list_1 = att2id_dict[key_1]
        for sid_0 in list_0:
            for sid_1 in list_1:
                if diff(sents[sid_0]['gpt'], sents[sid_1]['gpt']) and diff(sents[sid_0]['bert'], sents[sid_1]['bert']):
                    pairs.append((sid_0, sid_1))
    numpy.random.shuffle(pairs)
    sents_used = [0 for sent in sents]
    outputs = []
    for (sid_0, sid_1) in pairs:
        if len(outputs) == int(args.unit_size * config['units']):
            break
        if sents_used[sid_0] or sents_used[sid_1]:
            continue
        s0_txt = sents[sid_0]['txt']
        s1_txt = sents[sid_1]['txt']
        inv = numpy.random.randint(0, 2)
        if inv:
            outputs.append([src, s1_txt, s0_txt, 1])
        else:
            outputs.append([src, s0_txt, s1_txt, 0])
        sents_used[sid_0] = sents_used[sid_1] = 1
    print('collected %d of %d pairs from %s' % (len(outputs), len(pairs), src))
    return outputs

# output format
# acceptability_minimal_pairs.tsv
# column0: src, source tsv file of each pair
# column1: sent1, first sentence in each pair 
# column2: sent2, second sentence in each pair
# column3: label, whether the first sentence is acceptable
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
        '-u',
        '--unit_size',
        help='number of pairs in each unit',
        type=int,
        default='1000'
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
