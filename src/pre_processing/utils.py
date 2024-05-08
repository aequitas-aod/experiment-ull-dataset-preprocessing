import pandas as pd
import numpy as np


def get_feature_list_indexes(df: pd.DataFrame, feature_lists: dict):
    feature_list_idxs = {}
    for k in feature_lists.keys():
        feature_list_idxs[k] = [
            list(df.columns).index(x) for x in feature_lists[k] if x in df.columns
        ]
    return feature_list_idxs


def aggregate_features(
    df: pd.DataFrame,
    feature_lists: dict,
    aggregation_func,
    na_values_strategy: str = "skip",
):
    feature_list_idxs = get_feature_list_indexes(df, feature_lists)
    aggregated_features = {}
    for k in feature_list_idxs.keys():
        if feature_list_idxs[k]:
            df_subset = df.iloc[:, feature_list_idxs[k]]
            if na_values_strategy == "zeros":
                df_subset = df_subset.fillna(0)
            elif na_values_strategy == "mean":
                df_subset = df_subset.fillna(df_subset.mean())
            aggregated_features[k] = df_subset.agg(aggregation_func, axis=1)
    return aggregated_features


def features_to_drop_after_aggregation(df: pd.DataFrame, feature_lists: dict):
    feature_list_idxs = get_feature_list_indexes(df, feature_lists)
    features_to_drop = []
    for k in feature_list_idxs.keys():
        features_to_drop += feature_list_idxs[k]
    return features_to_drop


def features_with_too_many_nans(df: pd.DataFrame, nan_threshold: float):
    nan_percs = []
    for col in df.columns:
        nan_percs.append(df[col].isna().sum() / df.shape[0])
    return np.where(np.array(nan_percs) > nan_threshold)


def custom_binary_agg(series):
    binary = [1 if x == 1 else 0 if x == 2 else x for x in series]
    return sum(val * (2**idx) for idx, val in enumerate(reversed(binary)))


def custom_sum(series):
    return series.sum(min_count=1)


def custom_mean(series):
    return series.mean(skipna=True)

def normalize_bad_column(m, r_min, r_max, t_min, t_max):
    if m not in range(1, 5):
        num = m - r_min
        den = r_max - r_min
        res = num/den * (t_max - t_min) + t_min
        return res
    else:
        return m
    
################### MIXED FEATURES ###################


def get_good_bad_agg(row, group, aggregation_map, max_degree_of_agreement):
    no_good = (
        len(aggregation_map["a"][group]) - row[aggregation_map["a"][group]].isna().sum()
    )
    no_bad = (
        len(aggregation_map["b"][group]) - row[aggregation_map["b"][group]].isna().sum()
    )

    if no_good == 0 and no_bad == 0:
        return np.nan
    else:
        return (
            row[aggregation_map["a"][group]].sum()
            + (
                (no_bad * (max_degree_of_agreement + 1))
                - row[aggregation_map["b"][group]].sum()
            )
        ) / (no_good + no_bad)


def aggregate_mixed_features(df, agg_map, lambda_agg):
    aggregated_features = {}
    for new_column, lambda_rule in lambda_agg.items():
        columns = []
        for k in agg_map.keys():
            for _, cols_group in agg_map[k].items():
                columns += cols_group
        aggregated_features[new_column] = df.loc[:, columns].agg(lambda_rule, axis=1)
    return aggregated_features


def mixed_features_to_drop(df, mixed_features):
    features_to_drop = []
    for k in mixed_features.keys():
        for _, feats in mixed_features[k].items():
            features_to_drop += feats
    return [list(df.columns).index(x) for x in features_to_drop if x in df.columns]
