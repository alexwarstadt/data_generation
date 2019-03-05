# initialize output file
output = open("../outputs/plurals/environment=collectivepredicates.tsv", "w")

# set total number of paradigms to generate
number_to_generate = 1000
sentences = set()

# gather word classes that will be accessed frequently
all_irregular_nouns = get_all_conjunctive([("category", "N"), ("irrpl", "1")])
all_irregular_nouns_sg = get_all(["sg", "1"])
all_quantifiers = get_all("category", "(S/(S\\NP))/N")
all_UE_quantifiers = get_all("restrictor_DE", "0", all_quantifiers)
all_transitive_verbs = get_all("category", "(S\\NP)/NP")
all_non_singular_nouns = np.append(get_all("pl", "1"), get_all("mass", "1"))