import os

import pandas as pd
from src.pre_processing.macros import DATA_PREPROC_PATH, DATA_SPLIT_PATH
from src.pre_processing.principal_questionnaire import (
    preprocess_principal_questionnaire,
)
from src.pre_processing.family_questionnaire import preprocess_family_questionnaire
from src.pre_processing.student_questionnaire import preprocess_student_questionnaire
from src.pre_processing.teacher_questionnaire import preprocess_teacher_questionnaire


def main():

    print("Pre-processing...")
    print("\tStudent Questionnaire")
    student_df = preprocess_student_questionnaire()
    print("\tPrincipal Questionnaire")
    principal_df = preprocess_principal_questionnaire()
    print("\tFamily Questionnaire")
    family_df = preprocess_family_questionnaire()
    print("\tTeacher Questionnaire")
    teacher_df = preprocess_teacher_questionnaire()

    print("Merging...")
    print("\tStudent and Principal Questionnaires")
    merged_df = pd.merge(student_df, principal_df, left_index=True, right_index=True)
    print("\tFamily Questionnaire")
    merged_df = pd.merge(merged_df, family_df, left_index=True, right_index=True)
    print("\tTeacher Questionnaire")
    merged_df = pd.merge(merged_df, teacher_df, left_index=True, right_index=True)
    merged_df.to_csv(os.path.join(DATA_PREPROC_PATH, "merged.csv"))
    print("\tAdd indices")
    indices_df = pd.read_csv(os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False)[["id_student","id_year"]]
    indices_df = indices_df.set_index("id_student")

    # Check if a row has more than 90% of missing data and remove it
    missing_data = merged_df.isnull().sum(axis=1)
    missing_data = missing_data[missing_data > 0.9 * merged_df.shape[1]]
    print("\tSaving records with more than 90% of missing data")
    merged_df.loc[missing_data.index].to_csv(os.path.join(DATA_PREPROC_PATH, "missing_data.csv"))
    print(f"\tRemoving {missing_data.shape[0]} rows with more than 90% of missing data")
    merged_df = merged_df.drop(index=missing_data.index)

    # If a column is nan for at least one year (id_year), then it is a MCAR type of missing data
    null_df = merged_df.isnull()
    null_df_id_year = pd.merge(null_df, indices_df, left_index=True, right_index=True)
    mcar = null_df_id_year.groupby("id_year").all().sum(axis=0)
    mcar = mcar[mcar > 0].index
    print(f"\tThere are {len(mcar)} columns with MCAR missing data")

    merged_df = merged_df.drop(columns=mcar)
    merged_df.to_csv(os.path.join(DATA_PREPROC_PATH, "merged.csv"))

    print("Done!")


if __name__ == "__main__":
    main()
