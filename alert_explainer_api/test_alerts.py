from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def test_create_alert(client):
    alert_data = {
        "title": "High CPU usage",
        "severity": "critical",
        "source": "web-server",
        "metric_name": "cpu_usage",
        "metric_value": 95.0,
        "threshold": 80.0,
    }

    response = client.post("/alerts/", json=alert_data)

    assert response.status_code == 201
    created_alert = response.json()
    assert created_alert["id"] == 1
    assert created_alert["title"] == alert_data["title"]
    assert created_alert["severity"] == alert_data["severity"]
    assert created_alert["metric_name"] == alert_data["metric_name"]
    assert "created_at" in created_alert


def test_list_alerts(client):
    alert_data = {
        "title": "High CPU usage",
        "severity": "critical",
        "source": "web-server",
        "metric_name": "cpu_usage",
        "metric_value": 95.0,
        "threshold": 80.0,
    }
    client.post("/alerts/", json=alert_data)
    client.post(
        "/alerts/",
        json={
            **alert_data,
            "title": "High memory usage",
            "severity": "warning",
            "metric_name": "memory_usage",
        },
    )

    response = client.get("/alerts/")

    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) == 2
    assert [alert["id"] for alert in alerts] == [1, 2]
    assert [alert["metric_name"] for alert in alerts] == [
        "cpu_usage",
        "memory_usage",
    ]


def test_get_alert_by_id(client):
    alert_data = {
        "title": "High CPU usage",
        "severity": "critical",
        "source": "web-server",
        "metric_name": "cpu_usage",
        "metric_value": 95.0,
        "threshold": 80.0,
    }
    created_alert = client.post("/alerts/", json=alert_data).json()

    response = client.get(f"/alerts/{created_alert['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created_alert["id"]
    assert response.json()["title"] == alert_data["title"]
    assert response.json()["severity"] == alert_data["severity"]
    assert response.json()["metric_name"] == alert_data["metric_name"]


def test_explain_alert(client):
    alert_data = {
        "title": "High CPU usage",
        "severity": "critical",
        "source": "web-server",
        "metric_name": "cpu_usage",
        "metric_value": 95.0,
        "threshold": 80.0,
    }
    created_alert = client.post("/alerts/", json=alert_data).json()

    response = client.post(f"/alerts/{created_alert['id']}/explain")

    assert response.status_code == 200
    explanation = response.json()
    assert explanation["alert_id"] == created_alert["id"]
    assert alert_data["severity"] in explanation["explanation"]
    assert alert_data["metric_name"] in explanation["explanation"]
    generated_at = datetime.fromisoformat(explanation["generated_at"])
    assert generated_at.tzinfo is not None