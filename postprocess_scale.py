import os
import math
import pandas as pd
import matplotlib.pyplot as plt


def string_to_list(string):
    string = string[1:-1]
    content = string.split(", ")
    return [float(c) for c in content]


factors = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5,
           1., 2., 4., 8., 16., 32., 64., 128.]
os.chdir("/data/s3202844/data")
df = pd.read_csv("experiment_scale_kstest.csv")
os.chdir("/home/s3202844/results")
dataset_list = df.values.tolist()
columns = df.columns.values.tolist()
feature_list = columns[8:]
x = [math.log(f, 2) for f in factors]
for problem_id in range(1, 6):
    plt.figure(figsize=(15, 20))
    for i in range(len(feature_list)):
        pvalue = []
        for f in factors:
            ks_string = df[(df["problem_id"] == float(problem_id)) & 
                (df["scale_factor"] == float(f))][feature_list[i]].tolist()[0]
            ks_list = string_to_list(ks_string)
            pvalue += [ks_list[1]]
        plt.subplot(9, 6, i+1)
        plt.ylim(-0.1, 1.1)
        plt.plot(x, pvalue)
        plt.xlabel("$\log_2{scale\_factor}$")
        plt.axhline(0.05, color="red", linestyle=":")
        plt.title(feature_list[i])
    plt.tight_layout()
    plt.savefig("pvalue_scale_" + str(problem_id) + ".png")
    plt.cla()
