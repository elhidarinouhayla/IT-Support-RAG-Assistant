import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_query(client):
    
    question = "Comment contacter le support IT ?"

    response = client.post(
        "/query",
        {"question": question} )

    assert response.status_code == 200
