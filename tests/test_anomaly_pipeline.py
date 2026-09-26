from ml.anomaly_pipeline import AnomalyPipeline
from simulator.engine_simulator import EngineSimulator


def test_pipeline_normal_engine():

    pipeline = AnomalyPipeline(training_samples=500)

    pipeline.train()

    simulator = EngineSimulator()

    telemetry = simulator.generate(fault="normal")

    result = pipeline.predict_telemetry(telemetry)

    assert "is_anomaly" in result
    assert "anomaly_score" in result
    assert isinstance(result["is_anomaly"], bool)


def test_pipeline_detects_overheating():

    pipeline = AnomalyPipeline(training_samples=500)

    pipeline.train()

    simulator = EngineSimulator()

    telemetry = simulator.generate(fault="overheating")

    result = pipeline.predict_telemetry(telemetry)

    assert result["is_anomaly"] is True


if __name__ == "__main__":
    test_pipeline_normal_engine()
    test_pipeline_detects_overheating()

    print("Anomaly pipeline tests passed!")
