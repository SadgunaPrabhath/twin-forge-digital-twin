from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TelemetryInput(BaseModel):
    """
    Incoming virtual sensor telemetry for the aero piston engine.
    """

    timestamp: datetime

    mission_phase: str = Field(
        default="START", description="Current UAV mission phase."
    )

    # Operating state
    rpm: float = Field(ge=0, le=10000)
    torque: float = Field(ge=0, le=1000)
    throttle: float = Field(ge=0, le=100)

    # Thermal state
    oil_temperature: float = Field(ge=-50, le=300)
    cylinder_head_temperature: float = Field(ge=-50, le=400)
    egt: float = Field(ge=-50, le=1500)

    # Pressure / flow
    oil_pressure: float = Field(ge=0, le=20)
    fuel_flow: float = Field(ge=0, le=500)

    # Vibration
    vibration: float = Field(ge=0, le=100)

    # Long-term condition
    engine_hours: float = Field(ge=0, le=100000)


class HealthResponse(BaseModel):
    health_index: float
    status: str
    timestamp: Optional[datetime] = None


class FaultResponse(BaseModel):
    fault_type: str
    probability: float
    confidence: float
    severity: str
    explanation: str


class RULResponse(BaseModel):
    remaining_hours: Optional[float]
    confidence_lower: Optional[float] = None
    confidence_upper: Optional[float] = None
    status: str


class MissionResponse(BaseModel):
    mission_phase: str
    mission_reliability: float
    mission_duration_hours: float
    remaining_rul_hours: Optional[float]
    risk_level: str


class TelemetryResponse(BaseModel):
    timestamp: datetime
    mission_phase: str

    # Engine
    rpm: float
    torque: float
    power_kw: float
    throttle: float
    load: float

    # Thermal
    oil_temperature: float
    cylinder_head_temperature: float
    egt: float

    # Pressure / flow
    oil_pressure: float
    fuel_flow: float

    # Vibration
    vibration: float

    # Health / AI
    health_index: float
    anomaly_score: float
    fault_type: str
    fault_probability: float
    degradation_level: float

    # Prediction
    rul_hours: Optional[float]
    mission_reliability: Optional[float]

    # Decision support
    status: str
    severity: str
    recommendation: str
