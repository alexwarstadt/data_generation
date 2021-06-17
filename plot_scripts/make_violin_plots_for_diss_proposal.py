import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

results = pd.read_json("../results/all_metrics.jsonl", orient="records", lines=True)

# for experiment in ["subject_aux_inversion", "main_verb"]:
# for experiment in ["main_verb"]:
#     data = results[results["experiment"]==experiment]
data = results
data["training_str"] = data["training"].apply(lambda x: "\n".join(x.split("-")))
data["OOD"] = (data["ambiguous"] & data["reverse"]) | ((~data["ambiguous"]) & ~(data["reverse"]))
templates = set(data["template"])
templates.remove("overall")
templates = list(templates)
data["training_code"] = data["training"].apply(lambda x: ",".join([str(templates.index(t)) for t in x.split("-")]))
data = data[data["OOD"] & (~data["reverse"])]
data["training data"] = data["model_size"].apply(lambda x: "News, books, and web" if x=="30B" else "OpenSubtitles")
data_overall = data[data["template"] == "overall"]
g = sns.catplot(data=data_overall,
                hue="training data",
                col="experiment",
                x="model_size", y="mcc",
                kind="violin", cut=0, scale="width",
                order=["1M", "10M", "100M", "1B", "30B"]
                # order=["1M", "10M", "100M", "1B"]
                )
g.set(ylim=(-1, 1))
g.tight_layout()
plt.savefig(f"../figures/violins_for_diss_proposal/agg.png")
plt.savefig(f"../figures/violins_for_diss_proposal/agg.pdf")

