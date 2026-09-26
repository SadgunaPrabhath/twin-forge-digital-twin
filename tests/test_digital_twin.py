from digital_twin.twin import DigitalTwin


def test_digital_twin_update():
    twin = DigitalTwin()

    sensor_data = {
        "rpm": 4200,
        "torque": 85,
        "oil_temperature": 92,
        "vibration": 0.8,
    }

    state = twin.update(sensor_data)

    assert state.rpm == 4200
    assert state.torque == 85
    assert state.oil_temperature == 92
    assert state.vibration == 0.8


def test_digital_twin_get_state():
    twin = DigitalTwin()

    twin.update(
        {
            "rpm": 3500,
            "oil_pressure": 4.5,
        }
    )

    state = twin.get_state()

    assert isinstance(state, dict)
    assert state["rpm"] == 3500
    assert state["oil_pressure"] == 4.5


if __name__ == "__main__":
    test_digital_twin_update()
    test_digital_twin_get_state()
    print("DigitalTwin tests passed!")
