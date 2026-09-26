from ml.rul_pipeline import RULPipeline
from simulator.engine_simulator import EngineSimulator


def test_rul_pipeline():

    pipeline = RULPipeline(training_samples=500)

    pipeline.train()

    simulator = EngineSimulator()

    telemetry = simulator.generate(fault="normal")

    result = pipeline.predict_telemetry(telemetry)

    assert "rul_hours" in result
    assert "rul_days" in result

    assert result["rul_hours"] >= 0
    assert result["rul_days"] >= 0


def test_rul_pipeline_requires_training():

    pipeline = RULPipeline()

    simulator = EngineSimulator()

    telemetry = simulator.generate()

    try:
        pipeline.predict_telemetry(telemetry)

    except RuntimeError:
        return

    raise AssertionError("Untrained RUL pipeline should raise RuntimeError.")


if __name__ == "__main__":
    test_rul_pipeline()
    test_rul_pipeline_requires_training()

    print("RUL pipeline tests passed!")
