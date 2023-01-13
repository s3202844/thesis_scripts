import os
import re
import shutil
import warnings
import argparse
import numpy as np
import pandas as pd

from pflacco.classical_ela_features import calculate_dispersion
from pflacco.classical_ela_features import calculate_ela_distribution
from pflacco.classical_ela_features import calculate_ela_level
from pflacco.classical_ela_features import calculate_ela_meta
from pflacco.classical_ela_features import calculate_information_content
from pflacco.classical_ela_features import calculate_limo
from pflacco.classical_ela_features import calculate_nbc
from pflacco.classical_ela_features import calculate_pca

warnings.filterwarnings("ignore")


def read_x(num_sampling, num_x):
    X = []
    m = num_x+1
    f = open("/data/s3202844/data/samplingX.txt", "r")
    lines = f.readlines()
    f.close()
    for i in range(num_sampling):
        x = []
        content = lines[m*i:m*i+m]
        for j in range(1, m):
            temp = []
            line = re.split(r"[ ]+", content[j][:-1])
            for n in line[1:]:
                temp += [float(n)]
            x += [temp]
        X += [x]
    return X


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


def save_calculate_features(X, y, prefix, table_name,
                            target, problem_id, written):
    keys = []
    values = []

    if target == "disp":
        disp = calculate_dispersion(X, y)
        keys += list(disp.keys())[:-1]
        values += list(disp.values())[:-1]
    elif target == "ela_distr":
        ela_distr = calculate_ela_distribution(X, y)
        keys += list(ela_distr.keys())[:-1]
        values += list(ela_distr.values())[:-1]
    elif target == "ela_level":
        ela_level = calculate_ela_level(X, y)
        keys += list(ela_level.keys())[:-1]
        values += list(ela_level.values())[:-1]
    elif target == "ela_meta":
        ela_meta = calculate_ela_meta(X, y)
        keys += list(ela_meta.keys())[:-1]
        values += list(ela_meta.values())[:-1]
    elif target == "ic":
        ic = calculate_information_content(X, y)
        keys += list(ic.keys())[:-1]
        values += list(ic.values())[:-1]
    elif target == "limo":
        limo = calculate_limo(X, y, lower_bound=[-100. for _ in range(dim)],
                              upper_bound=[100. for _ in range(dim)])
        keys += ["limo.avg_length_norm", "limo.length_mean", "limo.ratio_mean"]
        values += [limo[keys[-3]], limo[keys[-2]], limo[keys[-1]]]
    elif target == "nbc":
        nbc = calculate_nbc(X, y)
        keys += list(nbc.keys())[:-1]
        values += list(nbc.values())[:-1]
    elif target == "pca":
        pca = calculate_pca(X, y)
        keys += list(pca.keys())[:-1]
        values += list(pca.values())[:-1]

    record = prefix + values
    column_names = ["problem_id", "experiment_id", "subtract_lim",
                    "rotate_lim", "scale_factor", "is_subtract",
                    "is_rotate", "is_scale"] + keys
    dataset_df = pd.DataFrame([record], columns=column_names)
    if not written:
        dataset_df.to_csv("tmp-"+table_name+"-" +
                          str(problem_id)+"-"+target+".csv", index=False)
    else:
        dataset_df.to_csv("tmp-"+table_name+"-" +
                          str(problem_id)+"-"+target+".csv", index=False,
                          header=False, mode="a")


if __name__ == "__main__":
    # meta data
    num_sampling = 100
    num_x = 1000
    dim = 10
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="description of the experiment")
    parser.add_argument("-p", help="path for original experiment data")
    parser.add_argument("-f", help="feature set's name")
    parser.add_argument("-i", type=int, help="ID of the problem")
    args = parser.parse_args()
    if args.d == None or args.f == None or args.i == None:
        parser.print_help()
        exit()
    table_name = args.d
    problem_id = args.i
    data_path = args.p
    target = args.f
    # collect basic data for table
    # problem_ids = []
    experiment_ids = []
    subtract_lims = []
    rotate_lims = []
    scale_factors = []
    is_subtracts = []
    is_rotates = []
    is_scales = []
    file_list = []
    file_list_tmp = os.listdir(data_path)
    for file_name in file_list_tmp:
        match_obj = re.match(
            r"(\d+)_(\d+)_(\d+\.\d+)_(\d+\.\d+)_(\d+\.\d+)_(\d+)_(\d+)_(\d+)\.txt",
            file_name)
        if int(match_obj.group(1)) != problem_id:
            continue
        experiment_ids += [int(match_obj.group(2))]
        subtract_lims += [float(match_obj.group(3))]
        rotate_lims += [float(match_obj.group(4))]
        scale_factors += [float(match_obj.group(5))]
        is_subtracts += [float(match_obj.group(6))]
        is_rotates += [float(match_obj.group(7))]
        is_scales += [float(match_obj.group(8))]
        file_list += [file_name]
    # read experiments results
    X = np.array(read_x(num_sampling, num_x))
    Y = []
    for file_name in file_list:
        file_path = data_path + file_name
        y = read_y(file_path, num_sampling, num_x)
        Y += [y]
        print("Read file:", file_path)
    Y = np.array(Y)
    # create table
    written = False
    for file_ind in range(Y.shape[0]):
        for i in range(num_sampling):
            prefix = [problem_id, experiment_ids[file_ind],
                      subtract_lims[file_ind], rotate_lims[file_ind],
                      scale_factors[file_ind], is_subtracts[file_ind],
                      is_rotates[file_ind], is_scales[file_ind]]
            save_calculate_features(X[i], Y[file_ind][i], prefix, table_name,
                                    target, problem_id, written)
            if not written:
                written = True
    os.rename("tmp-"+table_name+"-"+str(problem_id)+"-"+target+".csv",
              table_name+"-"+str(problem_id)+"-"+target+".csv")
    shutil.move(table_name+"-"+str(problem_id)+"-"+target+".csv",
                table_name+"/"+table_name+"-"+str(problem_id)+"-"+target+".csv")
