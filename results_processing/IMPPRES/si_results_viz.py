import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/SI_results.csv")

def weighted_avg(group):
    d = group["accuracy"]
    w = group["Num Examples"]
    return (d * w).sum() / w.sum()

d = data[((data["Control"] == "Opposite") | (data["Control"] == "Negation")) & (data["Logical"])][["accuracy", "Model", "Control", "Num Examples"]]
table = pd.pivot_table(d, values="accuracy", index="Control", columns="Model", aggfunc=weighted_avg)
# sns.heatmap(table, annot=True, cmap="Blues", cbar=False)

plt.show()



pass