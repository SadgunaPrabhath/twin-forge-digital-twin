from digital_twin.degradation import DegradationTracker


def test_degradation_tracking():
    tracker = DegradationTracker()

    assert tracker.current_degradation == 0.0

    tracker.update(100.0)
    tracker.update(95.0)
    tracker.update(90.0)

    assert tracker.history == [100.0, 95.0, 90.0]
    assert tracker.current_degradation == 10.0


def test_average_health():
    tracker = DegradationTracker()

    tracker.update(100.0)
    tracker.update(90.0)
    tracker.update(80.0)

    assert tracker.average_health == 90.0


def test_health_is_clamped():
    tracker = DegradationTracker()

    tracker.update(120.0)
    tracker.update(-20.0)

    assert tracker.history == [100.0, 0.0]
    assert tracker.current_degradation == 100.0


if __name__ == "__main__":
    test_degradation_tracking()
    test_average_health()
    test_health_is_clamped()

    print("Degradation Tracker tests passed!")
