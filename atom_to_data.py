import os
import re
import sys
import numpy as np
import pandas as pd


def parse_file_names(file_list):
    features = []
    id_ind = []
    for file_name in file_list:
        match_obj = re.match(r"(\w+)-(\d+)-(\w+)\.csv", file_name)
        problem_id = match_obj.group(2)
        feature = match_obj.group(3)
        if problem_id not in id_ind:
            features += [[problem_id, feature]]
            id_ind += [problem_id]
        else:
            features[id_ind.index(problem_id)] += [feature]
    return features


def verify_input_features(input_features, feature_list):
    result = True
    for rec in input_features:
        for f in feature_list:
            if f not in rec:
                print("Miss feature! problem_id: {}, feature: {}".format(
                    rec[0], f))
                result = False
    return result


def parse_experiment_data(input_features, feature_list, description):
    id_ind = [input_features[i][0] for i in range(len(input_features))]
    unique_header = []
    num_feature = 0
    for problem_id in id_ind:
        for feature in feature_list:
            temp_df = pd.read_csv("{}-{}-{}.csv".format(description,
                                  problem_id, feature))
            temp_list = temp_df.values.tolist()
            if problem_id == id_ind[0]:
                num_feature += len(temp_list[0])-8
            for rec in temp_list:
                if rec[:8] not in unique_header:
                    unique_header += [rec[:8]]
    return unique_header, num_feature


def merge_features(feature_list, description, unique_header,
                   num_sampling, num_feature):
    dataset = [[None for _ in range(num_feature+8)]
               for _ in range(len(unique_header)*num_sampling)]
    columns = ["problem_id", "experiment_id", "subtract_lim",
               "rotate_lim", "scale_factor", "is_subtract",
               "is_rotate", "is_scale"]
    for feature in feature_list:
        temp_df = pd.read_csv("{}-{}-{}.csv".format(description,
                                                    int(unique_header[0][0]),
                                                    feature))
        columns += temp_df.columns.values[8:].tolist()
    header_counter = 0
    for header in unique_header:
        feature_counter = 0
        for feature in feature_list:
            temp_df = pd.read_csv("{}-{}-{}.csv".format(description,
                                  int(header[0]), feature))
            temp_list = temp_df.values.tolist()
            sampling_counter = 0
            for i in range(len(temp_list)):
                if temp_list[i][:8] == header:
                    j = header_counter*num_sampling+sampling_counter
                    for k in range(8):
                        dataset[j][k] = temp_list[i][k]
                    for k in range(len(temp_list[0][8:])):
                        dataset[j][8+feature_counter+k] = temp_list[i][8+k]
                    sampling_counter += 1
            feature_counter += len(temp_list[0][8:])
        header_counter += 1
    dataset_df = pd.DataFrame(dataset, columns=columns)
    dataset_df.to_csv(
        "/data/s3202844/data/{}.csv".format(description), index=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please indicate the experiment by its description!")
        print("Must run this script in the folder that hold the <description>!")
        sys.exit()
    num_sampling = 100
    feature_list = ["disp", "ela_distr", "ela_level",
                    "ela_meta", "ic", "nbc", "pca"]
    description = sys.argv[1]
    os.chdir(description)
    file_list = os.listdir()
    input_features = parse_file_names(file_list)
    if not verify_input_features(input_features, feature_list):
        sys.exit()
    unique_header, num_feature = parse_experiment_data(input_features,
                                                       feature_list,
                                                       description)
    merge_features(feature_list, description, unique_header,
                   num_sampling, num_feature)
