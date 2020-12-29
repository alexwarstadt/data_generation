import argparse
import os
import numpy as np
import jsonlines
from itertools import chain, combinations
import random

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))



def sample_split(train_data, test_data, n_total, train_only=False, separate_templates=False, n_templates=None):
    ambiguous_train = [template for template in train_data if template["ambiguous"]]
    ambiguous_test = [template for template in test_data if template["ambiguous"]]
    unambiguous_test = [template for template in test_data if not template["ambiguous"]]
    lengths = [2 * len(x) for x in np.array_split(range(n_total // 2), n_templates)]
    if separate_templates:
        pass  # TODO
    else:
        if train_only:
            to_return_train = []
            ambiguous_sample = np.random.choice(ambiguous_train, n_templates, replace=False)
            train_templates = [t["template"] for t in ambiguous_sample]
            for template, length in zip(ambiguous_sample, lengths):
                to_return_train.extend(template["data"][:length])
            return to_return_train, train_templates
        else:  # both train & test
            pass  # TODO

def sample_all_subsets(train_data, n_total, max_per_size=None, reverse=False):
    usable_templates = [template for template in train_data if template["ambiguous"]] if not reverse \
        else [template for template in train_data if not template["ambiguous"]]
    all_combos = list(powerset(usable_templates))
    training_sets = []
    templates = []
    tracker = {}
    random.shuffle(all_combos)
    for combo in all_combos:
        if max_per_size is not None:
            if len(combo) not in tracker:
                tracker[len(combo)] = 0
            tracker[len(combo)] += 1
            if tracker[len(combo)] > max_per_size:
                continue
        lengths = [2 * len(x) for x in np.array_split(range(n_total // 2), len(combo))]
        curr_training_set = []
        train_templates = "-".join([t["template"] for t in combo])
        for template, length in zip(combo, lengths):
            curr_training_set.extend(template["data"][:length])
        training_sets.append(curr_training_set)
        templates.append(train_templates)
    return training_sets, templates


def make_test_set(test_data, n_each=1000):
    to_return = []
    for template in test_data:
        to_return.extend(template["data"][:n_each])
    return to_return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate datasets with different combinations of templates.")
    parser.add_argument("--directory", type=str, help="Path to directory containing template-only files.")
    parser.add_argument("--n_total", type=int, default=10000, help="Number of examples per dataset.")
    parser.add_argument("--n_templates", type=int, default=3, help="Number of templates to sample training data from.")
    parser.add_argument("--max_per_size", type=int, default=10000, help="In combination with all_subsets, use to set a maximum number of combinations for a given number of templates.")
    parser.add_argument("--test_only", default=False, action="store_true", help="Generate only a test set.")
    parser.add_argument("--all_subsets", default=False, action="store_true", help="Generate all possible training sets.")
    parser.add_argument("--reverse", default=False, action="store_true", help="Swap the in-domain and out-of-domain conditions.")
    parser.add_argument("--separate_templates", default=False, action="store_true", help="Avoid using ambiguous/unambiguous data from same template.")
    args = parser.parse_args()
    train_data = []
    test_data = []
    for file in os.listdir(os.path.join(args.directory, "train")):
        train_data.append({
            "ambiguous": "unambiguous" not in file,
            "template": "_".join(file.split("_")[1:-1]),
            "data": [eval(line) for line in open(os.path.join(args.directory, "train", file))]
        })
        test_data.append({
            "ambiguous": "unambiguous" not in file,
            "template": "_".join(file.split("_")[1:-1]),
            "data": [eval(line) for line in open(os.path.join(args.directory, "test", file))]
        })
    if args.test_only:
        test_sample = make_test_set(test_data)
        output = open(os.path.join(args.directory, "test.jsonl"), "w")
        jsonlines.Writer(output).write_all(test_sample)
    elif args.all_subsets:
        training_sets, templates = sample_all_subsets(train_data, n_total=args.n_total, max_per_size=args.max_per_size, reverse=args.reverse)
        for training_set, templates in zip(training_sets, templates):
            sample_dir = "sampled_training_sets_reverse" if args.reverse else "sampled_training_sets"
            output = open(os.path.join(args.directory, sample_dir, templates + ".jsonl"), "w")
            jsonlines.Writer(output).write_all(training_set)

    else:
        for n_templates in range(1, 5):
            train_sample, train_templates = sample_split(train_data, test_data, n_total=args.n_total, n_templates=n_templates, train_only=True)
            output = open(os.path.join(args.directory, "-".join(train_templates) + ".jsonl"), "w")
            jsonlines.Writer(output).write_all(train_sample)
    pass





