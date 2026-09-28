from app.simulation.cloud import CloudSimulator, VM
from app.services.prediction_service import PredictionService
from app.simulation.energy_optimizer import EnergyOptimizer


class PredictiveAllocator:

    def __init__(
        self,
        number_of_hosts=5,
        cpu_per_host=100,
        memory_per_host=100
    ):

        self.simulator = CloudSimulator(
            number_of_hosts=number_of_hosts,
            cpu_per_host=cpu_per_host,
            memory_per_host=memory_per_host
        )

        self.prediction_service = PredictionService()

        self.rejected_vms = 0
        self.vm_migrations = 0

    def predict_future_workload(self, workload):

        prediction = self.prediction_service.predict(workload)

        return prediction

    def calculate_required_hosts(
        self,
        predicted_cpu,
        predicted_memory,
        current_cpu,
        current_memory
    ):

        required_cpu = max(
            predicted_cpu,
            current_cpu
        )

        required_memory = max(
            predicted_memory,
            current_memory
        )

        # 20% safety headroom
        required_cpu = required_cpu / 0.80
        required_memory = required_memory / 0.80

        cpu_hosts = required_cpu / self.simulator.hosts[0].cpu_capacity
        memory_hosts = required_memory / self.simulator.hosts[0].memory_capacity

        required_hosts = max(
            cpu_hosts,
            memory_hosts
        )

        return max(1, int(required_hosts + 0.9999))

    def allocate_based_on_prediction(
        self,
        workload,
        current_vms
    ):

        prediction = self.predict_future_workload(workload)

        current_cpu = sum(
            vm.cpu_demand
            for vm in current_vms
        )

        current_memory = sum(
            vm.memory_demand
            for vm in current_vms
        )

        required_hosts = self.calculate_required_hosts(
            predicted_cpu=prediction["cpu_usage"],
            predicted_memory=prediction["memory_usage"],
            current_cpu=current_cpu,
            current_memory=current_memory
        )

        self.simulator.scale_to_hosts(required_hosts)

        for vm in current_vms:

            allocated = self.simulator.allocate_vm(vm)

            if not allocated:
                self.rejected_vms += 1

        return {
            "prediction": prediction,
            "current_cpu_demand": current_cpu,
            "current_memory_demand": current_memory,
            "required_hosts": required_hosts,
            "summary": self.simulator.get_summary()
        }

    def optimize_energy(self):

        optimizer = EnergyOptimizer(self.simulator)

        optimization_result = optimizer.optimize()

        self.vm_migrations += optimization_result["vm_migrations"]

        return optimization_result

    def get_results(self):

        summary = self.simulator.get_summary()

        return {
            "strategy": "predictive",
            "total_hosts": summary["total_hosts"],
            "powered_on_hosts": summary["powered_on_hosts"],
            "active_hosts": summary["active_hosts"],
            "total_vms": summary["total_vms"],
            "cpu_utilization": summary["cpu_utilization"],
            "power_watts": summary["power_watts"],
            "vm_migrations": self.vm_migrations,
            "rejected_vms": self.rejected_vms
        }