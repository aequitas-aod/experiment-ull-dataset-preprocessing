# %%
import pandas as pd
import numpy as np
import os
from src.pre_processing.macros import (
    DATA_PATH,
    DATA_PREPROC_PATH,
    ORIGINAL_DATASET_NAME,
)


def print_missing_values_ranges(range_count: dict):
    for k, v in range_count.items():
        print(
            f"Number of columns with a proportion of missing values in range {k}: {v}"
        )


def postprocessing_stats(df_orig: pd.DataFrame, df_merged: pd.DataFrame):

    # init ranges
    ranges = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)]
    range_count = {str(range): 0 for range in ranges}

    # update_ranges
    for col in df_merged.columns:
        nans = df_merged[col].isna().sum() / df_merged.shape[0]
        for range in ranges:
            if nans >= range[0] and nans < range[1]:
                range_count[str(range)] += 1
            if nans == 1.0:
                range_count[str(ranges[-1])] += 1

    # show stats about mvs ranges
    print_missing_values_ranges(range_count=range_count)

    # other stats
    print("\n" + "#" * 10 + "\n")
    nans_orig = np.sum(df_orig.isna().sum())
    nans_merged = np.sum(df_merged.isna().sum())

    size_orig = df_orig.shape[0] * df_orig.shape[1]
    size_merged = df_merged.shape[0] * df_merged.shape[1]

    print(
        f"Amount of data reduction: {((size_orig - size_merged) / size_orig) * 100} %"
    )
    print(
        f"Proportion of missing values before preprocessing: {(nans_orig/size_orig) * 100} %"
    )
    print(
        f"Proportion of missing values after preprocessing: {(nans_merged/size_merged) * 100} %"
    )


if __name__ == "__main__":
    df_orig = pd.read_csv(
        os.path.join(DATA_PATH, ORIGINAL_DATASET_NAME), low_memory=False
    )
    df_merged = pd.read_csv(
        os.path.join(DATA_PREPROC_PATH, "merged.csv"), low_memory=False
    )
    postprocessing_stats(df_orig=df_orig, df_merged=df_merged)
