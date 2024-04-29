import os

import pandas as pd

from src.pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
)


def main():

    print("Reading original file..")
    # Loading original dataset
    df = pd.read_csv(os.path.join(DATA_PATH, ORIGINAL_DATASET_NAME), low_memory=False)
    df = df.set_index("id_student")

    print("Change identifier types..")
    # Pre-process identifiers (i.e., change float columns to int)
    int_identifiers = [
        col for col in column_groups["identifiers"] if col not in ["id_class_group"]
    ]
    df[int_identifiers] = df[int_identifiers].astype("Int64")

    print("Print group sizes..")
    # Print group size (i.e., no. columns)
    for group, columns in column_groups.items():
        print(group, len(columns))

    print("Save splitted datasets..")
    # Save each group in a separated file
    for group, columns in column_groups.items():
        df[columns].to_csv(os.path.join(DATA_SPLIT_PATH, f"{group}.csv"))


if __name__ == "__main__":
    main()
