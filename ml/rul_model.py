import numpy as np
from sklearn.ensemble import RandomForestRegressor


class RULModel:
    """
    Machine-learning model for Remaining Useful Life prediction.
    """

    def __init__(
        self,
        n_estimators: int = 100,
        random_state: int = 42,
    ) -> None:

        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
        )

        self.is_trained = False

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
    ) -> None:

        X = np.asarray(X)
        y = np.asarray(y)

        if X.ndim != 2:
            raise ValueError("X must be a 2-dimensional array.")

        if y.ndim != 1:
            raise ValueError("y must be a 1-dimensional array.")

        if len(X) != len(y):
            raise ValueError("X and y must contain the same number of samples.")

        if len(X) < 20:
            raise ValueError("At least 20 samples are required.")

        self.model.fit(X, y)

        self.is_trained = True

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction.")

        X = np.asarray(X)

        predictions = self.model.predict(X)

        return np.maximum(
            predictions,
            0.0,
        )
