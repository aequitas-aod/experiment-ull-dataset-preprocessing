import os

import pandas as pd

from pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
)


def main():

    # Loading student questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "student_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # Load identifiers and change float columns to int
    ids = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "identifiers.csv"), low_memory=False
    )
    ids = ids.set_index("id_student")
    int_identifiers = [col for col in ids.columns if col not in ["id_class_group"]]
    ids[int_identifiers] = ids[int_identifiers].astype("Int64")

    # Merge identifiers and student questionnaire
    df = pd.merge(ids, df, left_index=True, right_index=True)


if __name__ == "__main__":
    main()
