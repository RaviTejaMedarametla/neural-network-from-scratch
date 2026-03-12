from __future__ import annotations


class EnergyModel:
    """Energy model parameterized by technology node."""

    def __init__(self, tech_node_nm: int) -> None:
        self.tech_node_nm = tech_node_nm

    def energy_per_mac_pj(self) -> float:
        """Return rough pJ/MAC based on process scaling."""
        return 5.0 * (self.tech_node_nm / 45.0)

    def energy_per_byte_pj(self) -> float:
        """Return rough pJ/byte scaling."""
        return 20.0 * (self.tech_node_nm / 45.0)


class TSMC28nmEnergy(EnergyModel):
    def __init__(self) -> None:
        super().__init__(28)


class TSMC7nmEnergy(EnergyModel):
    def __init__(self) -> None:
        super().__init__(7)
