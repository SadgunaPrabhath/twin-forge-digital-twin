import numpy as np

from simulator.engine_simulator import EngineSimulator

FEATURE_NAMES = [
    "rpm",
    "torque",
    "oil_temperature",
    "cylinder_head_temperature",
    "egt",
    "oil_pressure",
    "fuel_flow",
    "vibration",
]


def telemetry_to_features(telemetry) -> list:
    """
    Convert engine telemetry into ML features.
    """

    return [
        telemetry.rpm,
        telemetry.torque,
        telemetry.oil_temperature,
        telemetry.cylinder_head_temperature,
        telemetry.egt,
        telemetry.oil_pressure,
        telemetry.fuel_flow,
        telemetry.vibration,
    ]


def generate_training_data(
    samples: int = 1000,
    seed: int = 42,
) -> np.ndarray:
    """
    Generate normal engine operating data
    using the Digital Twin simulator.
    """

    simulator = EngineSimulator(seed=seed)

    data = []

    for _ in range(samples):
        telemetry = simulator.generate(fault="normal")

        features = telemetry_to_features(telemetry)

        data.append(features)

    return np.asarray(data, dtype=float)
