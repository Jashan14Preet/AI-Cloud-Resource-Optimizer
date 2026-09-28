from app.simulation.cloud import CloudSimulator, VM
from app.services.sla_service import SLAService


simulator = CloudSimulator(
    number_of_hosts=5,
    cpu_per_host=100,
    memory_per_host=100
)


vms = []

for vm_id in range(1, 11):

    vm = VM(
        vm_id=vm_id,
        cpu_demand=10,
        memory_demand=15
    )

    vms.append(vm)


rejected_vms = 0

for vm in vms:

    allocated = simulator.allocate_vm(vm)

    if not allocated:
        rejected_vms += 1


sla_service = SLAService()

result = sla_service.calculate_sla_violations(
    simulator,
    rejected_vms
)


print("\n===================================")
print("SLA ANALYSIS")
print("===================================")

print(result)

print("\n===================================")