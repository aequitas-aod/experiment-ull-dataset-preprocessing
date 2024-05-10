import json
import math
import os

import pandas as pd
from src.pre_processing.macros import (
    DATA_PATH,
    DATA_PREPROC_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
    RES_PATH,
    BEN_PATH,
)
from src.pre_processing.principal_questionnaire import (
    preprocess_principal_questionnaire,
)
from src.pre_processing.family_questionnaire import preprocess_family_questionnaire
from src.pre_processing.student_questionnaire import preprocess_student_questionnaire
from src.pre_processing.teacher_questionnaire import preprocess_teacher_questionnaire
from src.pre_processing.utils import normalize_merged_dataset
from src.stats.missing_values_stats import postprocessing_stats


def main():

    ####### SPLIT AND PREPROCESSING #######

    print("Splitting and Pre-processing...")
    print("\tStudent Questionnaire")
    student_df = preprocess_student_questionnaire(load=True)
    student_df = student_df.add_prefix("s_")
    print("\tPrincipal Questionnaire")
    principal_df = preprocess_principal_questionnaire(load=True)
    principal_df = principal_df.add_prefix("p_")
    print("\tFamily Questionnaire")
    family_df = preprocess_family_questionnaire(load=True)
    family_df = family_df.add_prefix("f_")
    print("\tTeacher Questionnaire")
    teacher_df = preprocess_teacher_questionnaire(load=True)
    teacher_df = teacher_df.add_prefix("t_")
    print()

    ####### MERGING #######

    print("Merging...")
    print("\tStudent and Principal Questionnaires")
    merged_df = pd.merge(student_df, principal_df, left_index=True, right_index=True)
    print("\tFamily Questionnaire")
    merged_df = pd.merge(merged_df, family_df, left_index=True, right_index=True)
    print("\tTeacher Questionnaire")
    merged_df = pd.merge(merged_df, teacher_df, left_index=True, right_index=True)
    print()

    ####### MISSING VALUES #######

    print("Checking missing values...")
    # Check if a row has more than 90% of missing data and remove it
    missing_data = merged_df.isnull().sum(axis=1)
    missing_data = missing_data[missing_data > 0.9 * merged_df.shape[1]]
    print("\tSaving records with more than 90% of missing data")
    merged_df.loc[missing_data.index].to_csv(
        os.path.join(DATA_PREPROC_PATH, "rows_with_missing_values_ge_90.csv")
    )
    print(f"\tRemoving {missing_data.shape[0]} rows with more than 90% of missing data")
    merged_df = merged_df.drop(index=missing_data.index)

    # If a column is nan for at least one year (id_year), then it is a MAR type of missing data
    null_df = merged_df.isnull()
    indices_df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    )[["id_student", "id_year"]]
    indices_df = indices_df.set_index("id_student")
    null_df_id_year = pd.merge(null_df, indices_df, left_index=True, right_index=True)
    mar = null_df_id_year.groupby("id_year").all().sum(axis=0)
    mar = mar[mar > 0].index
    print(f"\tThere are {len(mar)} columns with MAR missing data")

    # merged_df = merged_df.drop(columns=mar)
    merged_df.to_csv(os.path.join(DATA_PREPROC_PATH, "merged.csv"))
    print()

    ####### NORMALIZING #######

    print("Normalizing...")

    # merged_df = normalize_merged_dataset(merged_df)
    normalized_df = normalize_merged_dataset(merged_df)
    normalized_df.to_csv(os.path.join(DATA_PREPROC_PATH, "normalized.csv"))
    print()

    ####### NEW MERGING #######

    print("Merging with identifiers and scores...")

    ids = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    )
    ids = ids.set_index("id_student")
    int_identifiers = [col for col in ids.columns if col not in ["id_class_group"]]
    ids[int_identifiers] = ids[int_identifiers].astype("Int64")

    # Load identifiers and change float columns to int
    scores = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "student_scores.csv"), low_memory=False
    )
    scores = scores.set_index("id_student")

    ids = pd.merge(ids, scores, left_index=True, right_index=True)
    final_df = pd.merge(ids, normalized_df, left_index=True, right_index=True)

    final_df = final_df.reset_index()
    final_df = final_df.rename(columns={"id_student": "id_questionnaire"})
    final_df = final_df.set_index("id_questionnaire")
    final_df.to_csv(os.path.join(DATA_PREPROC_PATH, "final.csv"))
    final_df.to_csv(os.path.join(BEN_PATH, "dataset.csv"))

    final_df = pd.read_csv(os.path.join(DATA_PREPROC_PATH, "final.csv"))
    final_df = final_df.set_index("id_questionnaire")

    print()

    ####### RUNNING QUALITY CHECKS #######

    print("Running quality checks...")

    # Import meta data of merged
    with open(os.path.join(RES_PATH, "meta_data_final.json")) as file:
        meta_data = json.load(file)

    # Check each features is in range
    print("\tPrinting Errors:")
    error = False
    for col, details in meta_data.items():
        # print(col)
        value = details["values"][0][0]
        # if value == ["1", "2", "3", "4"]:
        #     value = {"min": 1, "max": 4}
        if value not in [["Unknown"], ["Integer"], ["Float"]]:
            if type(value) == dict:
                try:
                    col_min = final_df[col].min()
                    col_max = final_df[col].max()
                    if col_min < int(value["min"]) or col_max > int(value["max"]):
                        error = True
                        print(
                            f""""\t\tNO IN LIMIT\n\tcol:{col}, col_min:{col_min}, col_max:{col_max}, min_value:{value["min"]}, max_value:{value["max"]} """
                        )
                except:
                    error = True
                    print(col)
                    print(
                        [
                            elem
                            for elem in final_df[col].unique()
                            if type(elem) == str or not math.isnan(elem)
                        ]
                    )
            elif type(value) == list:
                distinct_in_col = [
                    elem
                    for elem in final_df[col].unique()
                    if type(elem) == str or not math.isnan(elem)
                ]
                value = (
                    value if not value[0].isdigit() else [int(elem) for elem in value]
                )
                if "True" not in value:
                    # if distinct_in_col not in value:
                    if not set(distinct_in_col).issubset(set(value)):
                        error = True
                        print(
                            f""""NO IN LIST\n\tcol:{col}, distinct_in_col:{distinct_in_col}, value:{value}"""
                        )
    if not (error):
        print("\tAll clear!")
    print()

    ####### RUNNING QUALITY CHECKS #######

    print("Giving some stats...")

    df_orig = pd.read_csv(
        os.path.join(DATA_PATH, ORIGINAL_DATASET_NAME), low_memory=False
    )

    postprocessing_stats(df_orig=df_orig, df_merged=final_df.reset_index())
    print()

    ####### EXPORTING META-DATA #######

    print("Exporting meta-data for missing patterns...")

    final_df.isna().to_csv(os.path.join(DATA_PREPROC_PATH, "missing_mask.csv"))
    final_df.isna().to_csv(os.path.join(BEN_PATH, "missing_mask.csv"))

    print("Done!")


if __name__ == "__main__":
    main()
