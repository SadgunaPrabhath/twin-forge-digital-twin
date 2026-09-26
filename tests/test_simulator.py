from simulator.engine_simulator import EngineSimulator


def test_normal_telemetry():

    simulator = EngineSimulator()

    telemetry = simulator.generate()

    assert telemetry.rpm > 0
    assert telemetry.torque > 0
    assert telemetry.oil_temperature > 0
    assert telemetry.oil_pressure > 0
    assert telemetry.vibration >= 0


def test_overheating_fault():

    simulator = EngineSimulator()

    telemetry = simulator.generate(fault="overheating")

    assert telemetry.oil_temperature > 110
    assert telemetry.cylinder_head_temperature > 200


def test_low_oil_pressure_fault():

    simulator = EngineSimulator()

    telemetry = simulator.generate(fault="low_oil_pressure")

    assert telemetry.oil_pressure < 2.5


def test_high_vibration_fault():

    simulator = EngineSimulator()

    telemetry = simulator.generate(fault="high_vibration")

    assert telemetry.vibration > 1.5


def test_combustion_anomaly():

    simulator = EngineSimulator()

    telemetry = simulator.generate(fault="combustion_anomaly")

    assert telemetry.egt > 750


if __name__ == "__main__":
    test_normal_telemetry()
    test_overheating_fault()
    test_low_oil_pressure_fault()
    test_high_vibration_fault()
    test_combustion_anomaly()

    print("Engine Simulator tests passed!")
