from digital_twin.engine import DigitalTwinEngine
from simulator.engine_simulator import EngineSimulator


def test_simulator_to_digital_twin():

    simulator = EngineSimulator()

    engine = DigitalTwinEngine(mission_duration_hours=10.0)

    telemetry = simulator.generate()

    result = engine.process(telemetry.to_dict())

    assert result["state"] is not None
    assert result["health_index"] >= 0
    assert result["health_index"] <= 100
    assert result["fault"] is not None
    assert result["rul"] is not None
    assert result["mission_reliability"] is not None


def test_simulator_can_trigger_fault():

    simulator = EngineSimulator()

    engine = DigitalTwinEngine(mission_duration_hours=10.0)

    telemetry = simulator.generate(fault="overheating")

    result = engine.process(telemetry.to_dict())

    assert result["anomaly"].is_anomaly is True
    assert result["fault"].fault_type == "OVERHEATING"


if __name__ == "__main__":
    test_simulator_to_digital_twin()
    test_simulator_can_trigger_fault()

    print("Simulator -> Digital Twin integration passed!")
