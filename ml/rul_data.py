import numpy as np

from ml.training_data import telemetry_to_features
from simulator.engine_simulator import EngineSimulator


def generate_rul_dataset(
    samples: int = 1000,
    seed: int = 42,
):
    """
    Generate synthetic engine degradation data
    for RUL model development.

    Returns:
        X -> telemetry features
        y -> remaining useful life in hours
    """

    simulator = EngineSimulator(seed=seed)

    X = []
    y = []

    max_life = 1000.0

    for step in range(samples):
        telemetry = simulator.generate(fault="normal")

        features = telemetry_to_features(telemetry)

        degradation_ratio = min(1.0, step / samples)

        remaining_life = max_life * (1.0 - degradation_ratio)

        X.append(features)
        y.append(max(0.0, remaining_life))

    return (
        np.asarray(X, dtype=float),
        np.asarray(y, dtype=float),
    )
