from digital_twin.anomaly_detector import AnomalyDetector
from digital_twin.twin_state import EngineState


def test_normal_engine():
    state = EngineState(
        oil_temperature=90,
        cylinder_head_temperature=160,
        egt=650,
        oil_pressure=4.5,
        vibration=0.5,
    )

    detector = AnomalyDetector()
    result = detector.detect(state)

    assert result.is_anomaly is False
    assert result.score == 0.0
    assert result.reasons == []


def test_high_temperature_anomaly():
    state = EngineState(
        oil_temperature=125,
        cylinder_head_temperature=160,
        egt=650,
        oil_pressure=4.5,
        vibration=0.5,
    )

    detector = AnomalyDetector()
    result = detector.detect(state)

    assert result.is_anomaly is True
    assert result.score > 0.0
    assert "High oil temperature" in result.reasons


def test_multiple_anomalies():
    state = EngineState(
        oil_temperature=125,
        cylinder_head_temperature=220,
        egt=800,
        oil_pressure=1.5,
        vibration=2.0,
    )

    detector = AnomalyDetector()
    result = detector.detect(state)

    assert result.is_anomaly is True
    assert result.score == 1.0
    assert len(result.reasons) == 5


if __name__ == "__main__":
    test_normal_engine()
    test_high_temperature_anomaly()
    test_multiple_anomalies()

    print("Anomaly Detector tests passed!")
