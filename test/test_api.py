from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "🔥 FIRMS API is running!"}

def test_get_fires():
    response = client.get("/fires")
    assert response.status_code == 200
    assert "fires" in response.json()