class SLAService:

    def __init__(
        self,
        cpu_threshold=0.90,
        memory_threshold=0.90
    ):

        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold

    def check_host_violation(self, host):

        cpu_violation = (
            host.cpu_utilization()
            > self.cpu_threshold
        )

        memory_violation = (
            host.memory_utilization()
            > self.memory_threshold
        )

        return cpu_violation or memory_violation

    def calculate_sla_violations(
        self,
        simulator,
        rejected_vms=0
    ):

        overloaded_hosts = 0

        for host in simulator.hosts:

            if self.check_host_violation(host):

                overloaded_hosts += 1

        total_violations = (
            rejected_vms
            + overloaded_hosts
        )

        return {
            "rejected_vms": rejected_vms,
            "overloaded_hosts": overloaded_hosts,
            "total_sla_violations": total_violations,
            "sla_status": (
                "VIOLATION"
                if total_violations > 0
                else "SATISFIED"
            )
        }