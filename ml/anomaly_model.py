import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyModel:
    """
    ML-based anomaly detector using Isolation Forest.
    """

    def __init__(
        self,
        contamination: float = 0.05,
        random_state: int = 42,
    ) -> None:

        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
        )

        self.is_trained = False

    def train(self, X: np.ndarray) -> None:
        """
        Train the anomaly detection model.
        """

        X = np.asarray(X)

        if X.ndim != 2:
            raise ValueError("Training data must be 2-dimensional.")

        if len(X) < 10:
            raise ValueError("At least 10 samples are required for training.")

        self.model.fit(X)
        self.is_trained = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict whether observations are normal or anomalous.

        Returns:
            1  -> normal
           -1  -> anomaly
        """

        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction.")

        X = np.asarray(X)

        return self.model.predict(X)

    def anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """
        Return anomaly scores.

        Higher values indicate more anomalous behaviour.
        """

        if not self.is_trained:
            raise RuntimeError("Model must be trained before scoring.")

        X = np.asarray(X)

        return -self.model.score_samples(X)
