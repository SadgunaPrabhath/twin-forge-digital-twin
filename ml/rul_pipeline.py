from typing import Any, Dict

from ml.rul_data import generate_rul_dataset
from ml.rul_model import RULModel
from ml.training_data import telemetry_to_features


class RULPipeline:
    """
    Complete Remaining Useful Life prediction pipeline.

    Generates synthetic degradation data, trains the
    RUL model, and predicts remaining engine life.
    """

    def __init__(
        self,
        training_samples: int = 1000,
        seed: int = 42,
    ) -> None:

        self.training_samples = training_samples
        self.seed = seed

        self.model = RULModel()

        self.is_trained = False

    def train(self) -> None:
        """
        Generate training data and train the RUL model.
        """

        X, y = generate_rul_dataset(
            samples=self.training_samples,
            seed=self.seed,
        )

        self.model.train(X, y)

        self.is_trained = True

    def predict_telemetry(
        self,
        telemetry,
    ) -> Dict[str, Any]:
        """
        Predict RUL for one engine telemetry observation.
        """

        if not self.is_trained:
            raise RuntimeError("RUL pipeline must be trained before prediction.")

        features = telemetry_to_features(telemetry)

        prediction = self.model.predict([features])[0]

        return {
            "rul_hours": float(prediction),
            "rul_days": float(prediction / 24.0),
        }
