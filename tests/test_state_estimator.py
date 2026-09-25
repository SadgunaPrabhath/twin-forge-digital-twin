from digital_twin.state_estimator import StateEstimator
from digital_twin.twin_state import EngineState


def test_power_estimation():
    state = EngineState(
        rpm=4200,
        torque=85,
    )

    estimator = StateEstimator()
    updated_state = estimator.estimate(state)

    expected_power = (85 * 4200) / 9550

    assert abs(updated_state.power_kw - expected_power) < 0.01


def test_load_estimation():
    state = EngineState(
        rpm=4200,
        torque=75,
    )

    estimator = StateEstimator()
    updated_state = estimator.estimate(state)

    assert updated_state.load == 75.0


def test_zero_rpm_load():
    state = EngineState(
        rpm=0,
        torque=0,
    )

    estimator = StateEstimator()
    updated_state = estimator.estimate(state)

    assert updated_state.load == 0.0


if __name__ == "__main__":
    test_power_estimation()
    test_load_estimation()
    test_zero_rpm_load()

    print("StateEstimator tests passed!")
