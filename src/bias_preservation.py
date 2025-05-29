# -*- coding: utf-8 -*-
"""# Install"""

# !pip install xgboost

"""# Imports"""


from sklearn.metrics import accuracy_score
from scipy.stats import ttest_rel, ks_2samp, wilcoxon, chi2_contingency, f_oneway
from sklearn.model_selection import StratifiedKFold
from xgboost import XGBClassifier
from sklearn.preprocessing import label_binarize
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, CategoricalNB
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, KBinsDiscretizer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import copy
import math
import time
import os


"""# Settings"""

path = "/home/raw_data/validation"

datasets = ["original", "final"]
meta_data_ops = "meta_data_mapping.csv"
meta_data_new = "meta_data_new.json"
# sensitive_feat = "f_ESCS"
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
    "score_LEN",
    "score_ING",
]
level_features = ["level_MAT", "level_LEN", "level_ING"]

to_drop = [
    "d30a",
    "d30b",
    "d30c",
    "d30d",
    "d30e",
    "d30f",
    "d301",
    "d302",
    "d303",
    "d304",
    "d305",
    "d306",
    "d307",
    "d308",
    "weight",
    "p_group_criteria_alphabet",
    "p_group_criteria_gender",
    "p_group_criteria_language",
    "p_group_criteria_performance",
    "p_group_criteria_homogeneity",
    "p_group_criteria_heterogeneity",
    "s_weight",
]

# ESCS bins and labels
bins = [-np.inf, -2, -1, 0, 1, 2, np.inf]  # Set bins at -2σ, -1σ, 0σ, 1σ, 2σ
labels = ["VERY LOW", "LOW", "BELOW AVG", "ABOVE AVG", "HIGH", "VERY HIGH"]


def load_and_run():
    """# Meta-data Loading"""

    metadata_ops = pd.read_csv(os.path.join(path, meta_data_ops))

    # Defining the lists
    s_columns = [
        "a1",
        "a2",
        "a3a",
        "a3b",
        "living_with_father_mother",
        "a3c",
        "a3d",
        "a3et",
        "a3f",
        "a4",
        "repeater",
        "a5",
        "a6nm",
        "a7",
        "a8a",
        "a8b",
        "a8c",
        "a09a",
        "a09b",
        "a09c",
        "a09d",
        "a09e",
        "a9a",
        "a9b",
        "a9c",
        "a9d",
        "a9e",
        "a9f",
        "a9g",
        "a10a",
        "a10b",
        "a10c",
        "a10d",
        "a10e",
        "a10f",
        "a10g",
        "a10h",
        "a10i",
        "a10j",
        "a10k",
        "a10l",
        "a10m",
        "a10n",
        "a11a",
        "a11b",
        "a11c",
        "a11d",
        "a11e",
        "a11f",
        "a11g",
        "a11h",
        "a12a",
        "a12b",
        "a12c",
        "a12d",
        "a12e",
        "a12f",
        "a12g",
        "a12h",
        "a12i",
        "a13a",
        "a13b",
        "a13c",
        "a13d",
        "a13e",
        "a14a",
        "a14b",
        "a14c",
        "a14d",
        "a14e",
        "a14f",
        "a14g",
        "a14h",
        "a15a",
        "a15b",
        "a15c",
        "a15d",
        "a15e",
        "a15f",
        "a15g",
        "a15h",
        "a15i",
        "a15j",
        "a16a",
        "a16b",
        "a16c",
        "a16d",
        "a16e",
        "a16f",
        "a16g",
        "a16h",
        "a16i",
        "a16j",
        "a16k",
        "a16l",
        "a17a",
        "a17b",
        "a17c",
        "a17d",
        "a17e",
        "a17f",
        "a17g",
        "a17h",
        "a20a",
        "a20b",
        "a20c",
        "a20d",
        "a20e",
        "a21a",
        "a21b",
        "a21c",
        "a21d",
        "a21e",
        "a22a",
        "a22b",
        "a22c",
        "a22d",
        "a23a",
        "a23b",
        "a23c",
        "a23d",
        "a23e",
        "a23f",
        "a23g",
        "a23h",
        "a23i",
        "a23j",
        "a23k",
        "a24",
        "a40a",
        "a40b",
        "a40c",
        "a40d",
        "a41",
        "a42",
        "a51",
        "a61",
        "a71",
        "a111a",
        "a141g",
        "a144d",
        "a144h",
        "a160k",
        "a162k",
        "a163k",
        "a166f",
        "a166k",
        "a171h",
        "a177d",
        "a211a",
        "a222b",
        "country_iso_cnac",
        "country_iso_nac",
        "Weight",
    ]
    p_columns = [
        "d1",
        "d2n",
        "d3n",
        "d4n",
        "d5n",
        "d6n",
        "d7n",
        "d8n",
        "d9a1",
        "d9a2",
        "d9b1",
        "d9b2",
        "d9c1",
        "d9c2",
        "d9d1",
        "d9d2",
        "d9e1",
        "d9e2",
        "d9f1",
        "d9f2",
        "d9g1",
        "d9g2",
        "d9h1",
        "d9h2",
        "d10a",
        "d10b",
        "d10c",
        "d11an",
        "d11bn",
        "d12an",
        "d12bn",
        "d13n",
        "d14",
        "d15",
        "d16an",
        "d16bn",
        "d16cn",
        "d16dn",
        "d16en",
        "d16fn",
        "d17a",
        "d17b",
        "d17c",
        "d17d",
        "d17e",
        "d17f",
        "d17g",
        "d17h",
        "d18a",
        "d18b",
        "d18c",
        "d18d",
        "d18e",
        "d18f",
        "d18g",
        "d18h",
        "d18i",
        "d18j",
        "d18k",
        "d18l",
        "d18m",
        "d18n",
        "d19a",
        "d19b",
        "d19c",
        "d19d",
        "d19e",
        "d19f",
        "d19g",
        "d19h",
        "d19i",
        "d19j",
        "d19k",
        "d19l",
        "d19m",
        "d19n",
        "d19o",
        "d19p",
        "d19q",
        "d19r",
        "d20a",
        "d20b",
        "d20c",
        "d20d",
        "d20e",
        "d20f",
        "d20g",
        "d20h",
        "d20i",
        "d20j",
        "d20k",
        "d20l",
        "d21a",
        "d21b",
        "d21c",
        "d21d",
        "d21e",
        "d21f",
        "d22a",
        "d22b",
        "d22c",
        "d22d",
        "d22e",
        "d22f",
        "d30a",
        "d30b",
        "d30c",
        "d30d",
        "d30e",
        "d30f",
        "d31a",
        "d31b",
        "d31c",
        "d32a",
        "d33a",
        "d121a",
        "d121b",
        "d131a",
        "d131b",
        "d301",
        "d302",
        "d303",
        "d304",
        "d305",
        "d306",
        "d307",
        "d308",
        "tasa_nac_eso4",
        "tasa_nac_pri3",
        "tasa_nac_pri6",
        "distnac",
        "distnac_eso4",
        "distnac_pri3",
        "distnac_pri6",
        "groups",
        "island",
        "capital_island",
        "public_private",
    ]
    f_columns = [
        "f0",
        "f1n",
        "f2an",
        "f2bn",
        "f3a",
        "f3b",
        "mother_education",
        "father_education",
        "f4a",
        "f4b",
        "f5a",
        "f5b",
        "f5n",
        "inmigrant",
        "inmigrant2",
        "inmigrant_second_gen",
        "f6",
        "f7",
        "f8ta",
        "f8tm",
        "start_schooling_age",
        "f9a",
        "f9b",
        "f9c",
        "f9d",
        "f9e",
        "f9f",
        "f9g",
        "f9h",
        "f10n",
        "f11",
        "books",
        "f12a",
        "f12b",
        "f13n",
        "f14a",
        "f14b",
        "f14c",
        "f15a",
        "f15b",
        "f15c",
        "f15d",
        "f15e",
        "f15f",
        "f16a",
        "f16b",
        "f16c",
        "f16d",
        "f16e",
        "f16f",
        "f17a",
        "f17b",
        "f17c",
        "f17d",
        "f18a",
        "f18b",
        "f18c",
        "f18d",
        "f18e",
        "f18f",
        "f18g",
        "f18h",
        "f18i",
        "f19a",
        "f19b",
        "f19c",
        "f19d",
        "f19e",
        "f20",
        "f21n",
        "f22",
        "f23",
        "f24a",
        "f24b",
        "mother_occupation",
        "father_occupation",
        "f30",
        "f31",
        "single_parent_household",
        "f33a",
        "f33b",
        "f33c",
        "f33d",
        "f33e",
        "f33f",
        "f33g",
        "f33h",
        "f34",
        "household_income_q",
        "nhousehold",
        "ESCS",
    ]
    t_columns = [
        "p2",
        "p2n",
        "p3n",
        "p4n",
        "p5",
        "p6n",
        "p7an",
        "p7bn",
        "p7cn",
        "p7dn",
        "p7en",
        "p7fn",
        "p7gn",
        "p8an",
        "p8bn",
        "p9a",
        "p9b",
        "p9c",
        "p9d",
        "p9e",
        "p9f",
        "p10n",
        "p11",
        "p12a",
        "p12b",
        "p12c",
        "p12d",
        "p13",
        "p13b",
        "p13c",
        "p15a",
        "p15b",
        "p15c",
        "p15d",
        "p15e",
        "p15f",
        "p15g",
        "p15h",
        "p15i",
        "p16a",
        "p16b",
        "p16c",
        "p16d",
        "p16e",
        "p16f",
        "p16g",
        "p16h",
        "p18a",
        "p18b",
        "p18c",
        "p18d",
        "p18e",
        "p18f",
        "p18g",
        "p18h",
        "p18i",
        "p19",
        "p20",
        "p21a",
        "p21b",
        "p21c",
        "p21d",
        "p21e",
        "p21f",
        "p22a",
        "p22b",
        "p22c",
        "p22d",
        "p22e",
        "p22f",
        "p22g",
        "p23a",
        "p23b",
        "p23c",
        "p23d",
        "p23e",
        "p23f",
        "p23g",
        "p23h",
        "p23i",
        "p24a",
        "p24b",
        "p24c",
        "p24d",
        "p24e",
        "p24f",
        "p24g",
        "p24h",
        "p24i",
        "p24j",
        "p24k",
        "p25",
        "p26",
        "p26a",
        "p26b",
        "p26c",
        "p26d",
        "p27a",
        "p27b",
        "p27c",
        "p27d",
        "p27e",
        "p27f",
        "p27g",
        "p27h",
        "p28n",
        "p29a",
        "p29b",
        "p29c",
        "p29d",
        "p29e",
        "p30a",
        "p30b",
        "p30c",
        "p31d",
        "p32a",
        "p32b",
        "p32c",
        "p32d",
        "p32e",
        "p34a",
        "p34b",
        "p34c",
        "p34d",
        "p34e",
        "p34f",
        "p34g",
        "p41a",
        "p41b",
        "p41c",
        "p41d",
        "p41e",
        "p41f",
        "p41g",
        "p41h",
        "p41i",
        "p41j",
        "p141",
        "p171n",
        "p172n",
        "p299d",
        "p311a",
        "p311b",
        "p311c",
        "p311e",
        "p311f",
        "p311g",
        "p311h",
        "p331a",
        "p331b",
        "p331c",
        "p331d",
        "p331e",
        "p331f",
        "p331g",
        "p331j",
        "pfc",
        "rep",
    ]

    # Function to determine prefix based on the column

    def add_prefix(row):
        if type(row["new_column"]) == str:
            new_col = row["new_column"].replace("\r", "").replace("\n", "")
            if row["original_column"] in s_columns:
                return f"s_{new_col}"
            elif row["original_column"] in p_columns:
                return f"p_{new_col}"
            elif row["original_column"] in f_columns:
                return f"f_{new_col}"
            elif row["original_column"] in t_columns:
                return f"t_{new_col}"
        return row["new_column"]  # No prefix added if not in any list

    # Apply the prefix function
    metadata_ops["new_column"] = metadata_ops.apply(add_prefix, axis=1)
    sanity_check = (
        metadata_ops.groupby("new_column")["sensitive"]
        .apply(lambda x: list(dict.fromkeys(x)))
        .apply(lambda x: all(i == x[0] for i in x))
        .to_list()
    )
    if all(sanity_check):
        metadata_sensitive = (
            metadata_ops.groupby("new_column")["sensitive"]
            .first()
            .apply(lambda x: x == "Yes")
            .to_dict()
        )

        with open(os.path.join(path, meta_data_new), "r") as file:
            metadata = json.load(file)

        for new_col in metadata.keys():
            metadata[new_col]["sensitive"] = metadata_sensitive[new_col]

        sanity_check_2 = [
            len(value["original_columns"]) == 1
            for new_col, value in metadata.items()
            if value["sensitive"]
        ]
        if all(sanity_check_2):
            sensitive_mapping = {
                value["original_columns"][0]: new_col
                for new_col, value in metadata.items()
                if value["sensitive"]
            }
            sensitive_features = list(sensitive_mapping.values())

            print(metadata)
            print(sensitive_mapping)
            print(f"{len(sensitive_features)} senstive features: ", sensitive_features)
        else:
            raise Exception("Sanity check 2 failed")
    else:
        raise Exception("Sanity check failed")

    """# Data Loading & Cleaning

    ## for Random Forest
    """

    dfs = {}
    dfs_control = {}
    dfs_pivoted = {}

    cat_encoder = {}
    sens_encoder = {}
    num_discretizer = {}

    categorical_features = {}

    for dataset in datasets:
        # print(dataset)
        # print()

        # Load
        df = pd.read_csv(os.path.join(path, f"{dataset}.csv"))
        df = df.drop(
            id_features + control_features + to_drop, axis="columns", errors="ignore"
        )
        if dataset == "original":
            df = df.rename(columns={"id_student": "id_questionnaire"})
            df = df.rename(columns=sensitive_mapping)
        df = df.set_index("id_questionnaire")

        # Discretize ESCS
        df["f_ESCS"] = pd.cut(df["f_ESCS"], bins=bins, labels=labels)
        # df["f_ESCS"] = pd.cut(df["f_ESCS"], bins=bins, labels=labels).values.add_categories("MISSING")
        # df["f_ESCS"] = df["f_ESCS"].fillna("MISSING")

        categorical_features[dataset] = [
            col
            for col in df.select_dtypes(include=["object", "category"]).columns.tolist()
            if col not in sensitive_features
            and col not in score_features
            and col not in level_features
        ]
        # numerical_features = [
        #     col
        #     for col in df.select_dtypes(exclude=["object", "category"]).columns.tolist()
        #     if col not in sensitive_features and
        #     col not in score_features and
        #     col not in level_features
        # ]

        cat_encoder[dataset] = OrdinalEncoder()
        df[categorical_features[dataset]] = cat_encoder[dataset].fit_transform(
            df[categorical_features[dataset]]
        )
        # df[categorical_features] = df[categorical_features].fillna(-1)

        sens_encoder[dataset] = OrdinalEncoder()
        df[sensitive_features] = sens_encoder[dataset].fit_transform(
            df[sensitive_features]
        )
        # df[sensitive_features] = df[sensitive_features].fillna(-1)

        # df[numerical_features] = df[numerical_features].fillna(0)
        # for col in numerical_features:
        #     num_discretizer[col] = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="kmeans")
        #     df[col] = num_discretizer[col].fit_transform(df[[col]])
        #     # df[col] = df[col].astype(int)

        dfs[dataset] = df

    dfs["original"] = dfs["original"].loc[dfs["final"].index]
    print(dfs["original"].shape)
    print(list(dfs["original"].columns))
    print(dfs["final"].shape)
    print(list(dfs["final"].columns))

    """# Algorithm Running

    ## Random Forest

    ### Instance Filtering

    #### No cross-validation
    """

    probabilities_p_y_given_si = {}
    performances = {}
    for algorithm in ["RandomForestClassifier"]:
        print(f"Algorithm: {algorithm}")
        probabilities_p_y_given_si[algorithm] = {}
        performances[algorithm] = {}
        for n_estimators in [500]:
            print(f"\tNo. estimators: {n_estimators}")
            probabilities_p_y_given_si[algorithm][n_estimators] = {}
            performances[algorithm][n_estimators] = {}
            for dataset, df in dfs.items():
                print(f"\t\tDataset: {dataset}")
                probabilities_p_y_given_si[algorithm][n_estimators][dataset] = {}
                performances[algorithm][n_estimators][dataset] = {}

                X, y = (
                    df.drop(
                        score_features + level_features, axis="columns", errors="ignore"
                    ),
                    df[level_features],
                )
                for target_feat in level_features:
                    print(f"\t\t\tTarget Feature: {target_feat}")
                    probabilities_p_y_given_si[algorithm][n_estimators][dataset][
                        target_feat
                    ] = {}
                    performances[algorithm][n_estimators][dataset][target_feat] = {}

                    y_encoder = LabelEncoder()
                    y_encoded = y_encoder.fit_transform(y[target_feat])

                    current_X = copy.deepcopy(X)

                    rf_classifier = globals()[algorithm](n_estimators=n_estimators)
                    start_time = time.time()
                    rf_classifier.fit(current_X, y_encoded)
                    fitting_time = time.time() - start_time
                    start_time = time.time()
                    y_pred = rf_classifier.predict(current_X)
                    inference_time = time.time() - start_time

                    acc = accuracy_score(y_encoded, y_pred)
                    precision = precision_score(
                        y_encoded, y_pred, average="weighted", zero_division=0
                    )
                    recall = recall_score(
                        y_encoded, y_pred, average="weighted", zero_division=0
                    )

                    performances[algorithm][n_estimators][dataset][target_feat] = {
                        "accuracy": acc,
                        "precision": precision,
                        "recall": recall,
                        "fitting_time": fitting_time,
                        "inference_time": inference_time,
                    }

                    print(f"\t\t\t\tAccuracy: {acc:.4f}")
                    print(f"\t\t\t\tPrecision: {precision:.4f}")
                    print(f"\t\t\t\tRecall: {recall:.4f}")
                    print(f"\t\t\t\tFitting time: {fitting_time:.2f} seconds")
                    print(f"\t\t\t\tInference time: {inference_time:.2f} seconds")

                    cat_X = copy.deepcopy(current_X)
                    cat_X[categorical_features[dataset]] = cat_encoder[
                        dataset
                    ].inverse_transform(current_X[categorical_features[dataset]])
                    cat_X[sensitive_features] = sens_encoder[dataset].inverse_transform(
                        current_X[sensitive_features]
                    )

                    for sens_feat in sensitive_features:

                        probabilities = {}
                        for i, s_value in enumerate(cat_X[sens_feat].unique()):
                            if type(s_value) != str and math.isnan(s_value):
                                X_to_input = current_X[current_X[sens_feat].isna()]
                            else:
                                X_to_input = current_X[cat_X[sens_feat] == s_value]

                            class_probabilities = rf_classifier.predict_proba(
                                X_to_input
                            ).mean(axis=0)
                            for cls_idx, prob in enumerate(class_probabilities):
                                class_label = y_encoder.inverse_transform([cls_idx])[0]
                                stringed_key = "___".join(
                                    [str(s_value), str(class_label)]
                                )
                                probabilities[stringed_key] = float(prob)

                        # Store results for the sensitive feature
                        probabilities_p_y_given_si[algorithm][n_estimators][dataset][
                            target_feat
                        ][sens_feat] = probabilities

                    # Print probabilities
                    for sens_feat, probs in probabilities_p_y_given_si[algorithm][
                        n_estimators
                    ][dataset][target_feat].items():
                        # print(f"\n\t\t\t\tProbabilities P(Y | {sens_feat}):")
                        for stringed_key, prob in probs.items():
                            s_value, class_label = stringed_key.split("___")
                            # print(
                            #     f"\t\t\t\t\tP(Y={class_label} | {sens_feat}={s_value}) = {prob:.4f}")
                        # print()

                    with open(
                        os.path.join(path, "probabilities_p_y_given_si.json"), "w"
                    ) as f:
                        json.dump(probabilities_p_y_given_si, f)

                    with open(os.path.join(path, "performance_metrics.json"), "w") as f:
                        json.dump(performances, f)


try:
    with open(os.path.join(path, "probabilities_p_y_given_si.json"), "r") as file:
        probabilities_p_y_given_si = json.load(file)
except:
    load_and_run()


"""### Statistic Tests"""


def compare_probability_matrices(probabilities_p_y_given_si, tolerance=1e-5):
    indeces = {}
    # Loop through datasets, target features, and sensitive features
    for algorithm in probabilities_p_y_given_si.keys():
        print(f"Algorithm: {algorithm}")
        indeces[algorithm] = {}
        for n_estimators in probabilities_p_y_given_si[algorithm].keys():
            print(f"\tNo. estimators: {n_estimators}")
            indeces[algorithm][n_estimators] = {}
            for target_feat in probabilities_p_y_given_si[algorithm][n_estimators][
                "original"
            ].keys():
                print(f"\t\tTarget Feature: {target_feat}")
                indeces[algorithm][n_estimators][target_feat] = {}

                for sens_feat in probabilities_p_y_given_si[algorithm][n_estimators][
                    "original"
                ][target_feat].keys():
                    print(f"\t\t\tSensitive Feature: {sens_feat}")
                    indeces[algorithm][n_estimators][target_feat][sens_feat] = {}

                    # Extract probabilities
                    original_probs = probabilities_p_y_given_si[algorithm][
                        n_estimators
                    ]["original"][target_feat][sens_feat]
                    final_probs = probabilities_p_y_given_si[algorithm][n_estimators][
                        "final"
                    ][target_feat][sens_feat]

                    # Convert to DataFrames: Rows are sensitive values, Columns are class labels
                    original_matrix = pd.DataFrame(
                        [
                            (
                                stringed_key.split("___")[0],
                                stringed_key.split("___")[1],
                                p,  # int(p * 100),
                            )
                            for stringed_key, p in original_probs.items()
                        ],
                        columns=["sensitive_value", "class_label", "probability"],
                    ).pivot(
                        index="sensitive_value",
                        columns="class_label",
                        values="probability",
                    )

                    final_matrix = pd.DataFrame(
                        [
                            (
                                stringed_key.split("___")[0],
                                stringed_key.split("___")[1],
                                p,  # int(p * 100),
                            )
                            for stringed_key, p in final_probs.items()
                        ],
                        columns=["sensitive_value", "class_label", "probability"],
                    ).pivot(
                        index="sensitive_value",
                        columns="class_label",
                        values="probability",
                    )

                    print(f"\n\t\t\tOriginal Probability Matrix:\n{original_matrix}")
                    print(f"\n\t\t\tFinal Probability Matrix:\n{final_matrix}")

                    # Flatten matrices to arrays for statistical tests
                    original_flat = original_matrix.values.flatten()
                    final_flat = final_matrix.values.flatten()

                    # Run Statistical Tests
                    print("\n\t\t\tStatistical Test Results:")

                    # 1. Paired t-Test
                    try:
                        t_stat, p_value = ttest_rel(original_flat, final_flat)
                        indeces[algorithm][n_estimators][target_feat][sens_feat][
                            "t_test"
                        ] = {"stat": t_stat, "p_value": p_value}
                        print(
                            f"\t\t\tPaired t-Test: t-stat = {t_stat:.4f}, p-value = {p_value:.4e}"
                        )
                    except Exception as e:
                        print(f"\t\t\tPaired t-Test: Failed due to {e}")

                    # 2. Wilcoxon Signed-Rank Test
                    try:
                        w_stat, p_value = wilcoxon(original_flat, final_flat)
                        indeces[algorithm][n_estimators][target_feat][sens_feat][
                            "w_stat"
                        ] = {"stat": w_stat, "p_value": p_value}
                        print(
                            f"\t\t\tWilcoxon Signed-Rank Test: w-stat = {w_stat:.4f}, p-value = {p_value:.4e}"
                        )
                    except Exception as e:
                        print(f"\t\t\tWilcoxon Signed-Rank Test: Failed due to {e}")

                    # 3. Kolmogorov-Smirnov Test
                    try:
                        ks_stat, p_value = ks_2samp(original_flat, final_flat)
                        indeces[algorithm][n_estimators][target_feat][sens_feat][
                            "ks_test"
                        ] = {"stat": ks_stat, "p_value": p_value}
                        print(
                            f"\t\t\tKolmogorov-Smirnov Test: ks-stat = {ks_stat:.4f}, p-value = {p_value:.4e}"
                        )
                    except Exception as e:
                        print(f"\t\t\tKolmogorov-Smirnov Test: Failed due to {e}")

                    # 4. Chi-Square Test (for frequencies or probabilities summing to 1 per row)
                    try:
                        original_frequencies = original_matrix.div(
                            original_matrix.sum(axis=1), axis=0
                        ).fillna(0)
                        final_frequencies = final_matrix.div(
                            final_matrix.sum(axis=1), axis=0
                        ).fillna(0)

                        chi2_stat, p_value, _, _ = chi2_contingency(
                            pd.concat([original_frequencies, final_frequencies]).values
                        )
                        indeces[algorithm][n_estimators][target_feat][sens_feat][
                            "chi_test"
                        ] = {"stat": chi2_stat, "p_value": p_value}
                        print(
                            f"\t\t\tChi-Square Test: chi2-stat = {chi2_stat:.4f}, p-value = {p_value:.4e}"
                        )
                    except Exception as e:
                        print(f"\t\t\tChi-Square Test: Failed due to {e}")

                    # 5. Absolute Difference and Mean Absolute Error
                    absolute_diff = np.abs(original_flat - final_flat)
                    max_diff = np.max(absolute_diff)
                    mae = np.mean(absolute_diff)
                    indeces[algorithm][n_estimators][target_feat][sens_feat][
                        "max_diff"
                    ] = max_diff
                    indeces[algorithm][n_estimators][target_feat][sens_feat][
                        "mae"
                    ] = mae
                    print(f"\t\t\tMax Absolute Difference: {max_diff:.6f}")
                    print(f"\t\t\tMean Absolute Error (MAE): {mae:.6f}")

                    print("\n")

                    with open(os.path.join(path, "indeces.json"), "w") as f:
                        json.dump(indeces, f)
    return indeces


indeces = compare_probability_matrices(probabilities_p_y_given_si)

# Define the number of observations for each sensitive feature
observations = {
    "s_gender": 15,
    "s_has_repeated": 15,
    "s_birth_country": 370,
    "s_nazionality_country": 390,
    "p_island": 25,
    "p_public_or_private": 15,
    "f_mother_education_level": 50,
    "f_father_education_level": 50,
    "f_mother_employment_status": 30,
    "f_father_employment_status": 30,
    "f_mother_place_of_birth": 25,
    "f_father_place_of_birth": 25,
    "f_student_place_of_birth": 25,
    "f_extent_of_books_at_home": 30,
    "f_parental_education_expectations": 35,
    "f_mother_occupation": 25,
    "f_father_occupation": 25,
    "f_monthly_household_income": 55,
    "f_ESCS": 35,
}

# Constants: Number of target labels and sensitive labels
TARGET_LABELS = 5  # Adjust accordingly if this changes
SENSITIVE_LABELS = {
    feat: len(set(range(obs // TARGET_LABELS)))  # Assuming equal rows across s
    for feat, obs in observations.items()
}


# Functions to calculate expected ranges
def calculate_t_range(n):
    # Approximate range for t-statistic based on normal distribution
    return (-2, 2)


def calculate_ks_range(n1, n2):
    # Critical value for KS test
    c_alpha = 1.36  # For alpha = 0.05
    d_critical = c_alpha * math.sqrt((n1 + n2) / (n1 * n2))
    return (0, round(d_critical, 2))


def calculate_chi_range(target_labels, sensitive_labels):
    # Calculate degrees of freedom for chi-squared test
    df = (target_labels - 1) * (sensitive_labels - 1)
    return (0, round(df, 2))


# Generate LaTeX Table
def generate_latex_table(data, observations):
    criticals = {}
    latex_table = "\\begin{table}[htbp]\n\\centering\n\\caption{Statistical tests results in comparing the distributions $P(h(X_\\text{original})|S)$ and $P(h(X_\\text{prep})|S)$ according to Sensitive Features $S$. The differences between the distributions (stat) are averaged among the possible target features (math, spanish, and english levels). The stat value, the lower the better, is colored red depending on how far it is from the critical value (critic).}\n\\resizebox{\\textwidth}{!}{%\n\\begin{tabular}{l|ll|ll|ll|ll|ll}\n"
    # latex_table += (
    #     "\\textbf{Sensitive Feature} & \\multicolumn{8}{c|}{\\textbf{level\\_MAT}} & "
    #     "\\multicolumn{8}{c|}{\\textbf{level\\_LEN}} & \\multicolumn{8}{c|}{\\textbf{level\\_ING}} \\\\\n"
    # )
    # latex_table += (
    #     "& \\multicolumn{2}{c|}{t-stat} & \\multicolumn{2}{c|}{ks-stat} & \\multicolumn{2}{c|}{chi-stat} & "
    #     "Max Diff & MAE & \\multicolumn{2}{c|}{t-stat} & \\multicolumn{2}{c|}{ks-stat} & "
    #     "\\multicolumn{2}{c|}{chi-stat} & Max Diff & MAE & \\multicolumn{2}{c|}{t-stat} & \\multicolumn{2}{c|}{ks-stat} & "
    #     "\\multicolumn{2}{c|}{chi-stat} & Max Diff & MAE \\\\\n"
    # )
    # latex_table += "& stat & range & stat & critic & stat & critic & & & stat & range & stat & critic & stat & critic & & & stat & range & stat & critic & stat & critic & & \\\\\n\\hline\n"

    latex_table += (
        "\\textbf{Sensitive Feature} & \\multicolumn{2}{c|}{T-Test} & \\multicolumn{2}{c|}{KS-Test} & \\multicolumn{2}{c|}{Chi-Test} & "
        "\\multicolumn{2}{c|}{Max Diff} & \\multicolumn{2}{c}{MAE} \\\\\n"
    )
    latex_table += "& Stat & Critic & Stat & Critic & Stat & Critic & Stat & Critic & Stat & Critic \\\\\n\\hline\n"

    levels = ["level_MAT", "level_LEN", "level_ING"]

    # Fill the table row by row
    for feature in observations:
        row = feature.replace("_", "\\_")
        # for level in levels:
        # if level in data:
        feat_data = {
            test: [
                (
                    data[level][feature][test]["stat"]
                    if type(data[level][feature][test]) == dict
                    else data[level][feature][test]
                )
                for level in levels
            ]
            for test in ["t_test", "ks_test", "chi_test", "max_diff", "mae"]
        }
        feat_data = {
            test: {
                "mean": np.mean(values),
                "std": np.std(values),
            }
            for test, values in feat_data.items()
        }

        t_range = calculate_t_range(observations[feature])
        ks_range = calculate_ks_range(observations[feature], observations[feature])
        chi_range = calculate_chi_range(TARGET_LABELS, SENSITIVE_LABELS[feature])
        if feature not in criticals:
            criticals[feature] = {
                "t-test": t_range,
                "ks-test": ks_range[1],
                "chi-test": chi_range[1],
            }

        chi_spacer = lambda x: "~~~~" if x < 10 else ("~~" if x < 100 else "")
        t_spacer = lambda x: "~~~" if x > 0 else ""
        get_percentage = lambda value, ref: round((value * 100) / (ref * 100), 2) * 100

        t_content = f"${abs(feat_data['t_test']['mean']):.0e}~(\pm~{feat_data['t_test']['std']:.0e})$"
        t_content = (
            "\cellcolor{red!"
            + str(int(get_percentage(feat_data["t_test"]["mean"], t_range[1])))
            + "}{"
            + t_content
            + "}"
        )
        ks_content = f"${feat_data['ks_test']['mean']:.2f}~(\pm~{feat_data['ks_test']['std']:.2f})$"
        ks_content = (
            "\cellcolor{red!"
            + str(int(get_percentage(feat_data["ks_test"]["mean"], ks_range[1])))
            + "}{"
            + ks_content
            + "}"
        )
        chi_content = f"${feat_data['chi_test']['mean']:.2f}~{chi_spacer(feat_data['chi_test']['mean'])}(\pm~{feat_data['chi_test']['std']:.2f})$"
        chi_content = (
            "\cellcolor{red!"
            + str(int(get_percentage(feat_data["chi_test"]["mean"], chi_range[1])))
            + "}{"
            + chi_content
            + "}"
        )
        max_diff_content = f"${feat_data['max_diff']['mean']:.2f}~(\pm~{feat_data['max_diff']['std']:.2f})$"
        max_diff_content = (
            "\cellcolor{red!"
            + str(int(get_percentage(feat_data["max_diff"]["mean"], 1)))
            + "}{"
            + max_diff_content
            + "}"
        )
        mae_content = (
            f"${feat_data['mae']['mean']:.2f}~(\pm~{feat_data['mae']['std']:.2f})$"
        )
        mae_content = (
            "\cellcolor{red!"
            + str(int(get_percentage(feat_data["mae"]["mean"], 1)))
            + "}{"
            + mae_content
            + "}"
        )

        # \cellcolor{blue!72}

        row += (
            f" & {t_content} & {t_range[1]} "
            f" & {ks_content} & {ks_range[1]} "
            f" & {chi_content} & {chi_range[1]} "
            f" & {max_diff_content} & 1 & {mae_content} & 1"
        )
        latex_table += row + " \\\\\n"

    with open(os.path.join(path, "criticals.json"), "w") as c_file:
        json.dump(criticals, c_file)

    latex_table += "\n\\end{tabular}\n}\n\\end{table}"
    return latex_table


# Generate the LaTeX table
for algo, algo_value in indeces.items():
    for n_estimators, n_estimators_value in algo_value.items():
        latex_code = generate_latex_table(n_estimators_value, observations)

        if algo == "RandomForestClassifier" and n_estimators == "500":
            suffix = ""
        else:
            suffix = "_" + algo + n_estimators

        # Save all tables into a single LaTeX file
        output_file = os.path.join(path, f"bias_preservation{suffix}.tex")
        os.makedirs(path, exist_ok=True)
        with open(output_file, "w") as tex_file:
            tex_file.write(latex_code)
