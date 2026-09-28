import os
import pandas as pd
import matplotlib.pyplot as plt


RESULT_FILE = "results/dynamic_experiment_results.csv"
CHART_DIRECTORY = "results/charts"


def load_results():

    if not os.path.exists(RESULT_FILE):
        raise FileNotFoundError(
            f"Result file not found: {RESULT_FILE}"
        )

    df = pd.read_csv(RESULT_FILE)

    # Normalize strategy names
    df["strategy"] = (
        df["strategy"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Normalize workload names
    df["workload"] = (
        df["workload"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


def create_chart_directory():

    os.makedirs(
        CHART_DIRECTORY,
        exist_ok=True
    )


def get_strategy_data(df, strategy):

    data = df[
        df["strategy"] == strategy.lower()
    ].copy()

    return data


def add_value_labels(
    x,
    y,
    values,
    decimals=2,
    suffix=""
):

    for xi, yi, value in zip(
        x,
        y,
        values
    ):

        if pd.isna(value):
            continue

        if decimals == 0:

            label = (
                f"{int(value)}"
                f"{suffix}"
            )

        else:

            label = (
                f"{value:.{decimals}f}"
                f"{suffix}"
            )

        plt.annotate(
            label,
            (xi, yi),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=9
        )


def save_power_comparison(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    x_positions = range(len(workload_order))

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "after_power_watts"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=0,
            suffix=" W"
        )

    plt.xticks(
        list(x_positions),
        workload_order
    )

    plt.title(
        "Power Consumption: Reactive vs Predictive",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "Power Consumption (Watts)",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "01_power_comparison.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_energy_saving(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "energy_saving_percentage"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=2,
            suffix="%"
        )

    plt.xticks(
        range(4),
        workload_order
    )

    plt.title(
        "Energy Saving Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "Energy Saving (%)",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "02_energy_saving.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_carbon_saving(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "carbon_saved_kg"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=3,
            suffix=" kg"
        )

    plt.xticks(
        range(4),
        workload_order
    )

    plt.title(
        "Carbon Reduction Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "Carbon Saved (kg CO2)",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "03_carbon_reduction.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_cost_saving(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "cost_saved"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=2,
            suffix=" Rs"
        )

    plt.xticks(
        range(4),
        workload_order
    )

    plt.title(
        "Electricity Cost Saving Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "Cost Saved (Rs)",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "04_cost_saving.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_rejected_vms(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "rejected_vms"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=0
        )

    plt.xticks(
        range(4),
        workload_order
    )

    plt.title(
        "Rejected VM Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "Rejected VMs",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "05_rejected_vms.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_sla_violations(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "sla_violations"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=0
        )

    plt.xticks(
        range(4),
        workload_order
    )

    plt.title(
        "SLA Violation Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "SLA Violations",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "06_sla_violations.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_active_hosts(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "active_hosts"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=0
        )

    plt.xticks(
        range(4),
        workload_order
    )

    plt.title(
        "Active Hosts Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "Active Hosts",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "07_active_hosts.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_vm_migrations(df):

    plt.figure(figsize=(11, 7))

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    for strategy in [
        "reactive",
        "predictive"
    ]:

        data = get_strategy_data(
            df,
            strategy
        )

        data["workload"] = pd.Categorical(
            data["workload"],
            categories=workload_order,
            ordered=True
        )

        data = data.sort_values(
            "workload"
        )

        values = data[
            "vm_migrations"
        ].tolist()

        x = list(range(len(values)))

        plt.plot(
            x,
            values,
            marker="o",
            linewidth=2.5,
            markersize=8,
            label=strategy.capitalize()
        )

        add_value_labels(
            x,
            values,
            values,
            decimals=0
        )

    plt.xticks(
        range(4),
        workload_order
    )

    plt.title(
        "VM Migration Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "VM Migrations",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "08_vm_migrations.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def save_summary_chart(df):

    workload_order = [
        "LOW",
        "MEDIUM",
        "HIGH",
        "PEAK"
    ]

    reactive = (
        df[df["strategy"] == "reactive"]
        .set_index("workload")
        .reindex(workload_order)
    )

    predictive = (
        df[df["strategy"] == "predictive"]
        .set_index("workload")
        .reindex(workload_order)
    )

    reactive_values = (
        reactive[
            "after_power_watts"
        ]
        .astype(float)
        .values
    )

    predictive_values = (
        predictive[
            "after_power_watts"
        ]
        .astype(float)
        .values
    )

    x = range(
        len(workload_order)
    )

    width = 0.35

    plt.figure(
        figsize=(12, 7)
    )

    bars1 = plt.bar(
        [
            i - width / 2
            for i in x
        ],
        reactive_values,
        width=width,
        label="Reactive"
    )

    bars2 = plt.bar(
        [
            i + width / 2
            for i in x
        ],
        predictive_values,
        width=width,
        label="Predictive"
    )

    for bar in bars1:

        value = bar.get_height()

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            value + 15,
            f"{value:.0f} W",
            ha="center",
            fontsize=9
        )

    for bar in bars2:

        value = bar.get_height()

        plt.text(
            bar.get_x()
            + bar.get_width() / 2,
            value + 15,
            f"{value:.0f} W",
            ha="center",
            fontsize=9
        )

    plt.xticks(
        list(x),
        workload_order
    )

    plt.title(
        "Overall Power Consumption Comparison",
        fontsize=15,
        fontweight="bold"
    )

    plt.xlabel(
        "Workload Level",
        fontsize=12
    )

    plt.ylabel(
        "Power Consumption (W)",
        fontsize=12
    )

    plt.legend(
        fontsize=11
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIRECTORY,
            "09_overall_power_bar_chart.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def main():

    print("\nLoading experiment results...")

    df = load_results()

    print("Rows:", len(df))

    print(
        "\nStrategy values found in CSV:"
    )

    print(
        df["strategy"]
        .value_counts()
        .to_string()
    )

    print(
        "\nWorkload values found in CSV:"
    )

    print(
        df["workload"]
        .value_counts()
        .to_string()
    )

    reactive_count = len(
        get_strategy_data(
            df,
            "reactive"
        )
    )

    predictive_count = len(
        get_strategy_data(
            df,
            "predictive"
        )
    )

    print(
        f"\nReactive rows: {reactive_count}"
    )

    print(
        f"Predictive rows: {predictive_count}"
    )

    if reactive_count == 0:
        raise ValueError(
            "No Reactive rows found in the CSV."
        )

    if predictive_count == 0:
        raise ValueError(
            "No Predictive rows found in the CSV."
        )

    create_chart_directory()

    print(
        "\nGenerating research charts..."
    )

    save_power_comparison(df)
    print("1. Power comparison created.")

    save_energy_saving(df)
    print("2. Energy saving comparison created.")

    save_carbon_saving(df)
    print("3. Carbon reduction comparison created.")

    save_cost_saving(df)
    print("4. Cost saving comparison created.")

    save_rejected_vms(df)
    print("5. Rejected VM comparison created.")

    save_sla_violations(df)
    print("6. SLA violation comparison created.")

    save_active_hosts(df)
    print("7. Active host comparison created.")

    save_vm_migrations(df)
    print("8. VM migration comparison created.")

    save_summary_chart(df)
    print("9. Overall power summary created.")

    print(
        "\n=============================================="
    )

    print(
        "RESEARCH CHARTS GENERATED SUCCESSFULLY"
    )

    print(
        "=============================================="
    )

    print(
        f"Location: {CHART_DIRECTORY}"
    )

    print(
        "Total charts: 9"
    )


if __name__ == "__main__":
    main()