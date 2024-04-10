from pathlib import Path
from typing import Callable
import pandas as pd
from matplotlib import pyplot as plt

PATH = Path(__file__).parents[0]


def sum_merge_strategy(df: pd.DataFrame, axis: int) -> pd.Series:
    """
    Merge the columns of a DataFrame by summing the values.
    :param df: DataFrame to merge the columns
    :param axis: axis to sum the values
    :return: Series with the sum of the values
    """
    return df.sum(axis=axis)


def mean_merge_strategy(df: pd.DataFrame, axis: int) -> pd.Series:
    """
    Merge the columns of a DataFrame by calculating the mean of the values.
    :param df: DataFrame to merge the columns
    :param axis: axis to calculate the mean
    :return: Series with the mean of the values
    """
    return df.mean(axis=axis)


def _constant_nan_strategy(merged_column: pd.Series, constant: int) -> pd.Series:
    """
    Handle NaN values by replacing them with a constant value.
    :param merged_column: Series with the merged column
    :param constant: constant value to replace the NaN values
    :return: Series with the NaN values replaced by the constant
    """
    return merged_column.fillna(constant)


def zero_nan_strategy(merged_column: pd.Series) -> pd.Series:
    """
    Handle NaN values by replacing them with 0.
    :param merged_column: Series with the merged column
    :return: Series with the NaN values replaced by 0
    """
    return _constant_nan_strategy(merged_column, 0)


def mean_nan_strategy(merged_column: pd.Series) -> pd.Series:
    """
    Handle NaN values by replacing them with the mean of the column.
    :param merged_column: Series with the merged column
    :return: Series with the NaN values replaced by the mean of the column
    """
    return merged_column.fillna(merged_column.mean())


def mode_nan_strategy(merged_column: pd.Series) -> pd.Series:
    """
    Handle NaN values by replacing them with the mode of the column.
    :param merged_column: Series with the merged column
    :return: Series with the NaN values replaced by the mode of the column
    """
    return merged_column.fillna(merged_column.mode()[0])


def merge_columns(df: pd.DataFrame,
                  column_names: list[str],
                  merge_strategy: Callable,
                  nan_strategies: Callable,
                  new_name: str) -> pd.DataFrame:
    """
    Merge the columns of a DataFrame into a single column.
    :param df: DataFrame to merge the columns
    :param column_names: list of column names to merge
    :param merge_strategy: function to merge the columns
    :param nan_strategies: function to handle NaN values
    :param new_name: name of the new column
    :return: DataFrame with the columns merged
    """
    merged_column = merge_strategy(df[column_names], axis=1)
    # Handle NaN values
    merged_column = nan_strategies(merged_column)
    # Drop the columns that were merged
    df.drop(column_names, axis=1, inplace=True)
    df[new_name] = merged_column
    # Sort the columns
    df = df.reindex(sorted(df.columns), axis=1)
    return df


def histogram_plot(df: pd.DataFrame, column_name: str) -> None:
    """
    Plot a histogram of the values of a column in a DataFrame.
    Use the number of unique values to determine the number of bins.
    :param df: DataFrame with the column
    :param column_name: name of the column
    """
    plt.hist(df[column_name], bins=df[column_name].nunique())
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {column_name}')
    plt.show()
