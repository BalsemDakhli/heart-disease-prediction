import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Cas nominal : envoi de données complètes et valides
def test_predict_success(client):
    payload = {
        "age": 54,
        "sex": 1,
        "cp": 0,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 1,
        "thalach": 187,
        "exang": 0,
        "oldpeak": 1.5,
        "slope": 2,
        "ca": 0,
        "thal": 2,
        "nom": "Test",
        "prenom": "User"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "heart_disease_risk" in data
    assert "probability" in data
    assert "recommendation" in data

# Test avec données manquantes (incomplètes)
def test_predict_missing_fields(client):
    payload = {
        "age": 54,
        "sex": 1
        # Champs manquants volontairement
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400  # ou 500 selon implémentation

# Test avec mauvaise donnée (type incorrect)
def test_predict_invalid_type(client):
    payload = {
        "age": "fifty",  # Mauvais type ici (str au lieu d'int)
        "sex": 1,
        "cp": 0,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 1,
        "thalach": 187,
        "exang": 0,
        "oldpeak": 1.5,
        "slope": 2,
        "ca": 0,
        "thal": 2,
        "nom": "Error",
        "prenom": "Test"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400  # on attend un Bad Request
    data = response.get_json()
    assert "error" in data
    # Optionnel : vérifier que le message mentionne un problème de type
    assert any(word in data["error"].lower() for word in ["type", "numeric", "value"])

