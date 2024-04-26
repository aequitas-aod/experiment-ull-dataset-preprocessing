import os

import pandas as pd

from src.pre_processing.macros import DATA_PREPROC_PATH
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
    print("Done!")


if __name__ == "__main__":
    main()
