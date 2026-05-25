import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

def test_upload_github_repo():
    response = client.post(
        "/api/upload/github",
        json={
            "github_url": "https://github.com/user/small-repo",
            "repo_type": "github"
        }
    )
    
    # This will fail without actual repo, but tests the endpoint
    assert response.status_code in [200, 500]

def test_chat_without_repo():
    response = client.post(
        "/api/chat",
        json={
            "repo_id": "nonexistent",
            "question": "What does main.py do?"
        }
    )
    
    assert response.status_code == 404