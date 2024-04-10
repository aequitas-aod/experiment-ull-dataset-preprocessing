import pandas as pd
import numpy as np  

def get_feature_list_indexes(df: pd.DataFrame, feature_lists: dict):
    feature_list_idxs = {}
    for k in feature_lists.keys():
        feature_list_idxs[k] = [list(df.columns).index(x) for x in feature_lists[k] if x in df.columns]
    return feature_list_idxs

def aggregate_features(df: pd.DataFrame, feature_lists: dict, aggregation_func, na_values_strategy: str = "skip"):
    feature_list_idxs = get_feature_list_indexes(df, feature_lists)
    aggregated_features = {}
    for k in feature_list_idxs.keys():
        if feature_list_idxs[k]:
            df_subset = df.iloc[:, feature_list_idxs[k][0]:feature_list_idxs[k][-1]+1]
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
    binary = [1 if x == 1 else 0 for x in series]
    return sum(val*(2**idx) for idx, val in enumerate(reversed(binary)))