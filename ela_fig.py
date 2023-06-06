import os
import joypy
import random
import pandas as pd
import matplotlib.pyplot as plt


def string_to_list(string):
    string = string[1:-1]
    content = string.split(", ")
    return [float(c) for c in content]


X = [5.0 * n for n in range(1, 21)]

os.chdir("/data/s3202844/data")
df = pd.read_csv("experiment_10_subtract_distr.csv")
df_test = pd.read_csv("experiment_10_subtract_kstest.csv")
if not os.path.exists("/home/s3202844/results/experiment_10_subtract/"):
    os.mkdir("/home/s3202844/results/experiment_10_subtract/")
os.chdir("/home/s3202844/results/")
columns = df.columns.values.tolist()
feature_list = columns[8:]


fig = plt.figure(figsize=(14, 16))
color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
for i in range(len(feature_list)):
    print(feature_list[i])
    ax = fig.add_subplot(8, 7, i + 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.text(0.5, 0.5, 'ELA_'+str(i+1), fontsize=20, ha='center')
plt.tight_layout()
plt.savefig("ela_fig.png")
plt.savefig("ela_fig.eps", dpi=600, format='eps')
plt.cla()
plt.close()
