import os
import re
import numpy as np


def read_y(path, num_sampling, num_x):
    Y = []
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    for i in range(num_sampling):
        y = []
        line = lines[i][:-1].split(" ")
        for j in range(num_x):
            y += [float(line[j])]
        Y += [y]
    return Y


if __name__ == "__main__":
    # meta data
    num_sampling = 100
    num_x = 1000
    dim = 10
    data_path = "/data/s3202844/data/atom_rotation/"
    os.chdir(data_path)
    file_list_tmp = os.listdir(data_path)
    for file_name in file_list_tmp:
        match_obj = re.match(
            r"(\d+)_(\d+)_(\d+\.\d+)_(\d+\.\d+)_(\d+\.\d+)_(\d+)_(\d+)_(\d+)\.txt",
            file_name)
        if float(match_obj.group(7)) != 0.0:
            continue
        problem_id = int(match_obj.group(1))
        experiment_id = 0
        rotate_lim = 0.
        scale_factor = 1.
        is_subtract = 1
        is_rotate = 0
        is_scale = 0
        y = np.array(read_y(file_name, num_sampling, num_x))
        path = "/data/s3202844/data/atom_y_subtract/" \
            + "{}_{}_{}_{}_{}_{}_{}_{}.txt".format(
                problem_id, experiment_id, 0.0, rotate_lim,
                scale_factor, 0, is_rotate, is_scale)
        np.savetxt(path, y)
        for sub in range(0, 1100, 100):
            subtract_lim = float(sub)
            new_y = y + subtract_lim
            path = "/data/s3202844/data/atom_y_subtract/" \
                + "{}_{}_{}_{}_{}_{}_{}_{}.txt".format(
                    problem_id, experiment_id, subtract_lim, rotate_lim,
                    scale_factor, is_subtract, is_rotate, is_scale)
            np.savetxt(path, new_y)
