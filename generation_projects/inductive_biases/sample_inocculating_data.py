import jsonlines
import os.path
import random

def read_pairs(file):
    pairs = []
    while True:
        try:
            pairs.append((file.read(), file.read()))
        except EOFError:
            break
    return pairs


def unzip_pairs(pairs):
    sentences = [sentence for pair in pairs for sentence in pair]
    return sentences


def unambiguize(dir):
    root = "/Users/alexwarstadt/Workspace/data_generation/outputs/inductive_biases/"
    dir_path = os.path.join(root, dir)
    train_file = jsonlines.open(os.path.join(dir_path, "train.jsonl"))
    train_control_file = jsonlines.open(os.path.join(dir_path, "control_train.jsonl"))
    train_pairs = read_pairs(train_file)
    train_control_pairs = read_pairs(train_control_file)

    percents = [0.0026, 0.005, 0.01, 0.02, 0.04, 0.08, 0.16]
    for p in percents:
        data = random.sample(train_pairs, int(5000.0 * (1 - p)))
        data.extend(random.sample(train_control_pairs, int(5000 * p)))
        output_file = open(os.path.join(dir_path, "train_%s.jsonl" % str(p)), "w")
        w = jsonlines.Writer(output_file)
        data = unzip_pairs(data)
        w.write_all(data)
        w.close()

    test_file = jsonlines.open(os.path.join(dir_path, "test.jsonl"))
    test_control_file = jsonlines.open(os.path.join(dir_path, "control_test.jsonl"))
    test_data = [x for x in test_file]
    test_data.extend([x for x in test_control_file])
    output_file = open(os.path.join(dir_path, "test_combined.jsonl"), "w")
    w = jsonlines.Writer(output_file)
    w.write_all(test_data)
    w.close()

#### MAIN ####
dirs = [
    "antonyms_relative_position",
    "control_raising_length",
    "irregular_form_title_case",
    "syntactic_category_absolute_position",
    "antonyms_lexical_content_the",
        ]
for dir in dirs:
    unambiguize(dir)
