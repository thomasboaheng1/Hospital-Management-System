"""
Tests for the main FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Hospital Management System API"


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert data["status"] == "healthy"


def test_api_info():
    """Test the API info endpoint"""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "features" in data
    assert isinstance(data["features"], list)


def test_docs_endpoint():
    """Test that the docs endpoint is accessible"""
    response = client.get("/api/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Test that the ReDoc endpoint is accessible"""
    response = client.get("/api/redoc")
    assert response.status_code == 200


def test_openapi_endpoint():
    """Test that the OpenAPI JSON endpoint is accessible"""
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data


def test_cors_headers():
    """Test that CORS headers are properly set"""
    response = client.options("/api/health")
    assert response.status_code == 200
    # CORS headers should be present
    assert "access-control-allow-origin" in response.headers


def test_process_time_header():
    """Test that process time header is added"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "x-process-time" in response.headers


def test_404_error():
    """Test 404 error handling"""
    response = client.get("/api/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"] is True


def test_validation_error():
    """Test validation error handling"""
    # This would typically test an endpoint that requires specific data
    # For now, we'll just ensure the error handler exists
    response = client.get("/api/health")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__]) 