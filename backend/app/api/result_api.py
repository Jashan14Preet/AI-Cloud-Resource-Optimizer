import os
import json
import pandas as pd

from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/results",
    tags=["Results"]
)


RESULT_FILE = "results/dynamic_experiment_results.csv"


@router.get("/")
def get_results():

    if not os.path.exists(RESULT_FILE):
        raise HTTPException(
            status_code=404,
            detail="Experiment results file not found."
        )

    df = pd.read_csv(RESULT_FILE)

    # Convert NaN values to JSON-compatible null values
    json_data = json.loads(
        df.to_json(
            orient="records"
        )
    )

    return {
        "total_results": len(json_data),
        "results": json_data
    }


@router.get("/summary")
def get_results_summary():

    if not os.path.exists(RESULT_FILE):
        raise HTTPException(
            status_code=404,
            detail="Experiment results file not found."
        )

    df = pd.read_csv(RESULT_FILE)

    reactive = df[
        df["strategy"].str.lower() == "reactive"
    ]

    predictive = df[
        df["strategy"].str.lower() == "predictive"
    ]

    return {
        "total_experiments": len(df),

        "reactive_experiments": len(
            reactive
        ),

        "predictive_experiments": len(
            predictive
        ),

        "reactive": {
            "average_power_watts": round(
                reactive[
                    "after_power_watts"
                ].mean(),
                2
            ),

            "average_energy_saving_percentage": round(
                reactive[
                    "energy_saving_percentage"
                ].mean(),
                2
            ),

            "total_rejected_vms": int(
                reactive[
                    "rejected_vms"
                ].sum()
            ),

            "total_sla_violations": int(
                reactive[
                    "sla_violations"
                ].sum()
            )
        },

        "predictive": {
            "average_power_watts": round(
                predictive[
                    "after_power_watts"
                ].mean(),
                2
            ),

            "average_energy_saving_percentage": round(
                predictive[
                    "energy_saving_percentage"
                ].mean(),
                2
            ),

            "total_rejected_vms": int(
                predictive[
                    "rejected_vms"
                ].sum()
            ),

            "total_sla_violations": int(
                predictive[
                    "sla_violations"
                ].sum()
            )
        }
    }