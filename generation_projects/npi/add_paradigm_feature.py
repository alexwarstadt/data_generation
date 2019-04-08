import os

def add_paradigm_feature(dataset_path, output_path=None, paradigm_size=8):
    data = [line for line in open(dataset_path)]
    if output_path is None:
        output_path = dataset_path
    out = open(output_path, "w")
    for i, line in enumerate(data):
        vals = line.split("\t")
        vals[0] = vals[0] + "-paradigm=" + str(i // paradigm_size)
        out.write("\t".join(vals))
    out.close()


project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
npi_dir = "outputs/npi/"
for file in os.listdir(os.path.join(project_root, npi_dir)):
    if ".tsv" in file:
        dataset_path = os.path.join(project_root, npi_dir, file)
        output_path = os.path.join(project_root, npi_dir, file + "_copy")
        add_paradigm_feature(dataset_path, output_path)
