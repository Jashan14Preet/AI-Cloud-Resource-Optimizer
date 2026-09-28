from dataclasses import dataclass
from typing import List


@dataclass
class VM:
    vm_id: int
    cpu_demand: float
    memory_demand: float
    host_id: int | None = None


@dataclass
class Host:
    host_id: int
    cpu_capacity: float
    memory_capacity: float
    idle_power: float
    max_power: float
    vms: List[VM]
    powered_on: bool = True

    def used_cpu(self):
        return sum(vm.cpu_demand for vm in self.vms)

    def used_memory(self):
        return sum(vm.memory_demand for vm in self.vms)

    def cpu_utilization(self):
        return self.used_cpu() / self.cpu_capacity

    def memory_utilization(self):
        return self.used_memory() / self.memory_capacity

    def is_overloaded(
        self,
        cpu_threshold=0.9,
        memory_threshold=0.9
    ):
        return (
            self.cpu_utilization() > cpu_threshold
            or self.memory_utilization() > memory_threshold
        )

    def power_consumption(self):
        """
        Simple linear server power model.

        If the host is powered off, power consumption is 0.

        Otherwise:
        Power =
        Idle Power + (Max Power - Idle Power) * CPU utilization
        """

        if not self.powered_on:
            return 0

        utilization = min(
            max(self.cpu_utilization(), 0),
            1
        )

        return (
            self.idle_power
            + (self.max_power - self.idle_power) * utilization
        )


class CloudSimulator:

    def __init__(
        self,
        number_of_hosts=10,
        cpu_per_host=100,
        memory_per_host=100,
        idle_power=120,
        max_power=250
    ):

        self.hosts = []

        for host_id in range(1, number_of_hosts + 1):

            host = Host(
                host_id=host_id,
                cpu_capacity=cpu_per_host,
                memory_capacity=memory_per_host,
                idle_power=idle_power,
                max_power=max_power,
                vms=[],
                powered_on=(host_id <= 5)
            )

            self.hosts.append(host)

    def allocate_vm(self, vm):
        """
        Allocate a VM using First Fit.

        Only powered-on hosts can receive VMs.
        """

        for host in self.hosts:

            if not host.powered_on:
                continue

            available_cpu = (
                host.cpu_capacity - host.used_cpu()
            )

            available_memory = (
                host.memory_capacity - host.used_memory()
            )

            if (
                vm.cpu_demand <= available_cpu
                and vm.memory_demand <= available_memory
            ):

                host.vms.append(vm)
                vm.host_id = host.host_id

                return True

        return False

    def get_active_hosts(self):
        """
        Return hosts that currently contain VMs.
        """

        return [
            host
            for host in self.hosts
            if len(host.vms) > 0
        ]

    def get_powered_on_hosts(self):
        """
        Return hosts that are currently powered on.
        """

        return [
            host
            for host in self.hosts
            if host.powered_on
        ]

    def get_total_power(self):
        """
        Calculate total power consumption
        of all hosts.
        """

        return sum(
            host.power_consumption()
            for host in self.hosts
        )

    def get_total_cpu_utilization(self):

        active_hosts = self.get_active_hosts()

        total_capacity = sum(
            host.cpu_capacity
            for host in active_hosts
        )

        if total_capacity == 0:
            return 0

        total_used = sum(
            host.used_cpu()
            for host in active_hosts
        )

        return total_used / total_capacity

    def scale_to_hosts(self, required_hosts):
        """
        Power on additional hosts when
        predicted workload requires them.
        """

        powered_on_hosts = self.get_powered_on_hosts()

        current_count = len(powered_on_hosts)

        if required_hosts <= current_count:
            return current_count

        for host in self.hosts:

            if not host.powered_on:

                host.powered_on = True
                current_count += 1

            if current_count >= required_hosts:
                break

        return current_count

    def power_on_host(self, host_id):

        for host in self.hosts:

            if host.host_id == host_id:
                host.powered_on = True
                return True

        return False

    def power_off_host(self, host_id):

        for host in self.hosts:

            if host.host_id == host_id:

                if len(host.vms) == 0:
                    host.powered_on = False
                    return True

                return False

        return False

    def get_summary(self):

        active_hosts = self.get_active_hosts()

        return {
            "total_hosts": len(self.hosts),

            "powered_on_hosts": len(
                self.get_powered_on_hosts()
            ),

            "active_hosts": len(active_hosts),

            "total_vms": sum(
                len(host.vms)
                for host in self.hosts
            ),

            "cpu_utilization": round(
                self.get_total_cpu_utilization() * 100,
                2
            ),

            "power_watts": round(
                self.get_total_power(),
                2
            )
        }


if __name__ == "__main__":

    simulator = CloudSimulator(
        number_of_hosts=5
    )

    for vm_id in range(1, 11):

        vm = VM(
            vm_id=vm_id,
            cpu_demand=10,
            memory_demand=15
        )

        allocated = simulator.allocate_vm(vm)

        print(
            f"VM {vm_id}: "
            f"{'Allocated' if allocated else 'Rejected'}"
        )

    print("\nCloud Summary:")
    print(simulator.get_summary())