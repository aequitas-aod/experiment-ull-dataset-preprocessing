from src.pre_processing import *
from src.pre_processing.utils import (
    aggregate_features,
    features_to_drop_after_aggregation,
    custom_mean,
    custom_binary_agg,
    custom_sum,
    get_good_bad_agg,
    aggregate_mixed_features,
    mixed_features_to_drop,
    normalize_in_new_range,
)

from src.pre_processing.macros import (
    column_groups,
    DATA_PATH,
    DATA_SPLIT_PATH,
    DATA_PREPROC_PATH,
    ORIGINAL_DATASET_NAME,
    agg_sum,
    agg_mean,
    agg_custom_binary,
    agg_mix,
    to_rename,
)


def preprocess_teacher_questionnaire(load=False):

    if load:
        df = pd.read_csv(os.path.join(DATA_PREPROC_PATH, "teacher_questionnaire.csv"))
        return df.set_index("id_student")

    # Loading teacher questionnaire
    df = pd.read_csv(
        os.path.join(DATA_SPLIT_PATH, "teacher_questionnaire.csv"), low_memory=False
    )
    df = df.set_index("id_student")

    # normalize "bad" columns
    df["p331g"] = df["p331g"].apply(
        lambda x: normalize_in_new_range(
            num=x, old_min=1, old_max=5, new_min=1, new_max=4
        )
    )
    df["p331j"] = df["p331j"].apply(
        lambda x: normalize_in_new_range(
            num=x, old_min=1, old_max=5, new_min=1, new_max=4
        )
    )

    # drop redundant features that have the most NaNs
    to_drop = "p5" if df["p5"].isna().sum() > df["rep"].isna().sum() else "rep"
    df = df.drop(to_drop, axis=1, inplace=False)

    pfc_topics = [
        "p15a",
        "p15b",
        "p15c",
        "p15d",
        "p15e",
        "p15f",
        "p15g",
        "p15h",
        "p15i",
    ]

    df = df.drop(pfc_topics, axis=1, inplace=False)

    class_problems = ["p26a", "p26b", "p26c", "p26d"]

    df = df.drop(class_problems, axis=1, inplace=False)

    # drop columns with too many missing values
    cols_to_drop = [
        "p27a",
        "p16h",
        "p19",
        "p23i",
        "p32e",
        "p41d",
        "p41e",
        "p41f",
        "p41j",
        "p299d",
        "p331j",
    ]
    cols_to_drop = [
        x for x in cols_to_drop if x not in pfc_topics and x not in class_problems
    ]
    df = df.drop(cols_to_drop, axis=1, inplace=False)

    # drop columns due to functional dependencies
    cols_to_drop = [
        "p12a",
        "p12c",
        "p13b",
        "p16d",
        "p16e",
        "p16b",
        "p16f",
        "p18c",
        "p18b",
        "p22b",
        "p22c",
        "p32d",
        "p32a",
        "p32c",
        "p34f",
        "p34e",
        "p34c",
        "p34a",
        "p34g",
        "p311h",
        "p311f",
        "p311g",
        "p331c",
        "p331b",
        "p331a",
    ]

    df = df.drop(cols_to_drop, axis=1, inplace=False)
    # aggregate features row-wise using mean
    new_features = aggregate_features(df, agg_mean, aggregation_func=custom_mean)
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    df = df.drop(
        df.columns[features_to_drop_after_aggregation(df, agg_mean)],
        axis=1,
        inplace=False,
    )

    # repeat with binary features that are not important taken one by one
    # features are aggregated through a custom sum that skips NaNs
    new_features = aggregate_features(df, agg_sum, aggregation_func=custom_sum)
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    df = df.drop(
        df.columns[features_to_drop_after_aggregation(df, agg_sum)],
        axis=1,
        inplace=False,
    )

    # repeat with binary features that are important taken one by one
    # features are aggregated through a custom function that returns a unique integer for each combination of values
    new_features = aggregate_features(
        df, agg_custom_binary, aggregation_func=custom_binary_agg
    )
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    df = df.drop(
        df.columns[features_to_drop_after_aggregation(df, agg_custom_binary)],
        axis=1,
        inplace=False,
    )

    # update aggregation map in case features have been dropped
    agg_mix_new = {}
    for k in agg_mix.keys():
        temp = {}
        for feat, col_names in agg_mix[k].items():
            temp[feat] = [x for x in col_names if x in df.columns]
        agg_mix_new[k] = temp

    # maximum degree of agreement
    max_deg = 4
    to_lambdate = {
        "extent_of_satisfaction_job_and_school": lambda x: get_good_bad_agg(
            x,
            group="extent_of_satisfaction_job_and_school",
            aggregation_map=agg_mix_new,
            max_degree_of_agreement=max_deg,
        ),
        "extent_of_results_satisfaction": lambda x: get_good_bad_agg(
            x,
            group="extent_of_results_satisfaction",
            aggregation_map=agg_mix_new,
            max_degree_of_agreement=max_deg,
        ),
    }

    new_features = aggregate_mixed_features(df, agg_mix_new, to_lambdate)
    new_features_df = pd.concat([new_features[k] for k in new_features.keys()], axis=1)
    new_features_df.columns = new_features.keys()
    df = pd.concat([df, new_features_df], axis=1)

    # drop features after aggregating
    df = df.drop(
        df.columns[mixed_features_to_drop(df, agg_mix_new)], axis=1, inplace=False
    )

    # rename features
    df = df.rename(columns=to_rename)
    # df.to_csv(
    #     os.path.join(DATA_SPLIT_PATH, "teacher_questionnaire_preprocessed.csv"),
    #     index=False,
    # )

    df["gender"] = df["gender"].apply(
        lambda x: "MALE" if x == 1 else ("FEMALE" if x == 2 else np.nan)
    )

    for col in ["has_taught_same_group_last_two_years"]:
        df[col] = df[col].apply(lambda x: 0 if x == 2 else x).astype("boolean")

    df["behaviour_problems_solution"] = df["behaviour_problems_solution"].apply(
        lambda x: (
            "PRINCIPAL"
            if x == 1
            else (
                "MANAGEMENT"
                if x == 2
                else (
                    "CLASSMATES" if x == 3 else ("INDIVIDUALLY" if x == 4 else np.nan)
                )
            )
        )
    )

    df.to_csv(os.path.join(DATA_PREPROC_PATH, "teacher_questionnaire.csv"))

    return df


if __name__ == "__main__":
    df = preprocess_teacher_questionnaire()
    print(f"Done! Number of columns: {df.shape[1]}")
