from app.simulation.cloud import CloudSimulator, VM


class EnergyOptimizer:

    def __init__(self, simulator):
        self.simulator = simulator

    def consolidate_vms(self):
        """
        Try to move VMs from lightly utilized hosts
        onto other active hosts.

        This helps reduce the number of active hosts.
        """

        hosts = self.simulator.get_active_hosts()

        # Sort hosts by CPU utilization
        hosts = sorted(
            hosts,
            key=lambda host: host.cpu_utilization()
        )

        migrations = 0

        for source_host in hosts:

            if not source_host.vms:
                continue

            source_vms = list(source_host.vms)

            for vm in source_vms:

                moved = False

                for target_host in hosts:

                    if target_host.host_id == source_host.host_id:
                        continue

                    available_cpu = (
                        target_host.cpu_capacity
                        - target_host.used_cpu()
                    )

                    available_memory = (
                        target_host.memory_capacity
                        - target_host.used_memory()
                    )

                    if (
                        vm.cpu_demand <= available_cpu
                        and vm.memory_demand <= available_memory
                    ):

                        source_host.vms.remove(vm)
                        target_host.vms.append(vm)

                        vm.host_id = target_host.host_id

                        migrations += 1
                        moved = True

                        break

                if not moved:
                    continue

        return migrations

    def shutdown_idle_hosts(self):
        """
        Power off hosts that no longer contain VMs.
        """

        shutdown_count = 0

        for host in self.simulator.hosts:

            if len(host.vms) == 0 and host.powered_on:

                powered_off = self.simulator.power_off_host(
                    host.host_id
                )

                if powered_off:
                    shutdown_count += 1

        return shutdown_count

    def optimize(self):
        """
        Perform VM consolidation and power off
        unused hosts.
        """

        # Step 1: Consolidate VMs
        migrations = self.consolidate_vms()

        # Step 2: Power off empty hosts
        shutdown_hosts = self.shutdown_idle_hosts()

        # Step 3: Get final state
        summary = self.simulator.get_summary()

        return {
            "vm_migrations": migrations,
            "shutdown_hosts": shutdown_hosts,
            "active_hosts": summary["active_hosts"],
            "powered_on_hosts": summary["powered_on_hosts"],
            "power_watts": summary["power_watts"]
        }


if __name__ == "__main__":

    simulator = CloudSimulator(
        number_of_hosts=5
    )

    # Create sample VMs
    for vm_id in range(1, 11):

        vm = VM(
            vm_id=vm_id,
            cpu_demand=10,
            memory_demand=15
        )

        simulator.allocate_vm(vm)

    print("\nBefore optimization:")
    print(simulator.get_summary())

    optimizer = EnergyOptimizer(simulator)

    results = optimizer.optimize()

    print("\nOptimization results:")
    print(results)

    print("\nAfter optimization:")
    print(simulator.get_summary())