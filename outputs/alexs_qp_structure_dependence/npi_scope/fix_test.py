import os

for data_set in os.listdir():
    if os.path.isdir(data_set):
        lines = []
        counter = 0
        for line in open(os.path.join(data_set, "CoLA/test_full.tsv")):
            vals = line.split("\t")
            vals = [str(counter), vals[3]]
            lines.append("\t".join(vals))
            counter += 1
        writer = open(os.path.join(data_set, "CoLA/test.tsv"), "w")
        for line in lines:
            writer.write(line)
        writer.close()