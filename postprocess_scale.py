import os
import math
import joypy
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ks_2samp


def string_to_list(string):
    string = string[1:-1]
    content = string.split(", ")
    return [float(c) for c in content]


factors = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5,
           1., 2., 4., 8., 16., 32., 64., 128.]
x = [math.log(f, 2) for f in factors]

os.chdir("/data/s3202844/data")
df = pd.read_csv("experiment_scale_distr.csv")
if not os.path.exists("/home/s3202844/results/experiment_scale/"):
    os.mkdir("/home/s3202844/results/experiment_scale/")
os.chdir("/home/s3202844/results/experiment_scale/")
dataset_list = df.values.tolist()
columns = df.columns.values.tolist()
feature_list = columns[8:]

for problem_id in range(1, 6):
    if not os.path.exists("{}/".format(problem_id)):
        os.mkdir("{}/".format(problem_id))
    for i in range(len(feature_list)):
        if not os.path.exists("{}/{}/".format(problem_id, feature_list[i])):
            os.mkdir("{}/{}/".format(problem_id, feature_list[i]))
        # 2 lists for 2 plots
        PQf = []
        pvalue = []
        for f in factors:
            # parse distribution
            p_string = df[(df["problem_id"] == float(problem_id)) &
                          (df["is_scale"] == 0.0)][feature_list[i]].tolist()[0]
            q_string = df[(df["problem_id"] == float(problem_id)) &
                          (df["scale_factor"] == float(f)) &
                          (df["is_scale"] == 1.0)][feature_list[i]].tolist()[0]
            p = string_to_list(p_string)
            q = string_to_list(q_string)
            for j in range(len(p)):
                PQf += [[p[j], q[j], f]]
            # parse pvalue
            _, pvalue_ = ks_2samp(p, q)
            pvalue += [pvalue_]
        # pvalue plot
        plt.figure(figsize=(5, 5))
        plt.ylim(-0.1, 1.1)
        plt.plot(x, pvalue)
        plt.axhline(0.05, color="red", linestyle=":")
        plt.xlabel("$\log_2{scale\_factor}$")
        plt.ylabel("$pvalue$")
        plt.title("KS-test result of {}.".format(feature_list[i]))
        plt.tight_layout()
        plt.savefig("{}/{}/{}_pvalue.png".format(problem_id, feature_list[i],
                                                 feature_list[i]))
        plt.clf()
        # distribution plot
        PQf_df = pd.DataFrame(PQf, columns=["p", "q", "factor"])
        try:
            joypy.joyplot(PQf_df, by="factor", figsize=(6, 10),
                          title="Distribution of ${}$ over scale factors.".format(
                feature_list[i]), color=["#1f77b4a0", "#ff7f0ea0"])
            rect1 = plt.Rectangle((0, 0), 0, 0, color='#1f77b4d0',
                                  label="basic distribution")
            rect2 = plt.Rectangle((0, 0), 0, 0, color='#ff7f0ed0',
                                  label="new distribution")
            plt.gca().add_patch(rect1)
            plt.gca().add_patch(rect2)
            plt.xlabel("feature value")
            plt.tight_layout()
            plt.legend(loc=3)
            plt.savefig("{}/{}/{}_distr.png".format(problem_id,
                                                    feature_list[i],
                                                    feature_list[i]))
            plt.clf()
        except ValueError:
            plt.clf()
            print("{} only have None value!".format(feature_list[i]))
        plt.close()
