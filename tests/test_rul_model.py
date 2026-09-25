import numpy as np

from ml.rul_model import RULModel


def test_rul_model():

    rng = np.random.default_rng(42)

    X = rng.normal(size=(200, 8))

    y = np.linspace(1000, 0, 200)

    model = RULModel()

    model.train(X, y)

    predictions = model.predict(X[:5])

    assert len(predictions) == 5

    assert np.all(predictions >= 0)


def test_untrained_model():

    model = RULModel()

    X = np.zeros((1, 8))

    try:
        model.predict(X)

    except RuntimeError:
        return

    raise AssertionError("Untrained model should raise RuntimeError.")


if __name__ == "__main__":
    test_rul_model()
    test_untrained_model()

    print("RUL model tests passed!")
