from ml.training_data import (
    FEATURE_NAMES,
    generate_training_data,
)


def test_training_data():

    data = generate_training_data(samples=100)

    assert data.shape == (100, 8)

    assert len(FEATURE_NAMES) == 8

    assert data[:, 0].min() > 0
    assert data[:, 1].min() > 0
    assert data[:, 2].min() > 0
    assert data[:, 5].min() > 0


if __name__ == "__main__":
    test_training_data()

    print("Training data generation tests passed!")
