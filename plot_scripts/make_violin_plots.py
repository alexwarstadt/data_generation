import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

results = pd.read_json("../results/all_metrics.jsonl", orient="records", lines=True)

for experiment in ["subject_aux_inversion", "main_verb"]:
# for experiment in ["main_verb"]:
    data = results[results["experiment"]==experiment]
    data["training_str"] = data["training"].apply(lambda x: "\n".join(x.split("-")))
    data["OOD"] = (data["ambiguous"] & data["reverse"]) | ((~data["ambiguous"]) & ~(data["reverse"]))
    templates = set(data["template"])
    templates.remove("overall")
    templates = list(templates)
    data["training_code"] = data["training"].apply(lambda x: ",".join([str(templates.index(t)) for t in x.split("-")]))
    data = data[data["OOD"]]
    g = sns.catplot(data=data,
                    col="training_code", hue="reverse", x="model_size", y="mcc",
                    col_wrap=10,
                    kind="violin", cut=0, scale="width",
                    order=["1M", "10M", "100M", "1B", "30B"]
                    )
    g.set(ylim=(-1, 1))
    g.tight_layout()
    plt.savefig(f"../figures/violins/{experiment}.png")
    plt.savefig(f"../figures/violins/{experiment}.pdf")

    plt.close()
    data_overall = data[data["template"] == "overall"]
    g = sns.catplot(data=data,
                    hue="reverse", x="model_size", y="mcc",
                    kind="violin", cut=0, scale="width",
                    order=["1M", "10M", "100M", "1B", "30B"]
                    )
    g.set(ylim=(-1, 1))
    g.tight_layout()
    plt.savefig(f"../figures/violins/{experiment}_agg.png")
    plt.savefig(f"../figures/violins/{experiment}_agg.pdf")

