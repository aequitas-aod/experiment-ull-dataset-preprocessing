# -*- coding: utf-8 -*-
"""# Install"""

# !pip install 'maxcorr[full]'

"""# Imports"""

import os

import copy

import json

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.preprocessing import OrdinalEncoder

from maxcorr import indicator


"""# Settings"""

path = "/home/raw_data/validation/"

datasets = ["original", "final"]
meta_data_new = "meta_data_new.json"
sensitive_feat = "f_ESCS"
control_feat = "id_year"

id_features = [
    # "id_questionnaire",
    # "id_student",
    "id_student_original",
    "id_grade",
    "id_class_group",
    "id_school",
    "id_student_16_19",
    "id_school_16_19",
]
control_features = [
    "student_questionnaire",
    "family_questionnaire",
    "principals_questionnaire",
    "teachers_questionnaire",
    "census",
    "scores",
]
score_features = [
    "score_MAT",
    "level_MAT",
    "score_LEN",
    "level_LEN",
    "score_ING",
    "level_ING",
]

# ESCS bins and labels
bins = [-np.inf, -2, -1, 0, 1, 2, np.inf]  # Set bins at -2σ, -1σ, 0σ, 1σ, 2σ
labels = ["VERY LOW", "LOW", "BELOW AVG", "ABOVE AVG", "HIGH", "VERY HIGH"]

"""# Src

## Data Loading
"""

dfs = {}
dfs_control = {}
dfs_pivoted = {}

for dataset in datasets:
    # print(dataset)
    # print()

    # Load
    df = pd.read_csv(os.path.join(path, f"{dataset}.csv"))
    df = df.drop(
        id_features + control_features + score_features, axis="columns", errors="ignore"
    )
    if dataset == "original":
        df = df.rename(columns={"id_student": "id_questionnaire"})
        df = df.rename(columns={"ESCS": sensitive_feat})
    df = df.set_index("id_questionnaire")

    # Discretize ESCS
    # df[sensitive_feat] = pd.cut(df[sensitive_feat], bins=bins, labels=labels)

    # Encode all categorical features
    categorical_features = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    encoder = OrdinalEncoder()
    df[categorical_features] = encoder.fit_transform(df[categorical_features])

    dfs[dataset] = df.fillna(-1)

dfs["original"] = dfs["original"].loc[dfs["final"].index]

dfs["original"] = dfs["original"].rename(columns={"f_ESCS": "ESCS"})

for dataset in datasets:
    dfs_control[dataset] = {
        c: df[df[control_feat] == c] for c in df[control_feat].unique()
    }

    for c in dfs_control[dataset]:
        dfs_control[dataset][c] = dfs_control[dataset][c].drop(
            control_feat, axis="columns"
        )

for year in dfs_control["original"].keys():
    dfs_pivoted[year] = {}
    for dataset in datasets:
        dfs_pivoted[year][dataset] = dfs_control[dataset].get(
            year, pd.DataFrame()
        )  # Handle missing years gracefully

"""## Meta-data Loading"""

with open(os.path.join(path, meta_data_new), "r") as file:
    metadata = json.load(file)

current_col = 1
total_cols = len(metadata)
for new_col, value in metadata.items():
    old_cols = value["original_columns"]
    operation = value["operation"]

    print(f"Col no. {current_col} out of {total_cols}")
    current_col += 1
    print(f"{new_col}\t{operation} ({len(old_cols)} cols)")

    if "corr" not in metadata[new_col]:
        metadata[new_col]["corr"] = {}

        # if len(old_cols) > 1:
        for algorithm in ["dk", "sk"]:
            if algorithm in metadata[new_col]["corr"]:
                corr = metadata[new_col]["corr"][algorithm]
            else:
                a = dfs["final"][new_col].to_numpy()
                b = dfs["original"][old_cols].to_numpy()
                ind = indicator(semantics="hgr", algorithm=algorithm, backend="numpy")
                corr = round(
                    ind.compute(dfs["final"][new_col], dfs["original"][old_cols]) * 100,
                    3,
                )
                metadata[new_col]["corr"][algorithm] = corr

    for algorithm in ["dk", "sk"]:
        print(f"""\t{algorithm}:\t{metadata[new_col]["corr"][algorithm]}\n""")

    with open(os.path.join(path, meta_data_new), "w") as f:
        json.dump(metadata, f)

filtered_corrs = [
    values["corr"]
    for feat, values in metadata.items()
    if values["operation"] != "none"
    and feat
    not in [
        "p_group_criteria_alphabet",
        "p_group_criteria_gender",
        "p_group_criteria_language",
        "p_group_criteria_performance",
        "p_group_criteria_homogeneity",
        "p_group_criteria_heterogeneity",
        "s_weight",
    ]
]
method_corrs = []
for method in ["sk", "dk"]:
    method_corrs += [elem[method] for elem in filtered_corrs]
print("\n\nSUMMARY\n\n")
print(
    f"""mean: {np.mean(method_corrs)},\n\tstd: {np.std(method_corrs)},\n\tmin: {np.min(method_corrs)}"""
)
