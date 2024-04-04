import pandas as pd
import numpy as np

def find_first_valid_index(df_columns, feature_interval, left_idx=None, right_idx=None):
    if not left_idx and not right_idx:
        raise ValueError("at least one of the two indices must not be None")
    else:
        if not left_idx:
            return search_left_to_right(df_columns, feature_interval, right_idx)
        if not right_idx:
            return search_right_to_left(df_columns, feature_interval, left_idx)
        
def search_left_to_right(df_columns, feature_interval, right_idx):
    i = 1
    stop = False
    new_left_idx = None
    while not stop:
        new_left_idx = list(df_columns).index(feature_interval[i])
        if df_columns[new_left_idx] or new_left_idx == right_idx:
            stop = True
        i += 1
    return new_left_idx

def search_right_to_left(df_columns, feature_interval, left_idx):
    i = 1
    stop = False
    new_right_idx = None
    while not stop:
        new_right_idx = list(df_columns).index(feature_interval[-i-1])
        if df_columns[new_right_idx] or new_right_idx == left_idx:
            stop = True
        i += 1
    return new_right_idx    

def get_feature_interval_indexes(df: pd.DataFrame, feature_intervals: dict):
    feature_interval_idxs = {}
    for k in feature_intervals.keys():
        if feature_intervals[k][0] in df.columns:
            # first element of list exists
            left_idx = list(df.columns).index(feature_intervals[k][0])
            if feature_intervals[k][-1] in df.columns:
                # no columns have been dropped
                feature_interval_idxs[k] = [list(df.columns).index(x) for x in feature_intervals[k]]
            else:
                # only last element of list was dropped
                # find first not None column moving from right to left
                new_right_idx = find_first_valid_index(df.columns, feature_intervals[k], left_idx)
                idx = feature_intervals[k].index(df.columns[new_right_idx])
                feature_interval_idxs[k] = [list(df.columns).index(x) for x in feature_intervals[k][:idx+1]]
        else:
            # first element of list was dropped
            if feature_intervals[k][1] in df.columns:
                # last element of list exists
                right_idx = list(df.columns).index(feature_intervals[k][1])
                # find first not None column moving from left to right
                new_left_idx = find_first_valid_index(df.columns, feature_intervals[k], right_idx)
                idx = feature_intervals[k].index(df.columns[new_left_idx])
                feature_interval_idxs[k] = [list(df.columns).index(x) for x in feature_intervals[k][idx:]]
    return feature_interval_idxs

def aggregate_features(df: pd.DataFrame, feature_intervals: dict, aggregation_func: str, na_values_strategy: str):
    feature_interval_idxs = get_feature_interval_indexes(df, feature_intervals)
    aggregated_features = {}
    for k in feature_interval_idxs.keys():
        df_subset = df.iloc[:, feature_interval_idxs[k][0]:feature_interval_idxs[k][-1]+1]
        if na_values_strategy == "zeros":
            df_subset = df_subset.fillna(0)
        elif na_values_strategy == "mean":
            df_subset = df_subset.fillna(df_subset.mean())
        aggregated_features[k] = df_subset.agg(aggregation_func, axis=1)
    return aggregated_features

def features_to_drop_after_aggregation(df: pd.DataFrame, feature_intervals: dict):
    feature_interval_idxs = get_feature_interval_indexes(df, feature_intervals)
    features_to_drop = []
    for k in feature_interval_idxs.keys():
        features_to_drop += feature_interval_idxs[k]
    return features_to_drop

def features_with_too_many_nans(df: pd.DataFrame, nan_threshold: float):
    nan_percs = []
    for col in df.columns:
        nan_percs.append(df[col].isna().sum() / df.shape[0])
    return np.where(np.array(nan_percs) > nan_threshold)