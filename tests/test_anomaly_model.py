import numpy as np

from ml.anomaly_model import AnomalyModel


def test_anomaly_model():

    rng = np.random.default_rng(42)

    # Normal engine operating data
    normal_data = rng.normal(
        loc=0.0,
        scale=1.0,
        size=(100, 5),
    )

    model = AnomalyModel()

    model.train(normal_data)

    normal_sample = np.array([[0.1, -0.2, 0.3, -0.1, 0.2]])

    anomaly_sample = np.array([[10.0, 10.0, 10.0, 10.0, 10.0]])

    normal_prediction = model.predict(normal_sample)

    anomaly_prediction = model.predict(anomaly_sample)

    assert normal_prediction[0] == 1
    assert anomaly_prediction[0] == -1


def test_anomaly_score():

    rng = np.random.default_rng(42)

    normal_data = rng.normal(
        loc=0.0,
        scale=1.0,
        size=(100, 5),
    )

    model = AnomalyModel()

    model.train(normal_data)

    samples = np.array(
        [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [10.0, 10.0, 10.0, 10.0, 10.0],
        ]
    )

    scores = model.anomaly_score(samples)

    assert len(scores) == 2
    assert scores[1] > scores[0]


if __name__ == "__main__":
    test_anomaly_model()
    test_anomaly_score()

    print("ML anomaly model tests passed!")
