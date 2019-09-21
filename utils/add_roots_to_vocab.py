from utils.vocab_table import *
from nltk.stem import WordNetLemmatizer
from utils.constituent_building import get_bare_form_str

lemmatizer = WordNetLemmatizer()

for entry in vocab:
    if entry["verb"] != "1":
        continue

    lemma = get_bare_form_str(entry["expression"])
    category = entry["category"]
    entry["root"] = lemma + "_" + category


vocab_file = open("../vocabulary2.csv", "w")

for entry in vocab:
    vocab_file.write(",".join(entry) + "\n")

vocab_file.close()

pass

