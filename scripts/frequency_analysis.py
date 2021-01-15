from collections import Counter
import csv
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
import random

celex_path = "efw/efw.cd"
counts = {}
with open(celex_path) as f:
    for line in f:
        vals = line.split("\\")
        counts[vals[1]] = int(vals[3])

counts = Counter(counts)
sorted_words = dict([(w[0], i) for i, w in enumerate(counts.most_common())])

vocab_path = "../vocabulary.csv"
words = []
with open(vocab_path) as f:
    next(f)
    for line in f:
        vals = line.split(",")
        w = vals[0]
        words.extend(w.split())


words = list(set(words))
word_ranks = [sorted_words[w] for w in words if w in sorted_words]



def plot_freq_rank_density():
    ax = plt.gca()
    density = gaussian_kde(word_ranks)
    xs = np.linspace(0, 100000, 1000)
    ax.plot(xs, density(xs))
    # ax.set_xscale("log")
    # ax.axvline(color="k", linestyle=":")
    ax.set_xlabel("Frequency Rank")
    ax.set_ylabel("Density")
    ax.set_title("Distribution of word frequency ranks in vocabulary")
    ax.set_xlim(-1000, 100000)
    # ax.set_ylim(-0.1, 5)
    # ax.legend()
    plt.show()


def plot_freq_rank_histogram():
    ax = plt.gca()
    ax.hist(word_ranks, bins=224)
    ax.set_ylabel("Number of vocabulary entries")
    ax.set_xlabel("Frequency rank")
    ax.set_title("Distribution of word frequency ranks in vocabulary\nBin width=400")
    plt.show()


def study_high_freq_words():
    top_1000 = counts.most_common()[:1000]
    top_1000_in = [w[0] for w in top_1000 if w[0] in words]
    top_1000_out = [w[0] for w in top_1000 if w[0] not in words]
    # print(top_1000_in)
    # print("\n" * 10)
    # print(top_1000_out)
    print(np.random.choice(top_1000_in, 50, replace=False))
    print(np.random.choice(top_1000_out, 50, replace=False))


study_high_freq_words()

pass
