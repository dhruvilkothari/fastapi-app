from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to FastAPI DevOps Project"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_application_info(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)

    response = client.get("/api/v1/info")

    assert response.status_code == 200
    data = response.json()

    assert data["application"] == "FastAPI DevOps Project"
    assert data["version"] == "1.0.0"
    assert data["environment"] == "development"


def test_application_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")

    response = client.get("/api/v1/info")

    assert response.status_code == 200
    assert response.json()["environment"] == "production"