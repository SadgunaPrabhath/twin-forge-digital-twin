import random
from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class EngineTelemetry:
    rpm: float
    torque: float
    oil_temperature: float
    cylinder_head_temperature: float
    egt: float
    oil_pressure: float
    fuel_flow: float
    vibration: float
    engine_hours: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


class EngineSimulator:
    """
    Simulates telemetry from an aero piston engine.

    Supports:
    - normal operation
    - gradual degradation
    - overheating
    - low oil pressure
    - high vibration
    - combustion anomaly
    """

    def __init__(self, seed: int = 42) -> None:
        random.seed(seed)

        self.engine_hours = 500.0
        self.step = 0

        self.base_rpm = 4200.0
        self.base_torque = 85.0

    def generate(self, fault: str = "normal") -> EngineTelemetry:
        self.step += 1
        self.engine_hours += 0.1

        degradation = min(1.0, self.step / 1000)

        rpm = self.base_rpm + random.uniform(-80, 80)
        torque = self.base_torque + random.uniform(-3, 3)

        oil_temperature = 90 + degradation * 10 + random.uniform(-2, 2)

        cylinder_head_temperature = 165 + degradation * 20 + random.uniform(-4, 4)

        egt = 650 + degradation * 40 + random.uniform(-15, 15)

        oil_pressure = 4.5 - degradation * 0.5 + random.uniform(-0.15, 0.15)

        fuel_flow = 18 + degradation * 1.5 + random.uniform(-0.5, 0.5)

        vibration = 0.5 + degradation * 0.4 + random.uniform(-0.05, 0.05)

        # Fault injection
        if fault == "overheating":
            oil_temperature += 35
            cylinder_head_temperature += 55
            egt += 100

        elif fault == "low_oil_pressure":
            oil_pressure -= 2.5

        elif fault == "high_vibration":
            vibration += 1.8

        elif fault == "combustion_anomaly":
            egt += 130
            fuel_flow += 4

        return EngineTelemetry(
            rpm=round(rpm, 2),
            torque=round(torque, 2),
            oil_temperature=round(oil_temperature, 2),
            cylinder_head_temperature=round(cylinder_head_temperature, 2),
            egt=round(egt, 2),
            oil_pressure=round(oil_pressure, 2),
            fuel_flow=round(fuel_flow, 2),
            vibration=round(vibration, 2),
            engine_hours=round(self.engine_hours, 2),
        )
