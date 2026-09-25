from digital_twin.health_index import HealthIndexCalculator
from digital_twin.twin_state import EngineState


def test_healthy_engine():
    state = EngineState(
        oil_temperature=90,
        cylinder_head_temperature=160,
        egt=650,
        oil_pressure=4.5,
        vibration=0.5,
    )

    calculator = HealthIndexCalculator()
    health = calculator.calculate(state)

    assert health == 100.0
    assert state.health_index == 100.0


def test_high_temperature_reduces_health():
    state = EngineState(
        oil_temperature=120,
        cylinder_head_temperature=200,
        egt=750,
        oil_pressure=4.0,
        vibration=0.5,
    )

    calculator = HealthIndexCalculator()
    health = calculator.calculate(state)

    assert health < 100.0
    assert health >= 0.0


def test_low_oil_pressure_reduces_health():
    state = EngineState(
        oil_temperature=90,
        cylinder_head_temperature=160,
        egt=650,
        oil_pressure=2.0,
        vibration=0.5,
    )

    calculator = HealthIndexCalculator()
    health = calculator.calculate(state)

    assert health < 100.0


def test_health_never_below_zero():
    state = EngineState(
        oil_temperature=200,
        cylinder_head_temperature=300,
        egt=1000,
        oil_pressure=0.5,
        vibration=10.0,
    )

    calculator = HealthIndexCalculator()
    health = calculator.calculate(state)

    assert health >= 0.0


if __name__ == "__main__":
    test_healthy_engine()
    test_high_temperature_reduces_health()
    test_low_oil_pressure_reduces_health()
    test_health_never_below_zero()

    print("Health Index tests passed!")
