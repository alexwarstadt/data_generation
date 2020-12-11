import json
import re

lines = []
for line in open("/Users/alexwarstadt/Workspace/data_generation/outputs/structure/subject_aux_inversion/test.jsonl"):
    lines.append(json.loads(line))

def remove_RCs(string):
    vals = string.split(",")
    vals = list(filter(lambda x: re.match(r"RC\d=\d", x) is None, vals))
    return ",".join(vals)

templates = {}
for line in lines:
    t = remove_RCs(line["template"])
    line["template"] = t
    if t not in templates.keys():
        templates[t] = []
    templates[t].append(line)

output = open("/Users/alexwarstadt/Workspace/data_generation/outputs/structure/subject_aux_inversion/validation.tsv", "w")
output.write("\t".join(["template", "base", "transform", "structural", "linear"]) + "\n")
for t in templates.keys():
    for i in range(3):
        example = templates[t][i]
        output.write("\t".join([example["template"], example["sentence_base"], example["sentence_transform"], str(example["linguistic_feature_label"]), str(example["surface_feature_label"])]) + "\n")
