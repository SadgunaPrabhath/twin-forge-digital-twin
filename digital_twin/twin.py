from dataclasses import asdict
from typing import Any, Dict

from digital_twin.twin_state import EngineState


class DigitalTwin:
    """
    Digital Twin responsible for maintaining the latest
    estimated state of the aero piston engine.
    """

    def __init__(self) -> None:
        self.state = EngineState()

    def update(self, sensor_data: Dict[str, Any]) -> EngineState:
        """
        Update the digital twin using incoming sensor data.
        """

        for field, value in sensor_data.items():
            if hasattr(self.state, field):
                setattr(self.state, field, value)

        return self.state

    def get_state(self) -> Dict[str, Any]:
        """
        Return the current digital twin state as a dictionary.
        """

        return asdict(self.state)
