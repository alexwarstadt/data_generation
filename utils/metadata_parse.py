import numpy as np

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
    data_type = [(k, "U100") for k in keys] + [("judgment", "U1"), ("sentence", "U10000")]
    data_table = []
    for line in data_file:
        columns = line.split("\t")
        metadata = columns[0].split("-")
        values = [kv.split("=")[1] for kv in metadata]
        array_entry = np.array(values + [columns[1], columns[3]])
        data_table.append(tuple(array_entry))
    data_table = np.array(data_table, data_type)
    return data_table



data = read_data_tsv("../outputs/npi/environment=quantifiers.tsv")

pass