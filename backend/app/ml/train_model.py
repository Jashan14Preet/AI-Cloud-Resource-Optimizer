import pandas as pd
import numpy as np
import os
import joblib


from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


FEATURE_COLUMNS = [
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "network_usage",
    "vm_count"
]

TARGET_COLUMNS = [
    "cpu_usage",
    "memory_usage",
    "disk_usage",
    "network_usage"
]


def prepare_dataset(file_path, horizon_minutes=10):
    """
    Prepare the dataset for ML training.

    Features:
        Current workload + previous workload values.

    Targets:
        Future CPU, memory, disk and network usage.
    """

    df = pd.read_csv(file_path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values("timestamp").reset_index(drop=True)

    # Create time features
    df["hour"] = df["timestamp"].dt.hour
    df["minute"] = df["timestamp"].dt.minute
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    # Create lag features
    for column in FEATURE_COLUMNS:

        for lag in range(1, 6):

            df[f"{column}_lag_{lag}"] = df[column].shift(lag)

    # Create future targets
    for column in TARGET_COLUMNS:

        df[f"{column}_future_{horizon_minutes}"] = (
            df[column].shift(-horizon_minutes)
        )

    # Remove rows with missing values caused by lagging/future shifting
    df = df.dropna().reset_index(drop=True)

    # Feature columns used by the model
    feature_columns = (
        FEATURE_COLUMNS
        + ["hour", "minute", "day_of_week"]
        + [
            f"{column}_lag_{lag}"
            for column in FEATURE_COLUMNS
            for lag in range(1, 6)
        ]
    )

    # Target columns
    target_columns = [
        f"{column}_future_{horizon_minutes}"
        for column in TARGET_COLUMNS
    ]

    X = df[feature_columns]
    y = df[target_columns]

    return X, y


def train_random_forest(X_train, y_train):
    """
    Train a Random Forest regression model.
    """

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained model using MAE, RMSE and R².
    """

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    return predictions, mae, rmse, r2


if __name__ == "__main__":

    file_path = "data/synthetic_workload.csv"

    print("\nPreparing dataset...")

    X, y = prepare_dataset(
        file_path,
        horizon_minutes=10
    )

    print("Feature shape:", X.shape)
    print("Target shape:", y.shape)

    # Chronological train/test split
    # First 80% = training
    # Last 20% = testing
    split_index = int(len(X) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    print("\nTraining samples:", len(X_train))
    print("Testing samples:", len(X_test))

    print("\nTraining Random Forest...")

    model = train_random_forest(
        X_train,
        y_train
    )

    print("Training completed!")

    print("\nEvaluating model...")

    predictions, mae, rmse, r2 = evaluate_model(
        model,
        X_test,
        y_test
    )

    print("\n===== MODEL RESULTS =====")

    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

    print("\nSample predictions:")

    comparison = pd.DataFrame({
        "Actual_CPU": y_test.iloc[:5]["cpu_usage_future_10"].values,
        "Predicted_CPU": predictions[:5, 0],

        "Actual_Memory": y_test.iloc[:5]["memory_usage_future_10"].values,
        "Predicted_Memory": predictions[:5, 1]
    })

    print(comparison)

        # Create models directory if it does not exist
    os.makedirs("models", exist_ok=True)

    # Save trained model
    model_path = "models/random_forest_10min.pkl"

    joblib.dump(model, model_path)

    print(f"\nModel saved successfully!")
    print(f"Model path: {model_path}")