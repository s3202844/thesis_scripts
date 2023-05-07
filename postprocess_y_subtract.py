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


X = [100 * i for i in range(11)]

os.chdir("/data/s3202844/data")
df = pd.read_csv("experiment_y_subtract_distr.csv")
df_test = pd.read_csv("experiment_y_subtract_kstest.csv")
if not os.path.exists("/home/s3202844/results/experiment_y_subtract/"):
    os.mkdir("/home/s3202844/results/experiment_y_subtract/")
os.chdir("/home/s3202844/results/experiment_y_subtract/")
columns = df.columns.values.tolist()
feature_list = columns[8:]

# remove limo features from feature list
feature_list = [f for f in feature_list if f[:4] != "limo"]


fig = plt.figure(figsize=(14, 16))
color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
for i in range(len(feature_list)):
    ax = fig.add_subplot(8, 7, i + 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.axhline(0.05, color="red", linestyle=":")
    for problem_id in range(1, 6):
        # 2 lists for 2 plots
        pvalue = []
        wd = []
        for x in X:
            # parse pvalue
            test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
                                  (df_test["subtract_lim"] == float(x)) &
                                  (df_test["is_subtract"] == 1.0)][
                feature_list[i]].tolist()[0]
            test = string_to_list(test_string)
            pvalue += [test[1]]
            wd += [test[2]]
        t_ind = int(len(feature_list[i]) / 2)
        ax.plot(X, pvalue, color=color[problem_id - 1], linewidth=1,
                label="problem {}".format(problem_id))
ax = fig.add_subplot(8, 7, 56)
ax.set_yticks([])
ax.xaxis.set_label_coords(0.5, 0.1)
ax.yaxis.set_label_coords(0.1, 0.5)
ax.set_xlabel('tranbslation')
ax.set_ylabel(r'p'+'-value')
ax.plot(X[0], X[0])
ax.plot(X[-1], X[-1])
for problem_id in range(1, 6):
    ax.plot([0], [0], color=color[problem_id - 1], linewidth=1,
            label="problem {}".format(problem_id))
ax.legend(loc="upper right", borderaxespad=0, ncol=1)
plt.tight_layout()
plt.savefig("pvalue.png")
plt.savefig("pvalue.eps", dpi=600, format='eps')
plt.cla()
plt.close()


fig = plt.figure(figsize=(14, 16))
color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
for i in range(len(feature_list)):
    ax = fig.add_subplot(8, 7, i + 1)
    ax.set_yticks([])
    ax.set_xticks([])
    for problem_id in range(1, 6):
        # 2 lists for 2 plots
        pvalue = []
        wd = []
        for x in X:
            # parse pvalue
            test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
                                  (df_test["subtract_lim"] == float(x)) &
                                  (df_test["is_subtract"] == 1.0)][
                feature_list[i]].tolist()[0]
            test = string_to_list(test_string)
            pvalue += [test[1]]
            wd += [test[2]]
        t_ind = int(len(feature_list[i]) / 2)
        ax.plot(X, wd, color=color[problem_id - 1], linewidth=1,
                 label="problem {}".format(problem_id))
ax = fig.add_subplot(8, 7, 56)
ax.set_yticks([])
ax.xaxis.set_label_coords(0.5, 0.1)
ax.yaxis.set_label_coords(0.1, 0.5)
ax.set_xlabel('tranbslation')
ax.set_ylabel('EMD')
ax.plot(X[0], X[0])
ax.plot(X[-1], X[-1])
for problem_id in range(1, 6):
    ax.plot([0], [0], color=color[problem_id - 1], linewidth=1,
            label="problem {}".format(problem_id))
ax.legend(loc="upper right", borderaxespad=0, ncol=1)
plt.tight_layout()
plt.savefig("wd.png")
plt.savefig("wd.eps", dpi=600, format='eps')
plt.cla()
plt.close()


# for problem_id in range(1, 6):
#     if not os.path.exists("{}/".format(problem_id)):
#         os.mkdir("{}/".format(problem_id))
#     for i in range(len(feature_list)):
#         if not os.path.exists("{}/{}/".format(problem_id, feature_list[i])):
#             os.mkdir("{}/{}/".format(problem_id, feature_list[i]))
#         # 2 lists for 2 plots
#         PQf = []
#         pvalue = []
#         wd = []
#         for x in X:
#             # parse distribution
#             p_string = df[(df["problem_id"] == float(problem_id)) &
#                           (df["is_subtract"] == 0.0)][
#                 feature_list[i]].tolist()[0]
#             q_string = df[(df["problem_id"] == float(problem_id)) &
#                           (df["subtract_lim"] == float(x)) &
#                           (df["is_subtract"] == 1.0)][
#                 feature_list[i]].tolist()[0]
#             p = string_to_list(p_string)
#             q = string_to_list(q_string)
#             for j in range(len(p)):
#                 PQf += [[p[j], q[j], x]]
#             # parse pvalue
#             test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
#                                   (df_test["subtract_lim"] == float(x)) &
#                                   (df_test["is_subtract"] == 1.0)][
#                 feature_list[i]].tolist()[0]
#             test = string_to_list(test_string)
#             pvalue += [test[1]]
#             wd += [test[2]]
#         # pvalue plot
#         plt.figure(figsize=(5, 5))
#         plt.ylim(-0.1, 1.1)
#         plt.plot(X, pvalue)
#         plt.axhline(0.05, color="red", linestyle=":")
#         plt.xlabel("$subtract\_lim$")
#         plt.ylabel("$pvalue$")
#         plt.title("KS-test result of {}.".format(feature_list[i]))
#         plt.tight_layout()
#         plt.savefig("{}/{}/{}_pvalue.png".format(problem_id, feature_list[i],
#                                                  feature_list[i]))
#         plt.cla()
#         plt.close()
#         # wd plot
#         plt.figure(figsize=(5, 5))
#         plt.plot(X, wd)
#         plt.xlabel("$subtract\_lim$")
#         plt.ylabel("$wasserstein_distance$")
#         plt.title("Wasserstein Distance result of {}.".format(feature_list[i]))
#         plt.tight_layout()
#         plt.savefig("{}/{}/{}_wd.png".format(problem_id, feature_list[i],
#                                                  feature_list[i]))
#         plt.cla()
#         plt.close()
#         # distribution plot
#         PQf_df = pd.DataFrame(PQf, columns=["p", "q", "lim"])
#         try:
#             joypy.joyplot(PQf_df, by="lim", figsize=(6, 10),
#                           title="Distribution of ${}$ over subtract limitation.".format(
#                 feature_list[i]), color=["#1f77b4a0", "#ff7f0ea0"])
#             rect1 = plt.Rectangle((0, 0), 0, 0, color='#1f77b4d0',
#                                   label="basic distribution")
#             rect2 = plt.Rectangle((0, 0), 0, 0, color='#ff7f0ed0',
#                                   label="new distribution")
#             plt.gca().add_patch(rect1)
#             plt.gca().add_patch(rect2)
#             plt.xlabel("feature value")
#             plt.tight_layout()
#             plt.legend(loc=3)
#             plt.savefig("{}/{}/{}_distr.png".format(problem_id,
#                                                     feature_list[i],
#                                                     feature_list[i]))
#             plt.cla()
#             plt.close()
#         except ValueError:
#             plt.cla()
#             plt.close()
#             print("{} only have None value!".format(feature_list[i]))
