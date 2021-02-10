import os
import pandas as pd


mapping = {"npi": [1, 0, 1, 1],
           "reflexive": [1, 0, 1, 1],
           "subject_aux_inversion": [1, 0, 0, 1],
           "tense": [1, 0, 1, 1]
           }

for experiment in os.listdir("tsv"):
    for split in os.listdir(os.path.join("tsv", experiment)):
        if split == "test.tsv":     # Use test_ful instead
            continue
        df = pd.read_csv(os.path.join("tsv", experiment, split), delimiter="\t", usecols=[0, 1, 3], names=["metadata", "linguistic_feature_label", "sentence"])
        def get_surface_label(i):
            if "test" in split:
                label = mapping[experiment][i%4]
            else:
                label = mapping[experiment][i%2]
            return label
        df["surface_feature_label"] = df.index.map(get_surface_label)
        if not os.path.exists(os.path.join("jsonl", experiment)):
            os.makedirs(os.path.join("jsonl", experiment))
        df.to_json(os.path.join("jsonl", experiment, split[:-3] + "jsonl"), orient="records", lines=True)
