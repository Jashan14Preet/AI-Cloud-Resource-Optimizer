from app.services.reactive_allocator import ReactiveAllocator
from app.services.predictive_allocator import PredictiveAllocator
from app.services.sla_service import SLAService
from app.services.sustainability_service import SustainabilityService
from app.services.result_service import ResultService
from app.simulation.cloud import VM


class DynamicExperiment:

    def __init__(self):

        self.sla_service = SLAService()
        self.sustainability_service = SustainabilityService()
        self.result_service = ResultService()

    # =========================================================
    # CREATE VMS
    # =========================================================

    def create_vms(self, number_of_vms):

        vms = []

        for vm_id in range(1, number_of_vms + 1):

            vm = VM(
                vm_id=vm_id,
                cpu_demand=10,
                memory_demand=15
            )

            vms.append(vm)

        return vms

    # =========================================================
    # SUSTAINABILITY CALCULATION
    # =========================================================

    def calculate_sustainability(self, power_watts):

        return self.sustainability_service.calculate_sustainability(
            power_watts=power_watts,
            duration_hours=1
        )

    # =========================================================
    # RUN REACTIVE STRATEGY
    # =========================================================

    def run_reactive_strategy(self, number_of_vms):

        vms = self.create_vms(number_of_vms)

        reactive = ReactiveAllocator(
            number_of_hosts=10
        )

        # Allocate workload
        reactive.allocate_workload(vms)

        # State before energy optimization
        before = reactive.simulator.get_summary()

        before_sustainability = self.calculate_sustainability(
            before["power_watts"]
        )

        # Perform energy optimization
        optimization = reactive.optimize_energy()

        # State after energy optimization
        after = reactive.simulator.get_summary()

        after_sustainability = self.calculate_sustainability(
            after["power_watts"]
        )

        results = reactive.get_results()

        # Calculate savings
        power_saved = (
            before["power_watts"]
            - after["power_watts"]
        )

        energy_saved = (
            before_sustainability["energy_kwh"]
            - after_sustainability["energy_kwh"]
        )

        carbon_saved = (
            before_sustainability["carbon_kg"]
            - after_sustainability["carbon_kg"]
        )

        cost_saved = (
            before_sustainability["electricity_cost"]
            - after_sustainability["electricity_cost"]
        )

        energy_saving_percentage = (
            (energy_saved / before_sustainability["energy_kwh"]) * 100
            if before_sustainability["energy_kwh"] > 0
            else 0
        )

        # SLA
        sla = self.sla_service.calculate_sla_violations(
            reactive.simulator,
            rejected_vms=results["rejected_vms"]
        )

        return {
            "before": before,
            "after": after,
            "optimization": optimization,
            "results": results,
            "before_sustainability": before_sustainability,
            "after_sustainability": after_sustainability,
            "savings": {
                "power_saved_watts": round(
                    power_saved, 2
                ),
                "energy_saved_kwh": round(
                    energy_saved, 4
                ),
                "energy_saving_percentage": round(
                    energy_saving_percentage, 2
                ),
                "carbon_saved_kg": round(
                    carbon_saved, 4
                ),
                "cost_saved": round(
                    cost_saved, 4
                )
            },
            "sla": sla
        }

    # =========================================================
    # RUN PREDICTIVE STRATEGY
    # =========================================================

    def run_predictive_strategy(self, number_of_vms):

        vms = self.create_vms(number_of_vms)

        predictive = PredictiveAllocator(
            number_of_hosts=10
        )

        # -----------------------------------------------------
        # Workload used by ML prediction model
        # -----------------------------------------------------

        workload = {

            "cpu_usage": min(
                40 + number_of_vms,
                90
            ),

            "memory_usage": min(
                40 + number_of_vms,
                90
            ),

            "disk_usage": 50,

            "network_usage": 50,

            "vm_count": number_of_vms,

            "hour": 12,

            "minute": 0,

            "day_of_week": 1,

            # CPU lags
            "cpu_usage_lag_1": 40,
            "cpu_usage_lag_2": 40,
            "cpu_usage_lag_3": 40,
            "cpu_usage_lag_4": 40,
            "cpu_usage_lag_5": 40,

            # Memory lags
            "memory_usage_lag_1": 40,
            "memory_usage_lag_2": 40,
            "memory_usage_lag_3": 40,
            "memory_usage_lag_4": 40,
            "memory_usage_lag_5": 40,

            # Disk lags
            "disk_usage_lag_1": 50,
            "disk_usage_lag_2": 50,
            "disk_usage_lag_3": 50,
            "disk_usage_lag_4": 50,
            "disk_usage_lag_5": 50,

            # Network lags
            "network_usage_lag_1": 50,
            "network_usage_lag_2": 50,
            "network_usage_lag_3": 50,
            "network_usage_lag_4": 50,
            "network_usage_lag_5": 50,

            # VM count lags
            "vm_count_lag_1": number_of_vms,
            "vm_count_lag_2": number_of_vms,
            "vm_count_lag_3": number_of_vms,
            "vm_count_lag_4": number_of_vms,
            "vm_count_lag_5": number_of_vms
        }

        # -----------------------------------------------------
        # Predict future workload and allocate resources
        # -----------------------------------------------------

        prediction_result = (
            predictive.allocate_based_on_prediction(
                workload,
                vms
            )
        )

        prediction = prediction_result["prediction"]

        # -----------------------------------------------------
        # State before energy optimization
        # -----------------------------------------------------

        before = predictive.simulator.get_summary()

        before_sustainability = self.calculate_sustainability(
            before["power_watts"]
        )

        # -----------------------------------------------------
        # Energy optimization
        # -----------------------------------------------------

        optimization = predictive.optimize_energy()

        # -----------------------------------------------------
        # State after energy optimization
        # -----------------------------------------------------

        after = predictive.simulator.get_summary()

        after_sustainability = self.calculate_sustainability(
            after["power_watts"]
        )

        results = predictive.get_results()

        # -----------------------------------------------------
        # Calculate savings
        # -----------------------------------------------------

        power_saved = (
            before["power_watts"]
            - after["power_watts"]
        )

        energy_saved = (
            before_sustainability["energy_kwh"]
            - after_sustainability["energy_kwh"]
        )

        carbon_saved = (
            before_sustainability["carbon_kg"]
            - after_sustainability["carbon_kg"]
        )

        cost_saved = (
            before_sustainability["electricity_cost"]
            - after_sustainability["electricity_cost"]
        )

        energy_saving_percentage = (
            (energy_saved / before_sustainability["energy_kwh"]) * 100
            if before_sustainability["energy_kwh"] > 0
            else 0
        )

        # -----------------------------------------------------
        # SLA
        # -----------------------------------------------------

        sla = self.sla_service.calculate_sla_violations(
            predictive.simulator,
            rejected_vms=results["rejected_vms"]
        )

        return {
            "prediction": prediction,
            "required_hosts": prediction_result["required_hosts"],
            "before": before,
            "after": after,
            "optimization": optimization,
            "results": results,
            "before_sustainability": before_sustainability,
            "after_sustainability": after_sustainability,
            "savings": {
                "power_saved_watts": round(
                    power_saved, 2
                ),
                "energy_saved_kwh": round(
                    energy_saved, 4
                ),
                "energy_saving_percentage": round(
                    energy_saving_percentage, 2
                ),
                "carbon_saved_kg": round(
                    carbon_saved, 4
                ),
                "cost_saved": round(
                    cost_saved, 4
                )
            },
            "sla": sla
        }

    # =========================================================
    # MAIN EXPERIMENT
    # =========================================================

    def run_experiment(self):

        workload_levels = {
            "LOW": 10,
            "MEDIUM": 20,
            "HIGH": 30,
            "PEAK": 40
        }

        experiment_results = []

        for level, number_of_vms in workload_levels.items():

            print("\n")
            print("==============================================")
            print(
                f"{level} WORKLOAD - {number_of_vms} VMs"
            )
            print("==============================================")

            # =================================================
            # REACTIVE
            # =================================================

            reactive_result = self.run_reactive_strategy(
                number_of_vms
            )

            print("\n----- REACTIVE -----")

            print(
                "Before Power:",
                reactive_result["before"]["power_watts"],
                "W"
            )

            print(
                "After Power:",
                reactive_result["after"]["power_watts"],
                "W"
            )

            print(
                "Powered-on Hosts:",
                reactive_result["after"]["powered_on_hosts"]
            )

            print(
                "Active Hosts:",
                reactive_result["after"]["active_hosts"]
            )

            print(
                "Rejected VMs:",
                reactive_result["results"]["rejected_vms"]
            )

            print(
                "VM Migrations:",
                reactive_result["results"]["vm_migrations"]
            )

            print(
                "Energy Saved:",
                reactive_result["savings"]["energy_saved_kwh"],
                "kWh"
            )

            print(
                "Carbon Saved:",
                reactive_result["savings"]["carbon_saved_kg"],
                "kg"
            )

            print(
                "Cost Saved:",
                reactive_result["savings"]["cost_saved"]
            )

            print(
                "Energy Saving:",
                reactive_result["savings"][
                    "energy_saving_percentage"
                ],
                "%"
            )

            print(
                "SLA:",
                reactive_result["sla"]["sla_status"]
            )

            print(
                "SLA Violations:",
                reactive_result["sla"][
                    "total_sla_violations"
                ]
            )

            # -------------------------------------------------
            # Save Reactive Result
            # -------------------------------------------------

            reactive_row = {

                "workload": level,

                "vm_count": number_of_vms,

                "strategy": "Reactive",

                "predicted_cpu": None,

                "predicted_memory": None,

                "required_hosts": None,

                "before_power_watts":
                    reactive_result["before"]["power_watts"],

                "after_power_watts":
                    reactive_result["after"]["power_watts"],

                "powered_on_hosts":
                    reactive_result["after"][
                        "powered_on_hosts"
                    ],

                "active_hosts":
                    reactive_result["after"][
                        "active_hosts"
                    ],

                "rejected_vms":
                    reactive_result["results"][
                        "rejected_vms"
                    ],

                "vm_migrations":
                    reactive_result["results"][
                        "vm_migrations"
                    ],

                "energy_saved_kwh":
                    reactive_result["savings"][
                        "energy_saved_kwh"
                    ],

                "energy_saving_percentage":
                    reactive_result["savings"][
                        "energy_saving_percentage"
                    ],

                "carbon_saved_kg":
                    reactive_result["savings"][
                        "carbon_saved_kg"
                    ],

                "cost_saved":
                    reactive_result["savings"][
                        "cost_saved"
                    ],

                "sla_status":
                    reactive_result["sla"][
                        "sla_status"
                    ],

                "sla_violations":
                    reactive_result["sla"][
                        "total_sla_violations"
                    ]
            }

            experiment_results.append(
                reactive_row
            )

            # =================================================
            # PREDICTIVE
            # =================================================

            predictive_result = (
                self.run_predictive_strategy(
                    number_of_vms
                )
            )

            print("\n----- PREDICTIVE -----")

            print(
                "Predicted CPU:",
                predictive_result["prediction"][
                    "cpu_usage"
                ],
                "%"
            )

            print(
                "Predicted Memory:",
                predictive_result["prediction"][
                    "memory_usage"
                ],
                "%"
            )

            print(
                "Required Hosts:",
                predictive_result[
                    "required_hosts"
                ]
            )

            print(
                "Before Power:",
                predictive_result["before"][
                    "power_watts"
                ],
                "W"
            )

            print(
                "After Power:",
                predictive_result["after"][
                    "power_watts"
                ],
                "W"
            )

            print(
                "Powered-on Hosts:",
                predictive_result["after"][
                    "powered_on_hosts"
                ]
            )

            print(
                "Active Hosts:",
                predictive_result["after"][
                    "active_hosts"
                ]
            )

            print(
                "Rejected VMs:",
                predictive_result["results"][
                    "rejected_vms"
                ]
            )

            print(
                "VM Migrations:",
                predictive_result["results"][
                    "vm_migrations"
                ]
            )

            print(
                "Energy Saved:",
                predictive_result["savings"][
                    "energy_saved_kwh"
                ],
                "kWh"
            )

            print(
                "Carbon Saved:",
                predictive_result["savings"][
                    "carbon_saved_kg"
                ],
                "kg"
            )

            print(
                "Cost Saved:",
                predictive_result["savings"][
                    "cost_saved"
                ]
            )

            print(
                "Energy Saving:",
                predictive_result["savings"][
                    "energy_saving_percentage"
                ],
                "%"
            )

            print(
                "SLA:",
                predictive_result["sla"][
                    "sla_status"
                ]
            )

            print(
                "SLA Violations:",
                predictive_result["sla"][
                    "total_sla_violations"
                ]
            )

            # -------------------------------------------------
            # Save Predictive Result
            # -------------------------------------------------

            predictive_row = {

                "workload": level,

                "vm_count": number_of_vms,

                "strategy": "Predictive",

                "predicted_cpu":
                    predictive_result["prediction"][
                        "cpu_usage"
                    ],

                "predicted_memory":
                    predictive_result["prediction"][
                        "memory_usage"
                    ],

                "required_hosts":
                    predictive_result[
                        "required_hosts"
                    ],

                "before_power_watts":
                    predictive_result["before"][
                        "power_watts"
                    ],

                "after_power_watts":
                    predictive_result["after"][
                        "power_watts"
                    ],

                "powered_on_hosts":
                    predictive_result["after"][
                        "powered_on_hosts"
                    ],

                "active_hosts":
                    predictive_result["after"][
                        "active_hosts"
                    ],

                "rejected_vms":
                    predictive_result["results"][
                        "rejected_vms"
                    ],

                "vm_migrations":
                    predictive_result["results"][
                        "vm_migrations"
                    ],

                "energy_saved_kwh":
                    predictive_result["savings"][
                        "energy_saved_kwh"
                    ],

                "energy_saving_percentage":
                    predictive_result["savings"][
                        "energy_saving_percentage"
                    ],

                "carbon_saved_kg":
                    predictive_result["savings"][
                        "carbon_saved_kg"
                    ],

                "cost_saved":
                    predictive_result["savings"][
                        "cost_saved"
                    ],

                "sla_status":
                    predictive_result["sla"][
                        "sla_status"
                    ],

                "sla_violations":
                    predictive_result["sla"][
                        "total_sla_violations"
                    ]
            }

            experiment_results.append(
                predictive_row
            )

        # =====================================================
        # SAVE ALL RESULTS
        # =====================================================

        file_path = self.result_service.save_dynamic_results(
            experiment_results
        )

        print("\n")
        print("==============================================")
        print("ALL EXPERIMENT RESULTS SAVED")
        print("==============================================")
        print(
            f"File: {file_path}"
        )

        print(
            f"Total experiment rows: "
            f"{len(experiment_results)}"
        )

        return experiment_results


# =============================================================
# RUN PROGRAM
# =============================================================

if __name__ == "__main__":

    experiment = DynamicExperiment()

    experiment.run_experiment()