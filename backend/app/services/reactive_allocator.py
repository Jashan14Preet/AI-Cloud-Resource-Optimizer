from app.simulation.cloud import CloudSimulator, VM
from app.simulation.energy_optimizer import EnergyOptimizer


class ReactiveAllocator:

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

        self.vm_migrations = 0
        self.rejected_vms = 0

    def allocate_workload(self, vms):

        for vm in vms:

            allocated = self.simulator.allocate_vm(vm)

            if not allocated:
                self.rejected_vms += 1

        return self.simulator.get_summary()

    def optimize_energy(self):

        optimizer = EnergyOptimizer(self.simulator)

        optimization_result = optimizer.optimize()

        self.vm_migrations += optimization_result["vm_migrations"]

        return optimization_result

    def get_results(self):

        summary = self.simulator.get_summary()

        return {
            "strategy": "reactive",
            "total_hosts": summary["total_hosts"],
            "powered_on_hosts": summary["powered_on_hosts"],
            "active_hosts": summary["active_hosts"],
            "total_vms": summary["total_vms"],
            "cpu_utilization": summary["cpu_utilization"],
            "power_watts": summary["power_watts"],
            "vm_migrations": self.vm_migrations,
            "rejected_vms": self.rejected_vms
        }