import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from core.rag.retriever import retrieve, project_has_chunks

@patch("core.rag.retriever._get_chroma_client")
@patch("core.rag.retriever.get_model")
def test_retrieve_returns_matching_chunks(mock_get_model, mock_get_client, tmp_path):
    class MockEmbedding:
        def tolist(self):
            return [[0.1, 0.2]]
            
    # Setup mock model
    mock_model = MagicMock()
    mock_model.encode.return_value = MockEmbedding()
    mock_get_model.return_value = mock_model
    
    # Setup mock ChromaDB client
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client
    
    # Setup mock collection data
    mock_collection.count.return_value = 5
    mock_collection.query.return_value = {
        "documents": [["def foo():\n    pass", "def bar():\n    pass"]],
        "metadatas": [[
            {"file_path": "foo.py", "start_line": 1, "project_root": str(tmp_path)},
            {"file_path": "bar.py", "start_line": 10, "project_root": str(tmp_path)}
        ]],
        "distances": [[0.1, 0.2]]
    }
    
    res = retrieve("query", str(tmp_path), top_k=2)
    
    assert len(res) == 2
    assert res[0]["content"] == "def foo():\n    pass"
    assert res[0]["file_path"] == "foo.py"
    assert res[0]["start_line"] == 1
    
    assert res[1]["content"] == "def bar():\n    pass"
    
    mock_collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2]],
        n_results=2,
        where={"project_root": str(tmp_path.resolve())}
    )

@patch("core.rag.retriever._get_chroma_client")
@patch("core.rag.retriever.get_model")
def test_retrieve_handles_missing_collection(mock_get_model, mock_get_client, tmp_path):
    mock_client = MagicMock()
    # Mock chroma db exception for missing collection
    mock_client.get_collection.side_effect = ValueError("Collection not found")
    mock_get_client.return_value = mock_client
    
    res = retrieve("query", tmp_path)
    assert res == []

@patch("core.rag.retriever._get_chroma_client")
def test_project_has_chunks(mock_get_client, tmp_path):
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client
    
    # Collection exists, query returns 1 item
    mock_collection.get.return_value = {"ids": ["1"]}
    assert project_has_chunks(tmp_path) is True
    
    mock_collection.get.assert_called_once_with(
        where={"project_root": str(tmp_path.resolve())},
        limit=1
    )
    
    # Collection exists, query returns 0 items
    mock_collection.get.return_value = {"ids": []}
    assert project_has_chunks(tmp_path) is False

@patch("core.rag.retriever._get_chroma_client")
def test_project_has_chunks_missing_collection(mock_get_client, tmp_path):
    mock_client = MagicMock()
    mock_client.get_collection.side_effect = ValueError("Collection not found")
    mock_get_client.return_value = mock_client
    
    assert project_has_chunks(tmp_path) is False

@patch("core.rag.retriever._get_chroma_client")
@patch("core.rag.retriever.get_model")
def test_retrieve_handles_absolute_relative_equivalence(mock_get_model, mock_get_client, tmp_path):
    import os
    
    class MockEmbedding:
        def tolist(self):
            return [[0.1, 0.2]]
            
    mock_model = MagicMock()
    mock_model.encode.return_value = MockEmbedding()
    mock_get_model.return_value = mock_model
    
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_collection.return_value = mock_collection
    mock_get_client.return_value = mock_client
    
    mock_collection.count.return_value = 5
    mock_collection.query.return_value = {
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]]
    }
    
    # Change current working directory to tmp_path temporarily
    old_cwd = os.getcwd()
    os.chdir(str(tmp_path))
    try:
        # relative path "."
        retrieve("query", ".", top_k=5)
        
        # Should be resolved to absolute path
        mock_collection.query.assert_called_once_with(
            query_embeddings=[[0.1, 0.2]],
            n_results=5,
            where={"project_root": str(tmp_path.resolve())}
        )
    finally:
        os.chdir(old_cwd)
