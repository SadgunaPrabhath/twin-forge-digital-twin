from typing import Any, Dict

from ml.anomaly_model import AnomalyModel
from ml.training_data import (
    generate_training_data,
    telemetry_to_features,
)


class AnomalyPipeline:
    """
    Complete ML anomaly-detection pipeline.

    Generates normal training data, trains the model,
    and evaluates new engine telemetry.
    """

    def __init__(
        self,
        training_samples: int = 1000,
        seed: int = 42,
    ) -> None:

        self.training_samples = training_samples
        self.seed = seed

        self.model = AnomalyModel()

        self.is_trained = False

    def train(self) -> None:
        """
        Generate normal engine data and train
        the anomaly detection model.
        """

        training_data = generate_training_data(
            samples=self.training_samples,
            seed=self.seed,
        )

        self.model.train(training_data)

        self.is_trained = True

    def predict_telemetry(
        self,
        telemetry,
    ) -> Dict[str, Any]:
        """
        Evaluate one engine telemetry observation.
        """

        if not self.is_trained:
            raise RuntimeError("Pipeline must be trained before prediction.")

        features = telemetry_to_features(telemetry)

        prediction = self.model.predict([features])[0]

        score = self.model.anomaly_score([features])[0]

        return {
            "is_anomaly": bool(prediction == -1),
            "prediction": int(prediction),
            "anomaly_score": float(score),
        }
