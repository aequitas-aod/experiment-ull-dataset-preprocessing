import pandas as pd
import os
from utils import aggregate_features, features_to_drop_after_aggregation, custom_mean, custom_binary_agg, custom_sum, get_good_bad_agg, aggregate_mixed_features, mixed_features_to_drop

from macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    ORIGINAL_DATASET_NAME,
    agg_sum,
    agg_mean,
    agg_custom_binary,
    agg_mix,
    to_rename
)

def main():

    # Loading teacher questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "teacher_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # drop features with too many nans
    # df = df.drop(df.columns[features_with_too_many_nans(df, 0.8)], axis=1, inplace=False)

    # aggregate features row-wise using mean
    new_features = aggregate_features(df, agg_mean, 
                                      aggregation_func=custom_mean
                                      )
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    df = df.drop(df.columns[features_to_drop_after_aggregation(df, agg_mean)], axis=1, inplace=False)

    # repeat with binary features that are not important taken one by one
    # features are aggregated through a custom sum that skips NaNs
    new_features = aggregate_features(df, agg_sum, 
                                      aggregation_func=custom_sum
                                      )
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    df = df.drop(df.columns[features_to_drop_after_aggregation(df, agg_sum)], axis=1, inplace=False)

    # repeat with binary features that are important taken one by one
    # features are aggregated through a custom function that returns a unique integer for each combination of values
    new_features = aggregate_features(df, agg_custom_binary, 
                                      aggregation_func=custom_binary_agg
                                      )
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    df = df.drop(df.columns[features_to_drop_after_aggregation(df, agg_custom_binary)], axis=1, inplace=False)

    # update aggregation map in case features have been dropped
    agg_mix_new = {}
    for k in agg_mix.keys():
        temp = {}
        for feat, col_names in agg_mix[k].items():
            temp[feat] =  [x for x in col_names if x in df.columns]
        agg_mix_new[k] = temp

    # maximum degree of agreement
    max_deg = 4
    to_lambdate = {
    "satisfaction_with_job_and_school": lambda x: get_good_bad_agg(x,
                                                            group="satisfaction_with_job_and_school",
                                                            aggregation_map=agg_mix_new,
                                                            max_degree_of_agreement=max_deg),
    "behaviour_problems_solution": lambda x: get_good_bad_agg(x,
                                                            group="behaviour_problems_solution",
                                                            aggregation_map=agg_mix_new,
                                                            max_degree_of_agreement=max_deg),
    "results_satisfaction": lambda x: get_good_bad_agg(x,
                                                            group="results_satisfaction",
                                                            aggregation_map=agg_mix_new,
                                                            max_degree_of_agreement=max_deg)  
    }

    new_features = aggregate_mixed_features(df, agg_mix_new, to_lambdate)
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()

    # drop features after aggregating
    df = df.drop(df.columns[mixed_features_to_drop(df, agg_mix_new)], axis=1, inplace=False)

    # rename features
    df = df.rename(columns=to_rename)

    print(f"Done! Number of columns: {df.shape[1]}")
    df.to_csv(os.path.join(DATA_SPLIT_PATH, "teacher_questionnaire_preprocessed.csv"), index=False)




if __name__ == "__main__":
    main()
