from digital_twin.mission_reliability import (
    MissionReliabilityCalculator,
)


def test_high_reliability():
    calculator = MissionReliabilityCalculator()

    result = calculator.calculate(
        health_index=95.0,
        fault_probability=0.05,
        rul_hours=100.0,
        mission_duration_hours=10.0,
    )

    assert result.reliability > 90.0
    assert result.risk_level == "LOW"


def test_medium_reliability():
    calculator = MissionReliabilityCalculator()

    result = calculator.calculate(
        health_index=70.0,
        fault_probability=0.30,
        rul_hours=20.0,
        mission_duration_hours=10.0,
    )

    assert 60.0 <= result.reliability < 80.0
    assert result.risk_level == "MEDIUM"


def test_high_risk():
    calculator = MissionReliabilityCalculator()

    result = calculator.calculate(
        health_index=30.0,
        fault_probability=0.80,
        rul_hours=2.0,
        mission_duration_hours=10.0,
    )

    assert result.reliability < 60.0
    assert result.risk_level == "HIGH"


def test_zero_mission_duration():
    calculator = MissionReliabilityCalculator()

    result = calculator.calculate(
        health_index=100.0,
        fault_probability=0.0,
        rul_hours=100.0,
        mission_duration_hours=0.0,
    )

    assert result.reliability == 100.0


if __name__ == "__main__":
    test_high_reliability()
    test_medium_reliability()
    test_high_risk()
    test_zero_mission_duration()

    print("Mission Reliability tests passed!")
