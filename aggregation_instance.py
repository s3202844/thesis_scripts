import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def string_to_list(string):
    string = string[1:-1]
    content = string.split(", ")
    return [float(c) for c in content]


X = [5.0 * n for n in range(1, 21)]

# os.chdir("/home/ian/thesis_data")
# df = pd.read_csv("experiment_10_subtract_distr.csv")
# df_test = pd.read_csv("experiment_10_subtract_kstest.csv")
# if not os.path.exists("/home/ian/thesis_results/experiment_10_subtract/"):
#     os.mkdir("/home/ian/thesis_results/experiment_10_subtract/")
# os.chdir("/home/ian/thesis_results/experiment_10_subtract/")

os.chdir("/data/s3202844/data")
df = pd.read_csv("experiment_10_subtract_distr.csv")
df_test = pd.read_csv("experiment_10_subtract_kstest.csv")
if not os.path.exists("/scratch/hyin/thesis_scripts/experiment_10_subtract/"):
    os.mkdir("/scratch/hyin/thesis_scripts/experiment_10_subtract/")
os.chdir("/scratch/hyin/thesis_scripts/experiment_10_subtract/")

columns = df.columns.values.tolist()
feature_list = columns[8:]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('translation limit', fontsize=12)
ax.set_ylabel('aggregation process', fontsize=12)
ax.set_zlabel('Earth Mover\'s Distance', fontsize=12)
sx = np.linspace(0, 100, 100)
sz = np.linspace(0, 1, 100)
sx, sz = np.meshgrid(sx, sz)
sy = np.array([[0 for _ in range(100)] for _ in range(100)])
ax.plot_surface(sx, sy, sz, color='white', alpha=0.5)


WD = [0 for _ in range(20)]
for i in range(len(feature_list)):
    for problem_id in range(1, 6):
        wd = []
        for j in range(len(X)):
            x = X[j]
            # parse pvalue
            test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
                                  (df_test["subtract_lim"] == float(x)) &
                                  (df_test["is_subtract"] == 1.0)][
                feature_list[i]].tolist()[0]
            test = string_to_list(test_string)
            wd += [test[2]]
        wd_min = min(wd)
        wd_max = max(wd)
        for j in range(len(wd)):
            if wd[j] == wd_min:
                wd[j] = 0.0
            else:
                wd[j] = (wd[j] - wd_min) / (wd_max - wd_min)
            WD[j] += wd[j] / len(feature_list)

ax.plot(X, [0]*20, wd, linewidth=2)




# selected_features = [0, 16, 20, 27, 53]
selected_features = [0, 16, 20, 53]
color = ["#8c564b", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
linestyle = ["-", "--", ":", "-.", "-"]

k = 1
for i in selected_features:
    sx = np.linspace(0, 100, 100)
    sz = np.linspace(0, 1, 100)
    sx, sz = np.meshgrid(sx, sz)
    sy = np.array([[0+10*k for _ in range(100)] for _ in range(100)])
    ax.plot_surface(sx, sy, sz, color='gray', alpha=0.5)
    for problem_id in range(1, 6):
        # 2 lists for 2 plots
        wd = []
        for x in X:
            # parse pvalue
            test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
                                  (df_test["subtract_lim"] == float(x)) &
                                  (df_test["is_subtract"] == 1.0)][
                feature_list[i]].tolist()[0]
            test = string_to_list(test_string)
            wd += [test[2]]
        wd_min = min(wd)
        wd_max = max(wd)
        for j in range(len(wd)):
            if wd[j] == wd_min:
                wd[j] = 0.0
            else:
                wd[j] = (wd[j] - wd_min) / (wd_max - wd_min)
        ax.plot(X, [0+10*k]*20, 
                # [cache+0.2*k for cache in wd], 
                wd,
                color=color[problem_id - 1],
                linestyle=linestyle[problem_id - 1], linewidth=2,
                label="problem {}".format(problem_id))
    k += 1
# ax.legend()
ax.scatter([50, 50, 50], [k*10, k*10+5, k*10+10], [0.5, 0.5, 0.5], color='black')
ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])
ax.zaxis.set_ticks([])
ax.xaxis.set_ticklabels([])
ax.yaxis.set_ticklabels([])
ax.zaxis.set_ticklabels([])
# ax.set_frame_on(False)
ax.view_init(elev=20, azim=-150)
plt.tight_layout()
plt.savefig("aggregation.png")
plt.show()
