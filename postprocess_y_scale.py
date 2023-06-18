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


factors = [2**i for i in range(-6, 7)]
x = [math.log(f, 2) for f in factors]
print(factors)
print(x)

# os.chdir("/home/ian/thesis_data")
# df = pd.read_csv("experiment_y_scale_distr.csv")
# df_test = pd.read_csv("experiment_y_scale_kstest.csv")
# if not os.path.exists("/home/ian/thesis_results/experiment_y_scale/"):
#     os.mkdir("/home/ian/thesis_results/experiment_y_scale/")
# os.chdir("/home/ian/thesis_results/experiment_y_scale/")

os.chdir("/data/s3202844/data")
df = pd.read_csv("experiment_y_scale_distr.csv")
df_test = pd.read_csv("experiment_y_scale_kstest.csv")
if not os.path.exists("/home/s3202844/results/experiment_y_scale/"):
    os.mkdir("/home/s3202844/results/experiment_y_scale/")
os.chdir("/home/s3202844/results/experiment_y_scale/")

dataset_list = df.values.tolist()
columns = df.columns.values.tolist()
feature_list = columns[8:]

# remove limo features from feature list
feature_list = [f for f in feature_list if f[:4] != "limo"]

fig = plt.figure(figsize=(14, 16))
color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
linestyle = ["-", "--", ":", "-.", "-"]
for i in range(len(feature_list)):
    ax = fig.add_subplot(8, 7, i + 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.axhline(0.05, color="red", linestyle=":")
    for problem_id in range(1, 6):
        # 2 lists for 2 plots
        pvalue = []
        wd = []
        for f in factors:
            # parse pvalue
            test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
                                  (df_test["scale_factor"] == float(f)) &
                                  (df_test["is_scale"] == 1.0)][
                feature_list[i]].tolist()[0]
            test = string_to_list(test_string)
            pvalue += [test[1]]
            wd += [test[2]]
        t_ind = int(len(feature_list[i]) / 2)
        ax.plot(x, pvalue, color=color[problem_id - 1],
                linestyle=linestyle[problem_id - 1], linewidth=2,
                label="problem {}".format(problem_id))
ax = fig.add_subplot(8, 7, 56)
ax.set_yticks([])
ax.xaxis.set_label_coords(0.5, 0.1)
ax.yaxis.set_label_coords(0.1, 0.5)
ax.set_xlabel(r'$\log_2 scale\_factor$', fontsize=14)
ax.set_ylabel(r'p'+'-value', fontsize=14)
ax.plot(x[0], x[0])
ax.plot(x[-1], x[-1])
for problem_id in range(1, 6):
    ax.plot([0], [0], color=color[problem_id - 1],
            linestyle=linestyle[problem_id - 1], linewidth=2,
            label="problem {}".format(problem_id))
ax.legend(loc="upper right", borderaxespad=0, ncol=1, fontsize=12)
plt.tight_layout()
plt.savefig("pvalue.png")
plt.savefig("pvalue.eps", dpi=600, format='eps')
plt.cla()
plt.close()


fig = plt.figure(figsize=(14, 16))
color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
linestyle = ["-", "--", ":", "-.", "-"]
for i in range(len(feature_list)):
    ax = fig.add_subplot(8, 7, i + 1)
    ax.set_yticks([])
    ax.set_xticks([])
    for problem_id in range(1, 6):
        # 2 lists for 2 plots
        pvalue = []
        wd = []
        for f in factors:
            # parse pvalue
            test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
                                  (df_test["scale_factor"] == float(f)) &
                                  (df_test["is_scale"] == 1.0)][
                feature_list[i]].tolist()[0]
            test = string_to_list(test_string)
            pvalue += [test[1]]
            wd += [test[2]]
        wd_min = min(wd)
        wd_max = max(wd)
        for j in range(len(wd)):
            if wd[j] == wd_min:
                wd[j] = 0.0
            else:
                wd[j] = (wd[j] - wd_min) / (wd_max - wd_min)
        t_ind = int(len(feature_list[i]) / 2)
        ax.plot(x, wd, color=color[problem_id - 1],
                linestyle=linestyle[problem_id - 1], linewidth=2,
                label="problem {}".format(problem_id))
ax = fig.add_subplot(8, 7, 56)
ax.set_yticks([])
ax.xaxis.set_label_coords(0.5, 0.1)
ax.yaxis.set_label_coords(0.1, 0.5)
ax.set_xlabel(r'$\log_2 scale\_factor$', fontsize=14)
ax.set_ylabel('EMD', fontsize=14)
ax.plot(x[0], x[0])
ax.plot(x[-1], x[-1])
for problem_id in range(1, 6):
    ax.plot([0], [0], color=color[problem_id - 1],
            linestyle=linestyle[problem_id - 1], linewidth=2,
            label="problem {}".format(problem_id))
ax.legend(loc="upper right", borderaxespad=0, ncol=1, fontsize=12)
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
#         for f in factors:
#             # parse distribution
#             p_string = df[(df["problem_id"] == float(problem_id)) &
#                           (df["is_scale"] == 0.0)][feature_list[i]].tolist()[0]
#             q_string = df[(df["problem_id"] == float(problem_id)) &
#                           (df["scale_factor"] == float(f)) &
#                           (df["is_scale"] == 1.0)][feature_list[i]].tolist()[0]
#             p = string_to_list(p_string)
#             q = string_to_list(q_string)
#             for j in range(len(p)):
#                 PQf += [[p[j], q[j], f]]
#             # parse pvalue
#             test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
#                                   (df_test["scale_factor"] == float(f)) &
#                                   (df_test["is_scale"] == 1.0)][
#                 feature_list[i]].tolist()[0]
#             test = string_to_list(test_string)
#             pvalue += [test[1]]
#             wd += [test[2]]
#         # pvalue plot
#         plt.figure(figsize=(5, 5))
#         plt.ylim(-0.1, 1.1)
#         plt.plot(x, pvalue)
#         plt.axhline(0.05, color="red", linestyle=":")
#         plt.xlabel("$\log_2{scale\_factor}$")
#         plt.ylabel("$pvalue$")
#         plt.title("KS-test result of {}.".format(feature_list[i]))
#         plt.tight_layout()
#         plt.savefig("{}/{}/{}_pvalue.png".format(problem_id, feature_list[i],
#                                                  feature_list[i]))
#         plt.cla()
#         plt.close()
#         # wd plot
#         plt.figure(figsize=(5, 5))
#         plt.plot(x, wd)
#         plt.xlabel("$\log_2{scale\_factor}$")
#         plt.ylabel("$wd$")
#         plt.title("Wasserstein Distance result of {}.".format(feature_list[i]))
#         plt.tight_layout()
#         plt.savefig("{}/{}/{}_wd.png".format(problem_id, feature_list[i],
#                                              feature_list[i]))
#         plt.cla()
#         plt.close()
#         # distribution plot
#         PQf_df = pd.DataFrame(PQf, columns=["p", "q", "factor"])
#         try:
#             joypy.joyplot(PQf_df, by="factor", figsize=(6, 10),
#                           title="Distribution of ${}$ over scale factors.".format(
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
