import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_workload(
    duration_minutes=1440,
    interval_seconds=60,
    random_seed=42
):
    """
    Generate a realistic synthetic cloud workload dataset.

    Parameters:
        duration_minutes: Total duration of the workload.
        interval_seconds: Time between measurements.
        random_seed: Seed for reproducible results.

    Returns:
        pandas DataFrame containing workload metrics.
    """

    np.random.seed(random_seed)

    total_points = int((duration_minutes * 60) / interval_seconds)

    timestamps = [
        datetime.now().replace(second=0, microsecond=0)
        + timedelta(seconds=i * interval_seconds)
        for i in range(total_points)
    ]

    time_index = np.arange(total_points)

    # ---------------------------------------------------------
    # 1. Daily workload pattern
    # ---------------------------------------------------------

    daily_pattern = (
        50
        + 20 * np.sin(2 * np.pi * time_index / 1440)
    )

    # ---------------------------------------------------------
    # 2. Short-term workload variation
    # ---------------------------------------------------------

    short_term_pattern = (
        10 * np.sin(2 * np.pi * time_index / 180)
    )

    # ---------------------------------------------------------
    # 3. Random workload variation
    # ---------------------------------------------------------

    noise = np.random.normal(0, 5, total_points)

    cpu_usage = (
        daily_pattern
        + short_term_pattern
        + noise
    )

    # Keep CPU between 5% and 95%
    cpu_usage = np.clip(cpu_usage, 5, 95)

    # ---------------------------------------------------------
    # 4. Memory usage
    # ---------------------------------------------------------

    memory_noise = np.random.normal(0, 3, total_points)

    memory_usage = (
        cpu_usage * 0.75
        + 10
        + memory_noise
    )

    memory_usage = np.clip(memory_usage, 10, 95)

    # ---------------------------------------------------------
    # 5. Disk usage
    # ---------------------------------------------------------

    disk_noise = np.random.normal(0, 2, total_points)

    disk_usage = (
        30
        + 0.25 * cpu_usage
        + disk_noise
    )

    disk_usage = np.clip(disk_usage, 5, 90)

    # ---------------------------------------------------------
    # 6. Network usage
    # ---------------------------------------------------------

    network_noise = np.random.normal(0, 4, total_points)

    network_usage = (
        20
        + 0.5 * cpu_usage
        + network_noise
    )

    network_usage = np.clip(network_usage, 5, 100)

    # ---------------------------------------------------------
    # 7. Number of VMs
    # ---------------------------------------------------------

    vm_count = (
        20
        + (cpu_usage / 10).astype(int)
        + np.random.randint(-2, 3, total_points)
    )

    vm_count = np.clip(vm_count, 5, 50)

    # ---------------------------------------------------------
    # 8. Build DataFrame
    # ---------------------------------------------------------

    workload = pd.DataFrame({
        "timestamp": timestamps,
        "cpu_usage": np.round(cpu_usage, 2),
        "memory_usage": np.round(memory_usage, 2),
        "disk_usage": np.round(disk_usage, 2),
        "network_usage": np.round(network_usage, 2),
        "vm_count": vm_count
    })

    return workload


if __name__ == "__main__":

    workload = generate_workload()

    print("\nGenerated workload:")
    print(workload.head(10))

    print("\nDataset shape:")
    print(workload.shape)

    print("\nDataset statistics:")
    print(workload.describe())