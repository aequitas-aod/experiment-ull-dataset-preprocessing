import pandas as pd
import os
from utils import features_with_too_many_nans, aggregate_features, features_to_drop_after_aggregation

from macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
    teacher_non_binary_feature_list,
    teacher_binary_feature_list
)

def main():

    # Loading teacher questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "teacher_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # drop features with too many nans
    features_to_drop = features_with_too_many_nans(df, 0.9)
    df = df.drop(df.columns[features_to_drop], axis=1, inplace=False)

    # aggregate non binary features
    # missing values are set to zero, features are aggregated row wise through the mean
    new_features = aggregate_features(df, teacher_non_binary_feature_list, 
                                      aggregation_func="mean", 
                                      na_values_strategy="zeros"
                                      )
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    features_to_drop = features_to_drop_after_aggregation(df, teacher_non_binary_feature_list)
    df = df.drop(df.columns[features_to_drop], axis=1, inplace=False)

    # repeat with binary features
    # missing values are set to zero, features are aggregated through a sum
    new_features = aggregate_features(df, teacher_binary_feature_list, 
                                      aggregation_func="sum", 
                                      na_values_strategy="zeros")
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    features_to_drop = features_to_drop_after_aggregation(df, teacher_binary_feature_list)
    df = df.drop(df.columns[features_to_drop], axis=1, inplace=False)

    print(f"Done! Number of columns: {df.shape[1]}")
    print(df.columns)

if __name__ == "__main__":
    main()
