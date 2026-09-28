import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


FEATURE_COLUMNS = [
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "network_usage",
    "vm_count"
]


def load_workload(file_path):
    """
    Load workload data from CSV.
    """

    df = pd.read_csv(file_path)

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort chronologically
    df = df.sort_values("timestamp").reset_index(drop=True)

    return df


def check_missing_values(df):
    """
    Check the number of missing values in each column.
    """

    missing_values = df.isnull().sum()

    return missing_values


def handle_missing_values(df):
    """
    Handle missing numerical values using interpolation
    followed by forward/backward filling.
    """

    df = df.copy()

    for column in FEATURE_COLUMNS:

        df[column] = df[column].interpolate()

        df[column] = df[column].ffill()

        df[column] = df[column].bfill()

    return df


def add_time_features(df):
    """
    Add useful time-based features.
    """

    df = df.copy()

    df["hour"] = df["timestamp"].dt.hour
    df["minute"] = df["timestamp"].dt.minute
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    return df


def add_lag_features(df, lag_steps=5):
    """
    Create previous workload values.

    Example:
    cpu_usage_lag_1 = CPU usage one time step earlier.
    """

    df = df.copy()

    for column in FEATURE_COLUMNS:

        for lag in range(1, lag_steps + 1):

            df[f"{column}_lag_{lag}"] = df[column].shift(lag)

    return df


def scale_features(df):
    """
    Scale numerical workload features between 0 and 1.
    """

    df = df.copy()

    scaler = MinMaxScaler()

    df[FEATURE_COLUMNS] = scaler.fit_transform(
        df[FEATURE_COLUMNS]
    )

    return df, scaler


def preprocess_workload(file_path):
    """
    Complete preprocessing pipeline.
    """

    df = load_workload(file_path)

    print("\nOriginal dataset:")
    print(df.head())

    print("\nMissing values:")
    print(check_missing_values(df))

    df = handle_missing_values(df)

    df = add_time_features(df)

    df = add_lag_features(df)

    # Remove rows created by lagging
    df = df.dropna().reset_index(drop=True)

    return df


if __name__ == "__main__":

    file_path = "data/synthetic_workload.csv"

    processed_data = preprocess_workload(file_path)

    print("\nProcessed dataset:")
    print(processed_data.head())

    print("\nProcessed shape:")
    print(processed_data.shape)

    print("\nColumns:")
    print(processed_data.columns.tolist())