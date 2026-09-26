from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from digital_twin.engine import DigitalTwinEngine
from simulator.engine_simulator import EngineSimulator


app = FastAPI(
    title="Twin Forge Digital Twin API",
    description=(
        "AI-enabled real-time digital twin for health monitoring, "
        "fault prediction, RUL estimation and mission reliability."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# GLOBAL ENGINE STATE
# ============================================================

engine = DigitalTwinEngine(
    mission_duration_hours=1.0
)

simulator = EngineSimulator()

latest_result: Optional[dict] = None
current_scenario = "normal"


# ============================================================
# REQUEST MODELS
# ============================================================

class SimulatorRequest(BaseModel):
    fault: str = "normal"


class ScenarioRequest(BaseModel):
    scenario: str = "normal"


# ============================================================
# HELPERS
# ============================================================

def serialize_result(result: dict) -> dict:
    """
    Convert Digital Twin pipeline dataclasses into JSON-safe data.
    """

    state = result.get("state")
    anomaly = result.get("anomaly")
    fault = result.get("fault")
    rul = result.get("rul")
    reliability = result.get("mission_reliability")

    state_dict = vars(state) if state is not None else {}

    anomaly_dict = vars(anomaly) if anomaly is not None else {}

    fault_dict = vars(fault) if fault is not None else {}

    rul_dict = vars(rul) if rul is not None else {}

    reliability_dict = (
        vars(reliability)
        if reliability is not None
        else {}
    )

    health = result.get("health_index", 0.0)

    fault_probability = result.get(
        "fault_probability",
        anomaly_dict.get("score", 0.0),
    )

    fault_type = result.get(
        "fault_type",
        fault_dict.get("fault_type", "NORMAL"),
    )

    rul_hours = result.get(
        "rul_hours",
        rul_dict.get("remaining_hours"),
    )

    reliability_value = result.get(
        "reliability",
        reliability_dict.get("reliability"),
    )

    # Determine severity for dashboard
    if fault_type == "NORMAL" and health >= 80:
        severity = "NORMAL"
    elif health < 40 or (
        rul_hours is not None and rul_hours < 10
    ):
        severity = "CRITICAL"
    elif fault_type != "NORMAL":
        severity = "WARNING"
    else:
        severity = "ATTENTION"

    telemetry = {}

    if state is not None:
        telemetry = {
            "rpm": state.rpm,
            "torque": state.torque,
            "oil_temperature": state.oil_temperature,
            "cylinder_head_temperature": state.cylinder_head_temperature,
            "egt": state.egt,
            "oil_pressure": state.oil_pressure,
            "fuel_flow": state.fuel_flow,
            "vibration": state.vibration,
            "engine_hours": state.engine_hours,
            "mission_phase": state.mission_phase,
            "timestamp": state.timestamp.isoformat()
            if hasattr(state.timestamp, "isoformat")
            else str(state.timestamp),
        }

    return {
        "status": "OK",
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "state": state_dict,

        "health_index": health,

        "anomaly": anomaly_dict,

        "fault": fault_dict,

        "degradation": result.get(
            "degradation",
            state.degradation_level if state else 0.0,
        ),

        "rul": rul_dict,

        "mission_reliability": reliability_dict,

        "rul_hours": rul_hours,

        "reliability": reliability_value,

        "fault_probability": fault_probability,

        "fault_type": fault_type,

        "severity": severity,

        "scenario": current_scenario,

        "telemetry": telemetry,
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "name": "Twin Forge Digital Twin",
        "status": "ONLINE",
        "version": "1.0.0",
        "docs": "/docs",
        "state": "/api/v1/twin/state",
        "simulator": "/api/v1/simulator/step",
        "scenario": "/api/v1/simulator/scenario",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Twin Forge Digital Twin API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# CURRENT TWIN STATE
# ============================================================

@app.get("/api/v1/twin/state")
def get_twin_state():

    if latest_result is None:
        return {
            "status": "NO_DATA",
            "state": None,
            "scenario": current_scenario,
        }

    return serialize_result(latest_result)


# ============================================================
# SIMULATOR STEP
# ============================================================

@app.post("/api/v1/simulator/step")
def simulator_step(request: SimulatorRequest):

    global latest_result

    fault = request.fault.lower().strip()

    allowed_faults = {
        "normal",
        "overheating",
        "low_oil_pressure",
        "high_vibration",
        "combustion_anomaly",
    }

    if fault not in allowed_faults:
        fault = "normal"

    telemetry = simulator.generate(fault=fault)

    sensor_data = telemetry.to_dict()

    result = engine.process(sensor_data)

    latest_result = result

    response = serialize_result(result)

    response["scenario"] = fault

    return response


# ============================================================
# SCENARIO CONTROL
# ============================================================

@app.post("/api/v1/simulator/scenario")
def set_scenario(request: ScenarioRequest):

    global current_scenario

    scenario = request.scenario.lower().strip()

    allowed_scenarios = {
        "normal",
        "overheating",
        "low_oil_pressure",
        "high_vibration",
        "combustion_anomaly",
    }

    if scenario not in allowed_scenarios:
        return {
            "status": "ERROR",
            "message": "Unsupported scenario.",
            "allowed_scenarios": sorted(allowed_scenarios),
        }

    current_scenario = scenario

    return {
        "status": "OK",
        "scenario": current_scenario,
        "message": f"Scenario changed to {current_scenario}.",
    }


# ============================================================
# DEMO SCENARIO
# ============================================================

@app.post("/api/v1/demo/scenario")
def demo_scenario(request: ScenarioRequest):

    global latest_result
    global current_scenario

    scenario = request.scenario.lower().strip()

    allowed_scenarios = {
        "normal",
        "overheating",
        "low_oil_pressure",
        "high_vibration",
        "combustion_anomaly",
    }

    if scenario not in allowed_scenarios:
        return {
            "status": "ERROR",
            "message": "Unsupported demo scenario.",
            "allowed_scenarios": sorted(allowed_scenarios),
        }

    current_scenario = scenario

    telemetry = simulator.generate(
        fault=scenario
    )

    result = engine.process(
        telemetry.to_dict()
    )

    latest_result = result

    response = serialize_result(result)

    response["demo"] = True
    response["scenario"] = scenario

    return response


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    print("=" * 60)
    print("TWIN FORGE DIGITAL TWIN API")
    print("API ONLINE")
    print("Docs: http://127.0.0.1:8000/docs")
    print("State: /api/v1/twin/state")
    print("Simulator: /api/v1/simulator/step")
    print("Scenario: /api/v1/simulator/scenario")
    print("Demo: /api/v1/demo/scenario")
    print("=" * 60)