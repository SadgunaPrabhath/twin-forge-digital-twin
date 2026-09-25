from digital_twin.twin_state import EngineState


def test_engine_state_defaults():
    state = EngineState()

    assert state.rpm == 0.0
    assert state.health_index == 100.0
    assert state.fault_probability == 0.0
    assert state.fault_type == "NORMAL"
    assert state.rul_hours is None


if __name__ == "__main__":
    test_engine_state_defaults()
    print("EngineState test passed!")
