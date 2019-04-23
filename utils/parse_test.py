from sklearn.metrics import matthews_corrcoef

probing_types = [("npi", "npi_present"), ("licensor", "licensor")]

data_types = ["adverbs", "conditionals", "determiner_negation_biclausal", "only", "quantifiers", "questions", "sentential_negation_biclausal", "simplequestions", "superlative"]

probing_data_folder = "data/npi_probing/"
results_folder = "../Spring19/npi_metadata_probing_0422/"
runs = ['cola']

for d in data_types:
    for t in probing_types:
        infile1 = open(probing_data_folder+d+"/"+t[1]+"/test_full.tsv", "r")
        infile1_read = infile1.readlines()[1:]
        test_ans = [x.split('\t')[1] for x in infile1_read if len(x) != 0]
 
        for r in runs: 
            with open(results_folder+r+"/npi_"+d+"_"+t[0]+"_test.tsv") as infile2:
                infile2_read = infile2.readlines()
                test_preds = [x.split('\t')[1] for x in infile2_read[1:] if len(x) != 0]
                print(d, t, r)
                print(matthews_corrcoef(test_ans, test_preds))




