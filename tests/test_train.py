from unittest.mock import MagicMock

import numpy as np
from omegaconf import OmegaConf
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from heart_failure_prediction.train import (
    build_pipeline,
    evaluate,
    split_data,
)


@pytest.fixture
def dummy_data():
    return pd.DataFrame(
        {
            'age': [50, 60, 70, 80] * 10,
            'creatinine': [1.0, 1.2, 0.8, 1.5] * 10,
            'sex': ['M', 'F', 'M', 'F'] * 10,
            'target': [0, 1, 0, 1] * 10,
        }
    )


@pytest.fixture
def dummy_config():
    conf = OmegaConf.create(
        {
            'processing': {
                'missing_vals_cols': ['creatinine'],
                'num_features': ['age', 'creatinine'],
                'cat_features': ['sex'],
                'num_impute_strategy': 'median',
                'cat_impute_strategy': 'most_frequent',
            },
            'model': {
                'target': 'target',
                'test_size': 0.25,
                'random_state': 42,
                'estimator': {
                    '_target_': 'sklearn.ensemble.RandomForestClassifier',
                    'n_estimators': 10,
                },
            },
        }
    )
    return conf


def test_split_data_shapes(dummy_config, dummy_data):
    X_train, X_test, y_train, y_test = split_data(dummy_config, dummy_data)

    assert 'target' not in X_train.columns
    assert 'target' not in X_test.columns

    assert len(X_test) == 10
    assert len(X_train) == 30
    assert len(y_test) == 10
    assert len(y_train) == 30


def test_evaluate_metrics():
    mock_model = MagicMock()
    # y_true = [1, 0, 1, 0]
    # y_pred = [1, 0, 0, 0]
    # Accuracy = 3/4 = 0.75
    # Recall (for 1) = 1/2 = 0.5
    mock_model.predict.return_value = np.array([1, 0, 0, 0])

    X_test = np.array([[1], [2], [3], [4]])  # Dummy input
    y_test = np.array([1, 0, 1, 0])

    scores = evaluate(mock_model, X_test, y_test)

    assert scores['accuracy'] == 0.75
    assert scores['recall'] == 0.5
    assert 'f1_score' in scores
    assert 'precision' in scores


def test_build_pipeline_structure(dummy_config):
    pipeline = build_pipeline(dummy_config)

    assert isinstance(pipeline, Pipeline)
    assert 'preprocessing' in pipeline.named_steps
    assert 'model' in pipeline.named_steps

    preprocessor = pipeline.named_steps['preprocessing']

    transformers = preprocessor.transformers

    num_step = [t for t in transformers if t[0] == 'num_pipeline'][0]
    assert num_step[2] == ['age', 'creatinine']  # Columns from dummy_config
