import os
import math
import joypy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ks_2samp


def string_to_list(string):
    string = string[1:-1]
    content = string.split(", ")
    return [float(c) for c in content]


os.chdir("/data/s3202844/data")
df = pd.read_csv("experiment_rotation_distr.csv")
if not os.path.exists("/home/s3202844/results/experiment_rotation/"):
    os.mkdir("/home/s3202844/results/experiment_rotation/")
os.chdir("/home/s3202844/results/experiment_rotation/")
dataset_list = df.values.tolist()
columns = df.columns.values.tolist()
feature_list = columns[8:]

plt.figure(figsize=(12, 12))
for problem_id in range(1, 6):
    boxes = []
    for i in range(len(feature_list)):
        p_string = df[(df["problem_id"] == float(problem_id)) &
                        (df["is_rotate"] == 0.0)][feature_list[i]].tolist()[0]
        p = string_to_list(p_string)
        p_mean = np.mean(p)
        diff = []
        for rotate_lim in range(30):
            # parse distribution
            q_string = df[(df["problem_id"] == float(problem_id)) &
                          (df["rotate_lim"] == float(rotate_lim)) &
                          (df["is_rotate"] == 1.0)][feature_list[i]].tolist()[0]
            q = string_to_list(q_string)
            q_mean = np.mean(q)
            diff_ = min(abs((p_mean-q_mean)/p_mean), 10.)
            diff += [diff_]
        boxes += [diff]
    plt.subplot(5, 1, problem_id)
    if problem_id == 5:
        plt.boxplot(boxes, labels=feature_list)
        plt.xticks(rotation=90)
    else:
        plt.boxplot(boxes, labels=["" for _ in range(len(feature_list))])
    plt.title("problem_id: {}".format(problem_id))
    plt.ylabel("%")
plt.tight_layout()
plt.savefig("mean.png".format(problem_id))
