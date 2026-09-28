import pandas as pd


TARGET_COLUMNS = [
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "network_usage"
]


def create_future_targets(df, horizon_minutes=10):
    """
    Create future workload targets.

    Example:
        If horizon_minutes = 10,
        the target at time T is the workload
        observed 10 minutes after T.
    """

    df = df.copy()

    for column in TARGET_COLUMNS:
        df[f"{column}_future_{horizon_minutes}"] = (
            df[column].shift(-horizon_minutes)
        )

    # Remove rows where future values do not exist
    df = df.dropna().reset_index(drop=True)

    return df


def create_all_prediction_targets(df):
    """
    Create targets for 10, 20 and 30 minute horizons.
    """

    results = {}

    for horizon in [10, 20, 30]:
        results[horizon] = create_future_targets(
            df,
            horizon_minutes=horizon
        )

    return results


if __name__ == "__main__":

    file_path = "data/synthetic_workload.csv"

    df = pd.read_csv(file_path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values("timestamp").reset_index(drop=True)

    print("\nOriginal dataset:")
    print(df.shape)

    prediction_datasets = create_all_prediction_targets(df)

    for horizon, dataset in prediction_datasets.items():

        print(f"\nPrediction horizon: {horizon} minutes")

        print("Shape:", dataset.shape)

        print("\nSample:")

        print(
            dataset[
                [
                    "timestamp",
                    "cpu_usage",
                    f"cpu_usage_future_{horizon}",
                    "memory_usage",
                    f"memory_usage_future_{horizon}"
                ]
            ].head()
        )