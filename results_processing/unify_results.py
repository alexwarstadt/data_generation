import pandas as pd
import re

roberta_base_results = pd.read_json("../results/roberta_base_results/all_metrics.jsonl", orient="records", lines=True)
miniberta_results = pd.read_json("../results/miniberta_results/all_metrics.jsonl", orient="records", lines=True)

roberta_base_results["model_id"] = "1"
roberta_base_results["model_size"] = "30B"
roberta_base_results["training"] = roberta_base_results["training"].apply(lambda x: re.sub(r"_\de-\d_\d*_run", "", x))

all_results = pd.concat([miniberta_results, roberta_base_results])

all_results.to_json("../results/all_metrics.jsonl", orient="records", lines=True)