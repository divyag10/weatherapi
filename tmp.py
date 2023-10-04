from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_outfit_recommendation():
    # Test the outfit recommendation
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_read_root_with_query_param():
    # Test the root endpoint with a query parameter
    response = client.get("/?name=John")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, John!"}

def test_read_nonexistent_endpoint():
    # Test a nonexistent endpoint
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}