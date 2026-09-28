from app.simulation.cloud import CloudSimulator, VM
from app.simulation.energy_optimizer import EnergyOptimizer
from app.services.sustainability_service import SustainabilityService


class ExperimentService:

    def __init__(self):
        self.sustainability = SustainabilityService()

    def run_experiment(self, number_of_vms=10, duration_hours=1):

        # -----------------------------------
        # 1. Create Cloud Simulator
        # -----------------------------------

        simulator = CloudSimulator(
            number_of_hosts=5
        )

        # -----------------------------------
        # 2. Create and Allocate VMs
        # -----------------------------------

        for vm_id in range(1, number_of_vms + 1):

            vm = VM(
                vm_id=vm_id,
                cpu_demand=10,
                memory_demand=15
            )

            simulator.allocate_vm(vm)

        # -----------------------------------
        # 3. Get Before Optimization Results
        # -----------------------------------

        before = simulator.get_summary()

        before_sustainability = (
            self.sustainability.calculate_sustainability(
                power_watts=before["power_watts"],
                duration_hours=duration_hours
            )
        )

        # -----------------------------------
        # 4. Perform Energy Optimization
        # -----------------------------------

        optimizer = EnergyOptimizer(simulator)

        optimization_results = optimizer.optimize()

        # -----------------------------------
        # 5. Get After Optimization Results
        # -----------------------------------

        after = simulator.get_summary()

        after_sustainability = (
            self.sustainability.calculate_sustainability(
                power_watts=after["power_watts"],
                duration_hours=duration_hours
            )
        )

        # -----------------------------------
        # 6. Calculate Savings
        # -----------------------------------

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

        # -----------------------------------
        # 7. Calculate Saving Percentages
        # -----------------------------------

        power_saving_percentage = (
            (power_saved / before["power_watts"]) * 100
            if before["power_watts"] > 0
            else 0
        )

        energy_saving_percentage = (
            (energy_saved / before_sustainability["energy_kwh"]) * 100
            if before_sustainability["energy_kwh"] > 0
            else 0
        )

        carbon_reduction_percentage = (
            (carbon_saved / before_sustainability["carbon_kg"]) * 100
            if before_sustainability["carbon_kg"] > 0
            else 0
        )

        cost_saving_percentage = (
            (cost_saved / before_sustainability["electricity_cost"]) * 100
            if before_sustainability["electricity_cost"] > 0
            else 0
        )

        # -----------------------------------
        # 8. Final Experiment Result
        # -----------------------------------

        return {

            "before": before,

            "after": after,

            "optimization": optimization_results,

            "before_sustainability": before_sustainability,

            "after_sustainability": after_sustainability,

            "savings": {

                "power_saved_watts": round(
                    power_saved, 2
                ),

                "power_saving_percentage": round(
                    power_saving_percentage, 2
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

                "carbon_reduction_percentage": round(
                    carbon_reduction_percentage, 2
                ),

                "cost_saved": round(
                    cost_saved, 4
                ),

                "cost_saving_percentage": round(
                    cost_saving_percentage, 2
                )
            }
        }


if __name__ == "__main__":

    experiment = ExperimentService()

    results = experiment.run_experiment(
        number_of_vms=10,
        duration_hours=1
    )

    print("\n===== BEFORE OPTIMIZATION =====")
    print(results["before"])

    print("\n===== OPTIMIZATION =====")
    print(results["optimization"])

    print("\n===== AFTER OPTIMIZATION =====")
    print(results["after"])

    print("\n===== BEFORE SUSTAINABILITY =====")
    print(results["before_sustainability"])

    print("\n===== AFTER SUSTAINABILITY =====")
    print(results["after_sustainability"])

    print("\n===== SAVINGS =====")
    print(results["savings"])