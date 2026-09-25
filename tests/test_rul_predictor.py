from digital_twin.rul_predictor import RULPredictor


def test_rul_with_degradation():
    predictor = RULPredictor(
        maximum_life_hours=2000.0,
        minimum_health=20.0,
    )

    history = [
        100.0,
        95.0,
        90.0,
        85.0,
        80.0,
    ]

    result = predictor.predict(
        health_history=history,
        current_engine_hours=500.0,
    )

    assert result.remaining_hours == 12.0
    assert result.confidence > 0.0


def test_failed_engine_has_zero_rul():
    predictor = RULPredictor()

    result = predictor.predict(
        health_history=[30.0, 20.0],
        current_engine_hours=1000.0,
    )

    assert result.remaining_hours == 0.0


def test_no_history():
    predictor = RULPredictor()

    result = predictor.predict(
        health_history=[],
        current_engine_hours=500.0,
    )

    assert result.remaining_hours == 2000.0
    assert result.confidence == 0.20


def test_no_degradation():
    predictor = RULPredictor(maximum_life_hours=2000.0)

    result = predictor.predict(
        health_history=[
            100.0,
            100.0,
            100.0,
        ],
        current_engine_hours=500.0,
    )

    assert result.remaining_hours == 1500.0
    assert result.confidence == 0.40


if __name__ == "__main__":
    test_rul_with_degradation()
    test_failed_engine_has_zero_rul()
    test_no_history()
    test_no_degradation()

    print("RUL Predictor tests passed!")
