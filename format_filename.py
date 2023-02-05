import os
import re
import pandas as pd
import numpy as np

# os.chdir("/data/s3202844/data/subtract")
# file_list = os.listdir("/data/s3202844/data/subtract")
# print(file_list)
# df = pd.read_csv("/data/s3202844/data/experiment_subtract.csv")
# header = df.columns.values[1:].tolist()
# header = ["problem_id", "experiment_id", "subtract_lim", "rotate_lim",
#           "scale_factor", "is_subtract", "is_rotate", "is_scale"] + header[4:]
# data = df.values[:, 1:]
# dataset = []
# for i in range(data.shape[0]):
#     dataset += [[data[i][0], data[i][1], data[i][2], 0.0,
#                  1.0, data[i][3], 0, 0] + data[i][4:].tolist()]
# dataset = np.array(dataset)
# dataset = pd.DataFrame(dataset, columns=header)
# dataset.to_csv("/data/s3202844/data/experiment_subtract.csv", index=False)
# for file_name in file_list:
#     match_obj = re.match(
#         r"(\d+)_(\d+)_(\d+\.\d+)_(\d+\.\d+)_(\d+)_(\d+)\.txt",
#         file_name)
#     problem_id = match_obj.group(1)
#     experiment_id = match_obj.group(2)
#     subtract_lim = match_obj.group(3)
#     rotate_lim = match_obj.group(4)
#     is_subtract = match_obj.group(5)
#     is_rotate = match_obj.group(6)
#     os.rename(file_name, problem_id + "_" + experiment_id + "_" +
#               subtract_lim + "_" + rotate_lim + "_1.000000_" +
#               is_subtract + "_" + is_rotate + "_0.txt")
