from digital_twin.fault_classifier import FaultClassifier
from digital_twin.twin_state import EngineState


def test_overheating_fault():
    state = EngineState(
        oil_temperature=125,
        cylinder_head_temperature=220,
    )

    classifier = FaultClassifier()
    result = classifier.classify(state)

    assert result.fault_type == "OVERHEATING"
    assert result.confidence > 0.9


def test_low_oil_pressure_fault():
    state = EngineState(
        oil_pressure=1.5,
    )

    classifier = FaultClassifier()
    result = classifier.classify(state)

    assert result.fault_type == "LOW_OIL_PRESSURE"


def test_high_vibration_fault():
    state = EngineState(
        vibration=2.0,
    )

    classifier = FaultClassifier()
    result = classifier.classify(state)

    assert result.fault_type == "HIGH_VIBRATION"


def test_combustion_anomaly():
    state = EngineState(
        egt=800,
    )

    classifier = FaultClassifier()
    result = classifier.classify(state)

    assert result.fault_type == "COMBUSTION_ANOMALY"


def test_normal_engine():
    state = EngineState(
        oil_temperature=90,
        cylinder_head_temperature=160,
        egt=650,
        oil_pressure=4.5,
        vibration=0.5,
    )

    classifier = FaultClassifier()
    result = classifier.classify(state)

    assert result.fault_type == "NORMAL"
    assert result.confidence == 0.99


if __name__ == "__main__":
    test_overheating_fault()
    test_low_oil_pressure_fault()
    test_high_vibration_fault()
    test_combustion_anomaly()
    test_normal_engine()

    print("Fault Classifier tests passed!")
