import os
import re

os.chdir("/data/s3202844/data/subtract")
file_list = os.listdir("/data/s3202844/data/subtract")
print(file_list)
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
