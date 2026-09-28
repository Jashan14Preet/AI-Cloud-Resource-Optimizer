class SustainabilityService:

    def __init__(
        self,
        carbon_intensity=0.7,
        electricity_cost=8.0
    ):
        """
        carbon_intensity:
            kg CO2 emitted per kWh.

        electricity_cost:
            Cost per kWh.
        """

        self.carbon_intensity = carbon_intensity
        self.electricity_cost = electricity_cost

    def calculate_energy(self, power_watts, duration_hours):
        """
        Convert power consumption in watts
        into energy consumption in kWh.
        """

        energy_kwh = (
            power_watts * duration_hours
        ) / 1000

        return round(energy_kwh, 4)

    def calculate_carbon(self, energy_kwh):
        """
        Calculate carbon emissions in kg CO2.
        """

        carbon_kg = (
            energy_kwh * self.carbon_intensity
        )

        return round(carbon_kg, 4)

    def calculate_cost(self, energy_kwh):
        """
        Calculate electricity cost.
        """

        cost = (
            energy_kwh * self.electricity_cost
        )

        return round(cost, 4)

    def calculate_sustainability(
        self,
        power_watts,
        duration_hours
    ):
        """
        Calculate energy, carbon and cost
        for a given workload period.
        """

        energy_kwh = self.calculate_energy(
            power_watts,
            duration_hours
        )

        carbon_kg = self.calculate_carbon(
            energy_kwh
        )

        cost = self.calculate_cost(
            energy_kwh
        )

        return {
            "power_watts": round(power_watts, 2),
            "duration_hours": duration_hours,
            "energy_kwh": energy_kwh,
            "carbon_kg": carbon_kg,
            "electricity_cost": cost
        }


if __name__ == "__main__":

    service = SustainabilityService()

    result = service.calculate_sustainability(
        power_watts=370,
        duration_hours=1
    )

    print("\nSustainability Results:")

    print(result)