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
    json={"question": question} 
    )

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == question
    assert "answer" in data



# import pytest
# from fastapi.testclient import TestClient
# from app.main import app

# @pytest.fixture
# def client():
#     return TestClient(app)

# @pytest.fixture
# def auth_token(client):

#     client.post("/register", json={
#         "username": "test",
#         "email": "test@test.com",
#         "password": "test123"
#     })

#     response = client.post("/login", json={
#         "username": "test",
#         "password": "test123"
#     })
#     return response.json()["token"]




# from unittest.mock import patch

# @patch('app.main.rag_chain')
# @patch('app.main.cluster')

# def test_query(mock_cluster, mock_rag, client, auth_token):
#     mock_cluster.return_value = 1
#     mock_rag.invoke.return_value = {"result": "Contactez support@example.com"}
    
#     response = client.post(
#         "/query",
#         json={"question": "Comment contacter le support IT ?"},
#         headers={"Authorization": f"Bearer {auth_token}"}
#     )
    
#     assert response.status_code == 200
#     assert "answer" in response.json()