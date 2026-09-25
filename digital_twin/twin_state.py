from dataclasses import dataclass
from typing import Optional


@dataclass
class EngineState:
    """
    Current estimated state of the aero piston engine.
    """

    timestamp: Optional[str] = None
    mission_phase: str = "START"

    # Operating state
    rpm: float = 0.0
    torque: float = 0.0
    power_kw: float = 0.0
    throttle: float = 0.0
    load: float = 0.0

    # Thermal state
    oil_temperature: float = 0.0
    cylinder_head_temperature: float = 0.0
    egt: float = 0.0

    # Pressure / flow
    oil_pressure: float = 0.0
    fuel_flow: float = 0.0

    # Vibration
    vibration: float = 0.0

    # Long-term condition
    engine_hours: float = 0.0
    degradation_level: float = 0.0

    # AI outputs
    health_index: float = 100.0
    fault_probability: float = 0.0
    fault_type: str = "NORMAL"

    # Prediction outputs
    rul_hours: Optional[float] = None
    mission_reliability: Optional[float] = None
