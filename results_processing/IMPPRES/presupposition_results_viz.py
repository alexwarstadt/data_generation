import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/presupposition.csv")
data.head()

# # Plot unembedded positive
# y_labels = ["All N",
#             "Both",
#             "Change of state",
#             "Cleft existence",
#             "Cleft uniqueness",
#             "Only",
#             "Possess. existence",
#             "Possess. uniqueness",
#             "Question"
#             ]
# d = data[(~data["filtered"]) & (data["condition"] == "test_unembedded_positive")][["accuracy", "model", "trigger_type"]]
# d = d.pivot_table(columns="model", index="trigger_type", values="accuracy")
# ax = sns.heatmap(d, annot=True, cmap="Blues", cbar=False, vmin=0, vmax=1, yticklabels=y_labels)
# ax.set_title("Presupposition Trigger Results\n(Accuracy)")
# ax.set_ylabel("Trigger")
# ax.set_xlabel("Model")
# plt.show()

# # Plot controls
# d = data[(~data["filtered"]) & (data["control"])][["accuracy", "model", "trigger_type", "trigger_condition"]]
# table = pd.pivot_table(d, values="accuracy", index="trigger_condition", columns="model", aggfunc=np.mean)
# table = table.rename_axis(index={"trigger_condition":"Operator"})
# # table.rename({})
# ax = plt.axes()
# sns.heatmap(table, annot=True, ax=ax, cmap="Blues", cbar=False, vmin=0, vmax=1)
# plt.yticks(rotation=0)
# ax.set_title('Presupposition Controls (Accuracy)')
# plt.show()


# # PLOT FILTERED WEIGHTED RESULTS
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/presupposition_results_filtered.csv")
# y_labels_1 = ["conditional",
#             "conditional",
#             "conditional",
#             "interrogative",
#             "interrogative",
#             "interrogative",
#             "modal",
#             "modal",
#             "modal",
#             "negated",
#             "negated",
#             "negated"]
# y_labels_2 = ["negated",
#             "neutral",
#             "positive",
#             "negated",
#             "neutral",
#             "positive",
#             "negated",
#             "neutral",
#             "positive",
#             "negated",
#             "neutral",
#             "positive"]
# ax = sns.heatmap(data.pivot(index="Condition", columns="model", values="Accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Trigger Condition")
# ax2 = ax.twinx()
# sns.heatmap(data.pivot(index="Condition", columns="model", values="Accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1, ax=ax2)
# ax2.set_yticklabels(y_labels_2)
# ax2.hlines([3, 6, 9, 12], *ax.get_xlim())
# ax2.set_ylabel("Presupposition Condition")
# ax2.set_title('Projection Results (Accuracy)')
# plt.show()




# # PLOT SI RESULTS
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/agg_allSI(test).csv")
# y_labels_1 = ["connectives",
#             "connectives",
#             "determiners",
#             "determiners",
#             "gradable adjectives",
#             "gradable adjectives",
#             "gradable verbs",
#             "gradable verbs",
#             "modals",
#             "modals",
#             "numerals",
#             "numerals"]
# y_labels_2 = ["logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic"]
# ax = sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Dataset")
# # ax.set_title('Projection Conditions')
# ax2 = ax.twinx()
# sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2, vmin=0, vmax=1)
# # ax2.set_yticklabels(y_labels_2)
# ax2.set_ylabel("Logical/Pragmatic")
# ax2.hlines([2,4,6,8,10], *ax.get_xlim())
# ax2.set_title("Implicatures Results (Accuracy)")
# ax.set_xlabel("Model")
# plt.show()



# PLOT SI RESULTS DETERMINER
data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/redatasets/breakdown_determiners.csv")
x_labels_1 = ["all/some",
              "all/some",
              "none/not all",
              "none/not all",
              "not all/none",
              "not all/none",
              "not all/some",
              "not all/some",
              "some/all",
              "some/all",
              "some/not all",
              "some/not all"]
x_labels_2 = ["logical", "pragmatic",
              "logical", "pragmatic",
              "logical", "pragmatic",
              "logical", "pragmatic",
              "logical", "pragmatic",
              "logical", "pragmatic"]
data = data[data["model"] == "BERT"]
data = data.pivot_table(columns=["condition", "log-prag"], index="model", values="accuracy")
ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, xticklabels=x_labels_2, vmin=0, vmax=1)
ax.set_xlabel("Logical/Pragmatic")
# ax.set_title('Determiner Implicature Results (Accuracy)')
ax2 = ax.twiny()
plt.title('Determiner Implicature Results (Accuracy)', y=3)
sns.heatmap(data, annot=True, cmap="Blues", cbar=False, xticklabels=x_labels_1, vmin=0, vmax=1, ax=ax2)
# sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2)
# ax2.set_yticklabels(y_labels_2)
ax2.set_xlabel("Condition")
ax2.set_yticklabels(ax2.get_yticklabels(), rotation=90)
ax2.vlines([2,4,6,8,10,12], *ax.get_xlim())
# ax2.set_title("Implicatures Results (Accuracy)")
plt.show()

# # PLOT SI RESULTS CONNECTIVES
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/redatasets/breakdown_connectives.csv")
# y_labels_1 = ["A and B/A or B",
#               "A and B/A or B",
#               "A or B/A and B",
#               "A or B/A and B",
#               "A or B/not both A and B",
#               "A or B/not both A and B",
#               "neither A nor B/not both A and B",
#               "neither A nor B/not both A and B",
#               "not both A and B/A or B",
#               "not both A and B/A or B",
#               "not both A and B/neither A nor B",
#               "not both A and B/neither A nor B",
#               ]
# y_labels_2 = ["logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic"]
# data = data.pivot_table(index=["condition", "log-prag"], columns="model", values="accuracy")
# ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Condition")
# # ax.set_title('Determiner Implicature Results (Accuracy)')
# ax2 = ax.twinx()
# plt.title('Connectives Implicature Results (Accuracy)')
# sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, vmin=0, vmax=1, ax=ax2)
# # sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2)
# # ax2.set_yticklabels(y_labels_2)
# ax2.set_ylabel("Logical/Pragmatic")
# # ax2.set_yticklabels(ax2.get_yticklabels(), rotation=90)
# ax2.hlines([2,4,6,8,10,12], *ax.get_xlim())
# # ax2.set_title("Implicatures Results (Accuracy)")
# plt.show()

# #PLOT SI RESULTS MODALS
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/redatasets/breakdown-modals.csv")
# y_labels_1 = ["can/have to",
#               "can/have to",
#               "can/not have to",
#               "can/not have to",
#               "cannot/not have to",
#               "cannot/not have to",
#               "have to/can",
#               "have to/can",
#               "not have to/can",
#               "not have to/can",
#               "not have to/cannot",
#               "not have to/cannot",
#               ]
# y_labels_2 = ["logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic"]
# data = data.pivot_table(index=["condition", "log-prag"], columns="model", values="accuracy")
# ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Condition")
# # ax.set_title('Determiner Implicature Results (Accuracy)')
# ax2 = ax.twinx()
# plt.title('Modals Implicature Results (Accuracy)')
# sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, vmin=0, vmax=1, ax=ax2)
# # sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2)
# # ax2.set_yticklabels(y_labels_2)
# ax2.set_ylabel("Logical/Pragmatic")
# # ax2.set_yticklabels(ax2.get_yticklabels(), rotation=90)
# ax2.hlines([2,4,6,8,10,12], *ax.get_xlim())
# # ax2.set_title("Implicatures Results (Accuracy)")
# plt.show()

# # #PLOT SI RESULTS ADJECTIVES
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/redatasets/breakdown_adjectives.csv")
# y_labels_1 = ["excellent/good",
#               "excellent/good",
#               "good/excellent",
#               "good/excellent",
#               "good/not excellent",
#               "good/not excellent",
#               "not excellent/good",
#               "not excellent/good",
#               "not excellent/not good",
#               "not excellent/not good",
#               "not good/not excellent",
#               "not good/not excellent",
#               ]
# y_labels_2 = ["logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic"]
# data = data.pivot_table(index=["condition", "log-prag"], columns="model", values="accuracy")
# ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Condition")
# # ax.set_title('Determiner Implicature Results (Accuracy)')
# ax2 = ax.twinx()
# plt.title('Adjectives Implicature Results (Accuracy)')
# sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, vmin=0, vmax=1, ax=ax2)
# # sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2)
# # ax2.set_yticklabels(y_labels_2)
# ax2.set_ylabel("Logical/Pragmatic")
# # ax2.set_yticklabels(ax2.get_yticklabels(), rotation=90)
# ax2.hlines([2,4,6,8,10,12], *ax.get_xlim())
# # ax2.set_title("Implicatures Results (Accuracy)")
# plt.show()

# # # #PLOT SI RESULTS VERBS
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/redatasets/breakdown_verbs.csv")
# y_labels_1 = ["not run/not sprint",
#               "not run/not sprint",
#               "not sprint/not run",
#               "not sprint/not run",
#               "not sprint/run",
#               "not sprint/run",
#               "run/not sprint",
#               "run/not sprint",
#               "run/sprint",
#               "sprint/run",
#               "sprint/run",
#               ]
# y_labels_2 = ["logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic"]
# data = data.pivot_table(index=["condition", "log-prag"], columns="model", values="accuracy")
# ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Condition")
# # ax.set_title('Determiner Implicature Results (Accuracy)')
# ax2 = ax.twinx()
# plt.title('Verbs Implicature Results (Accuracy)')
# sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, vmin=0, vmax=1, ax=ax2)
# # sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2)
# # ax2.set_yticklabels(y_labels_2)
# ax2.set_ylabel("Logical/Pragmatic")
# # ax2.set_yticklabels(ax2.get_yticklabels(), rotation=90)
# ax2.hlines([2,4,6,8,10,12], *ax.get_xlim())
# # ax2.set_title("Implicatures Results (Accuracy)")
# plt.show()

# # # #PLOT SI RESULTS NUMERALS
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/redatasets/breakdown_numerals.csv")
# y_labels_1 = ["10/100",
#               "10/100",
#               "10/not 100",
#               "10/not 100",
#               "100/10",
#               "100/10",
#               "not 10/not 100",
#               "not 10/not 100",
#               "not 100/10",
#               "not 100/10",
#               "not 100/not 10",
#               "not 100/not 10",
#               ]
# y_labels_2 = ["logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic"]
# data = data.pivot_table(index=["condition", "log-prag"], columns="model", values="accuracy")
# ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Condition")
# # ax.set_title('Determiner Implicature Results (Accuracy)')
# ax2 = ax.twinx()
# plt.title('Numerals Implicature Results (Accuracy)')
# sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, vmin=0, vmax=1, ax=ax2)
# # sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2)
# # ax2.set_yticklabels(y_labels_2)
# ax2.set_ylabel("Logical/Pragmatic")
# # ax2.set_yticklabels(ax2.get_yticklabels(), rotation=90)
# ax2.hlines([2,4,6,8,10,12], *ax.get_xlim())
# # ax2.set_title("Implicatures Results (Accuracy)")
# plt.show()

# # # #PLOT SI RESULTS DETERMINERS FULL
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/redatasets/breakdown_determiners.csv")
# y_labels_1 = ["all/some",
#               "all/some",
#               "none/not all",
#               "none/not all",
#               "not all/none",
#               "not all/none",
#               "not all/some",
#               "not all/some",
#               "some/all",
#               "some/all",
#               "some/not all",
#               "some/not all",
#               ]
# y_labels_2 = ["logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic",
#               "logical", "pragmatic"]
# data = data.pivot_table(index=["condition", "log-prag"], columns="model", values="accuracy")
# ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_1, vmin=0, vmax=1)
# ax.set_ylabel("Condition")
# # ax.set_title('Determiner Implicature Results (Accuracy)')
# ax2 = ax.twinx()
# plt.title('Determiners Implicature Results (Accuracy)')
# sns.heatmap(data, annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, vmin=0, vmax=1, ax=ax2)
# # sns.heatmap(data.pivot_table(index=["dataset", "log-prag"], columns="model", values="accuracy"), annot=True, cmap="Blues", cbar=False, yticklabels=y_labels_2, ax=ax2)
# # ax2.set_yticklabels(y_labels_2)
# ax2.set_ylabel("Logical/Pragmatic")
# # ax2.set_yticklabels(ax2.get_yticklabels(), rotation=90)
# ax2.hlines([2,4,6,8,10,12], *ax.get_xlim())
# # ax2.set_title("Implicatures Results (Accuracy)")
# plt.show()


# # PLOT SI CONTROLS
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/aggSI_controls.csv")
# y_labels_1 = ["Connectives",
#             "Connectives",
#             "Determiners",
#             "Determiners",
#             "Gradable adjectives",
#             "Gradable adjectives",
#             "Gradable verbs",
#             "Gradable verbs",
#             "Modals",
#             "Modals",
#             "Numerals",
#             "Numerals"]
# y_labels_2 = [
#     "Negation", "Opposite",
#     "Negation", "Opposite",
#     "Negation", "Opposite",
#     "Negation", "Opposite",
#     "Negation", "Opposite",
#     "Negation", "Opposite"]
# data = data.pivot_table(index=["dataset", "control type"], columns="model", values="accuracy")
# ax = sns.heatmap(data, annot=True, cmap="Blues", cbar=False, vmin=0, vmax=1, yticklabels=y_labels_1)
# ax.set_ylabel("Implicature Trigger")
# ax2 = ax.twinx()
# sns.heatmap(data, annot=True, cmap="Blues", cbar=False, vmin=0, vmax=1, yticklabels=y_labels_2, ax=ax2)
# ax2.set_ylabel("Control Type")
# ax2.set_xlabel("Model")
# ax2.hlines([2,4,6,8,10], *ax.get_xlim())
# ax2.set_title("Implicatures Controls (Accuracy)")
#
# plt.show()




#USELESS THINGS??

bert_good = ["cleft_existence", "only_presupposition", "possessed_definites_existence", "question_presupposition"]
# # Plot test results only for triggers where BERT succeeds.
# d = data[(~data["filtered"]) & (~data["control"]) & (data["trigger_type"].isin(bert_good))][["accuracy", "model", "trigger_type", "trigger_condition", "presupposition_condition"]]
# d = pd.pivot_table(d, values="accuracy", index=["presupposition_condition", "trigger_condition"], columns="model", aggfunc=np.mean)
# sns.heatmap(d, annot=True)
# plt.show()

# # Plot test results only for broken down by trigger, only for triggers where BERT succeeds.
# fig = plt.figure()
# axes = [fig.add_subplot(2, 2, i+1) for i in range(len(bert_good))]
# for i, t in enumerate(bert_good):
#     d = data[(~data["filtered"]) & (~data["control"]) & (data["trigger_type"] == t)][["accuracy", "model", "trigger_type", "trigger_condition", "presupposition_condition"]]
#     d = pd.pivot_table(d, values="accuracy", index=["presupposition_condition", "trigger_condition"], columns="model", aggfunc=np.mean)
#     sns.heatmap(d, ax=axes[i], annot=True)
# plt.show()

# # Plot test results by presupposition condition only for triggers where BERT succeeds.
# fig = plt.figure()
# axes = [fig.add_subplot(2, 2, i+1) for i in range(len(bert_good))]
# for x,t in zip(axes, bert_good):
#     x.title.set_text(t)
# for i, t in enumerate(bert_good):
#     d = data[(~data["filtered"]) & (~data["control"]) & (data["trigger_type"]==t)][
#         ["accuracy", "model", "trigger_type", "trigger_condition", "presupposition_condition"]]
#     d = pd.pivot_table(d, values="accuracy", index=["presupposition_condition"], columns="model", aggfunc=np.mean)
#     sns.heatmap(d, ax=axes[i], annot=True)
# plt.show()

# Plot test results by presupposition condition broken down by trigger.
# trigger_types = set(data["trigger_type"])
# fig = plt.figure()
# axes = [fig.add_subplot(3, 3, i+1) for i in range(len(trigger_types))]
# for x, t in zip(axes, trigger_types):
#     x.title.set_text(t)
# for i, t in enumerate(trigger_types):
#     d = data[(~data["filtered"]) & (~data["control"]) & (data["trigger_type"]==t)][
#         ["accuracy", "model", "trigger_type", "trigger_condition", "presupposition_condition"]]
#     d = pd.pivot_table(d, values="accuracy", index=["presupposition_condition"], columns="model", aggfunc=np.mean)
#     sns.heatmap(d, ax=axes[i], annot=True)
# plt.show()

# # Plot test results by trigger condition only for triggers where BERT succeeds.
# fig = plt.figure()
# axes = [fig.add_subplot(2, 2, i+1) for i in range(len(bert_good))]
# for x,t in zip(axes, bert_good):
#     x.title.set_text(t)
# for i, t in enumerate(bert_good):
#     d = data[(data["filtered"]) & (~data["control"]) & (data["trigger_type"]==t)][
#         ["accuracy", "model", "trigger_type", "trigger_condition", "presupposition_condition"]]
#     d = pd.pivot_table(d, values=["accuracy"], index=["trigger_condition"], columns="model", aggfunc=np.mean)
#     sns.heatmap(d, ax=axes[i], annot=True)
# plt.show()








# SCALAR IMPLICATURE
# data = pd.read_csv("/Users/alexwarstadt/Workspace/data_generation/results/IMPPRES/SI_results.csv")
#
# def weighted_avg(group):
#     d = group["accuracy"]
#     w = group["Num Examples"]
#     return (d * w).sum() / w.sum()
#
# d = data[((data["Control"] == "Opposite") | (data["Control"] == "Negation")) & (data["Logical"])][["accuracy", "Model", "Control", "Num Examples"]]
# table = pd.pivot_table(d, values="accuracy", index="Control", columns="Model", aggfunc=weighted_avg)
# # sns.heatmap(table, annot=True, cmap="Blues", cbar=False)
#
# plt.show()