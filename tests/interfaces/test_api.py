from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import httpx

from interfaces.api.main import app

client = TestClient(app)

@patch("interfaces.api.main.index_directory")
def test_index_endpoint(mock_index):
    mock_index.return_value = {"files_indexed": 1, "chunks_indexed": 2}
    response = client.post("/index", json={"path": "/fake/path"})
    assert response.status_code == 200
    assert response.json() == {"files_indexed": 1, "chunks_indexed": 2}
    mock_index.assert_called_once_with("/fake/path")

@patch("interfaces.api.main.project_has_chunks")
def test_chat_returns_not_indexed_when_no_chunks(mock_has_chunks):
    mock_has_chunks.return_value = False
    response = client.post("/chat", json={"message": "hello", "project_root": "/fake/path"})
    assert response.status_code == 200
    assert response.json() == {"response": "Project not indexed"}

@patch("interfaces.api.main.project_has_chunks")
@patch("interfaces.api.main.retrieve")
def test_chat_returns_not_found_when_no_retrieval(mock_retrieve, mock_has_chunks):
    mock_has_chunks.return_value = True
    mock_retrieve.return_value = []
    response = client.post("/chat", json={"message": "hello", "project_root": "/fake/path"})
    assert response.status_code == 200
    assert response.json() == {"response": "I don't see that"}

@patch("interfaces.api.main.project_has_chunks")
@patch("interfaces.api.main.retrieve")
@patch("interfaces.api.main.httpx.AsyncClient")
def test_chat_returns_503_when_ollama_down(mock_client_class, mock_retrieve, mock_has_chunks):
    mock_has_chunks.return_value = True
    mock_retrieve.return_value = [{"content": "foo", "file_path": "bar.py", "start_line": 1}]
    
    mock_client_instance = AsyncMock()
    mock_client_instance.__aenter__.return_value = mock_client_instance
    mock_client_instance.post.side_effect = httpx.ConnectError("down")
    mock_client_class.return_value = mock_client_instance
    
    response = client.post("/chat", json={"message": "hello", "project_root": "/fake/path"})
    assert response.status_code == 503

@patch("interfaces.api.main.project_has_chunks")
@patch("interfaces.api.main.retrieve")
@patch("interfaces.api.main.httpx.AsyncClient")
def test_chat_returns_502_on_http_error(mock_client_class, mock_retrieve, mock_has_chunks):
    mock_has_chunks.return_value = True
    mock_retrieve.return_value = [{"content": "foo", "file_path": "bar.py", "start_line": 1}]
    
    mock_client_instance = AsyncMock()
    mock_client_instance.__aenter__.return_value = mock_client_instance
    
    response_mock = MagicMock()
    response_mock.raise_for_status.side_effect = httpx.HTTPStatusError("502", request=AsyncMock(), response=AsyncMock())
    mock_client_instance.post.return_value = response_mock
    mock_client_class.return_value = mock_client_instance
    
    response = client.post("/chat", json={"message": "hello", "project_root": "/fake/path"})
    assert response.status_code == 502

@patch("interfaces.api.main.project_has_chunks")
@patch("interfaces.api.main.retrieve")
@patch("interfaces.api.main.httpx.AsyncClient")
def test_chat_success(mock_client_class, mock_retrieve, mock_has_chunks):
    mock_has_chunks.return_value = True
    mock_retrieve.return_value = [{"content": "foo", "file_path": "bar.py", "start_line": 1}]
    
    mock_client_instance = AsyncMock()
    mock_client_instance.__aenter__.return_value = mock_client_instance
    
    response_mock = MagicMock()
    response_mock.json.return_value = {"response": "Ollama response"}
    mock_client_instance.post.return_value = response_mock
    mock_client_class.return_value = mock_client_instance
    
    response = client.post("/chat", json={"message": "hello", "project_root": "/fake/path"})
    assert response.status_code == 200
    assert response.json() == {
        "response": "Ollama response",
        "sources": [{"file_path": "bar.py", "start_line": 1}]
    }
