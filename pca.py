import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA

df = pd.read_csv("/data/s3202844/data/experiment_subtract.csv")
data = []
for i in range(2, 6):
    temp_data = df[(df["problem_id"] == i) & (df["is_subtract"] == 0) & (
        df["is_rotate"] == 0) & (df["is_scale"] == 0)].values
    norms = np.linalg.norm(temp_data[:, 8:], axis=0)
    temp_data[:, 8:] = temp_data[:, 8:] / norms
    data.append(temp_data)
data = np.concatenate(data)
X = data[:, 8:]
Y = data[:, 0]
X[np.isnan(X) | np.isinf(X)] = 0
pca = PCA(n_components=2)
pca.fit(X)
X_r = pca.transform(X)
plt.figure()
colors = ['navy', 'turquoise', 'darkorange', 'cornflowerblue', 'teal']
lw = 2
problem_id = [i for i in range(2, 6)]
# problem_id = [2, 3]
labels = ["problem {}".format(i) for i in problem_id]
for color, i, target_name in zip(colors[1:], problem_id, labels):
    plt.scatter(X_r[Y == i, 0], X_r[Y == i, 1], color=color, alpha=.8, lw=lw,
                label=target_name)
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('PCA of dataset')
plt.savefig("pca25.png")
