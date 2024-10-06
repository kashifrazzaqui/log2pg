import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from log2pg.api import app, get_stats_from_db
from datetime import datetime, timedelta
from collections import namedtuple

@pytest.fixture
def client():
    return TestClient(app)

def test_get_customer_stats(client):
    customer_id = "test_customer"
    from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    StatsResult = namedtuple('StatsResult', ['total_requests', 'successful_requests', 'failed_requests', 'avg_latency', 'median_latency', 'p99_latency'])
    mock_result = StatsResult(100, 90, 10, 0.25, 0.2, 0.5)

    with patch('log2pg.api.get_stats_from_db', return_value=mock_result):
        response = client.get(f"/customers/{customer_id}/stats?from_date={from_date}")

    assert response.status_code == 200
    data = response.json()
    assert data["total_requests"] == 100
    assert data["successful_requests"] == 90
    assert data["failed_requests"] == 10
    assert data["uptime"] == "90.00%"
    assert data["avg_latency"] == "0.25ms"
    assert data["median_latency"] == "0.20ms"
    assert data["p99_latency"] == "0.50ms"

def test_get_customer_stats_no_data(client):
    customer_id = "non_existent"
    from_date = datetime.now().strftime("%Y-%m-%d")

    StatsResult = namedtuple('StatsResult', ['total_requests', 'successful_requests', 'failed_requests', 'avg_latency', 'median_latency', 'p99_latency'])
    mock_result = StatsResult(0, 0, 0, None, None, None)

    with patch('log2pg.api.get_stats_from_db', return_value=mock_result):
        response = client.get(f"/customers/{customer_id}/stats?from_date={from_date}")

    assert response.status_code == 404
    assert "No data found" in response.json()["detail"]

def test_get_customer_stats_invalid_date(client):
    customer_id = "test_customer"
    invalid_date = "invalid-date"

    response = client.get(f"/customers/{customer_id}/stats?from_date={invalid_date}")

    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]

def test_get_customer_stats_zero_requests(client):
    customer_id = "test_customer"
    from_date = datetime.now().strftime("%Y-%m-%d")

    StatsResult = namedtuple('StatsResult', ['total_requests', 'successful_requests', 'failed_requests', 'avg_latency', 'median_latency', 'p99_latency'])
    mock_result = StatsResult(0, 0, 0, None, None, None)

    with patch('log2pg.api.get_stats_from_db', return_value=mock_result):
        response = client.get(f"/customers/{customer_id}/stats?from_date={from_date}")

    assert response.status_code == 404
    assert "No data found" in response.json()["detail"]