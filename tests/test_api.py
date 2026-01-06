from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
import numpy as np
import pytest

from heart_failure_prediction.serving.app import app

client = TestClient(app)


@pytest.fixture
def dummy_valid_data():
    data = {
        'Age': 45,
        'Sex': 'M',
        'ChestPainType': 'ATA',
        'RestingBP': 130,
        'Cholesterol': 230,
        'FastingBS': 0,
        'RestingECG': 'Normal',
        'MaxHR': 140,
        'ExerciseAngina': 'N',
        'Oldpeak': 1.5,
        'ST_Slope': 'Flat',
    }
    return data


@pytest.fixture
def dummy_invalid_data():
    data = {
        'Age': -45,
        'Sex': 'M',
        'ChestPainType': 'ATA',
        'RestingBP': 130,
        'Cholesterol': 230,
        'FastingBS': 0,
        'MaxHR': 140,
        'ExerciseAngina': 'N',
        'Oldpeak': 1.5,
        'ST_Slope': 'Flat',
    }
    return data


def test_healthy():
    model = MagicMock()

    with patch('heart_failure_prediction.serving.app.artifacts', {'model': model}):
        response = client.get('/health')

    assert response.status_code == 200


def test_unhealthy():
    with patch('heart_failure_prediction.serving.app.artifacts', {}):
        response = client.get('/health')

    assert response.status_code == 503


def test_returns_correct_value(dummy_valid_data):
    model = MagicMock()
    model.predict.return_value = np.array([1])
    model.predict_proba.return_value = np.array([[0.2, 0.8]])

    with patch('heart_failure_prediction.serving.app.artifacts', {'model': model}):
        response = client.post(url='/predict', json=dummy_valid_data)

    assert response.status_code == 200
    assert response.json()['HeartDisease'] == 1
    assert response.json()['Probability-positive'] == 0.8
    assert response.json()['Probability-negative'] == 0.2


def test_rejects_invalid_data(dummy_invalid_data):
    response = client.post(url='/predict', json=dummy_invalid_data)

    assert response.status_code == 422


def test_explain_returns_correct_value(dummy_valid_data):
    model = MagicMock()
    explainer = MagicMock()
    feature_names = ['feature1', 'feature2']

    # Mock preprocessing
    preprocessor = MagicMock()
    preprocessor.transform.return_value = np.array([[1, 2]])
    model.named_steps = {'preprocessing': preprocessor}

    # Mock shap values
    explainer.shap_values.return_value = np.array([[0.1, -0.2]])

    artifacts = {
        'model': model,
        'explainer': explainer,
        'feature_names': feature_names,
    }

    with patch('heart_failure_prediction.serving.app.artifacts', artifacts):
        response = client.post(url='/explain', json=dummy_valid_data)

    assert response.status_code == 200
    json_response = response.json()
    keys = list(json_response.keys())
    assert keys[0] == 'feature2'
    assert keys[1] == 'feature1'
    assert json_response['feature1'] == 0.1
    assert json_response['feature2'] == -0.2


def test_explain_service_unavailable(dummy_valid_data):
    with patch('heart_failure_prediction.serving.app.artifacts', {}):
        response = client.post(url='/explain', json=dummy_valid_data)

    assert response.status_code == 503


def test_explain_rejects_invalid_data(dummy_invalid_data):
    response = client.post(url='/explain', json=dummy_invalid_data)

    assert response.status_code == 422


def test_explain_internal_server_error(dummy_valid_data):
    model = MagicMock()
    preprocessor = MagicMock()
    preprocessor.transform.side_effect = Exception('Transformation failed')
    model.named_steps = {'preprocessing': preprocessor}

    explainer = MagicMock()
    feature_names = ['feature1']

    artifacts = {
        'model': model,
        'explainer': explainer,
        'feature_names': feature_names,
    }

    with patch('heart_failure_prediction.serving.app.artifacts', artifacts):
        response = client.post(url='/explain', json=dummy_valid_data)

    assert response.status_code == 500
