from digital_twin.engine import DigitalTwinEngine


def test_complete_pipeline():

    engine = DigitalTwinEngine(mission_duration_hours=10.0)

    sensor_data = {
        "rpm": 4200,
        "torque": 85,
        "oil_temperature": 92,
        "cylinder_head_temperature": 170,
        "egt": 680,
        "oil_pressure": 4.2,
        "fuel_flow": 18,
        "vibration": 0.8,
        "engine_hours": 500,
    }

    result = engine.process(sensor_data)

    assert result["state"].rpm == 4200

    assert result["health_index"] == 100.0

    assert result["anomaly"].is_anomaly is False

    assert result["fault"].fault_type == "NORMAL"

    assert result["degradation"] == 0.0

    assert result["rul"].remaining_hours == 1500.0

    assert result["mission_reliability"].reliability > 90.0


def test_pipeline_detects_fault():

    engine = DigitalTwinEngine(mission_duration_hours=10.0)

    sensor_data = {
        "rpm": 4200,
        "torque": 85,
        "oil_temperature": 125,
        "cylinder_head_temperature": 220,
        "egt": 800,
        "oil_pressure": 1.5,
        "fuel_flow": 18,
        "vibration": 2.0,
        "engine_hours": 500,
    }

    result = engine.process(sensor_data)

    assert result["anomaly"].is_anomaly is True

    assert result["fault"].fault_type == "OVERHEATING"

    assert result["health_index"] < 100.0

    assert result["degradation"] > 0.0


if __name__ == "__main__":
    test_complete_pipeline()
    test_pipeline_detects_fault()

    print("Complete Digital Twin pipeline tests passed!")
