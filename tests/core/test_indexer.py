import pytest
from pathlib import Path
from unittest.mock import patch
import shutil

from core.config import MAX_FILES, MAX_FILE_SIZE_KB, CHROMA_PATH, SUPPORTED_EXTENSIONS
from core.rag.indexer import index_directory, _chunk_lines

@pytest.fixture(autouse=True)
def clean_chroma(tmp_path_factory, monkeypatch):
    """
    Autouse fixture to clean up ChromaDB before each test.
    Note: this breaks pytest-xdist because it shares the same persistent DB.
    """
    test_chroma_path = tmp_path_factory.mktemp("chroma_db")
    monkeypatch.setattr("core.rag.indexer.CHROMA_PATH", test_chroma_path)
    monkeypatch.setattr("tests.core.test_indexer.CHROMA_PATH", test_chroma_path)
    
    import chromadb
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    yield test_chroma_path
    chromadb.api.client.SharedSystemClient.clear_system_cache()

@pytest.fixture(autouse=True)
def mock_get_model(monkeypatch):
    class MockModel:
        def encode(self, docs):
            import numpy as np
            return np.zeros((len(docs), 384))
    monkeypatch.setattr("core.rag.indexer.get_model", lambda: MockModel())

def test_chunk_lines():
    lines = ["line1", "line2", "line3", "line4", "line5"]
    with patch("core.rag.indexer.CHUNK_SIZE", 3), \
         patch("core.rag.indexer.CHUNK_OVERLAP", 1):
        chunks = _chunk_lines(lines)
    
    assert len(chunks) == 3
    assert chunks[0] == (1, "line1\nline2\nline3")
    assert chunks[1] == (3, "line3\nline4\nline5")
    assert chunks[2] == (5, "line5")

def test_index_directory_counts_files_and_chunks(tmp_path):
    f1 = tmp_path / "test1.py"
    f1.write_text("print('hello')\n" * 5)
    
    f2 = tmp_path / "test2.js"
    f2.write_text("console.log('world');\n")
    
    f3 = tmp_path / "test3.unsupported"
    f3.write_text("unsupported")
    
    with patch("core.rag.indexer.CHUNK_SIZE", 3), \
         patch("core.rag.indexer.CHUNK_OVERLAP", 1):
        result = index_directory(str(tmp_path))
        
    assert result["files_indexed"] == 2
    assert result["chunks_indexed"] == 4

def test_index_directory_max_files(tmp_path, monkeypatch):
    monkeypatch.setattr("core.rag.indexer.MAX_FILES", 5)
    for i in range(6):
        (tmp_path / f"test{i}.py").write_text("test")
        
    with pytest.raises(ValueError, match="Too many files"):
        index_directory(str(tmp_path))

def test_index_directory_skips_large_files(tmp_path, monkeypatch):
    monkeypatch.setattr("core.rag.indexer.MAX_FILE_SIZE_KB", 1)
    f1 = tmp_path / "normal.py"
    f1.write_text("normal")
    
    f2 = tmp_path / "large.py"
    f2.write_text("a" * (1 * 1024 + 10))
    
    result = index_directory(str(tmp_path))
    assert result["files_indexed"] == 1
    assert result["chunks_indexed"] == 1

def test_index_directory_stores_absolute_project_root_and_clears_old(tmp_path):
    f1 = tmp_path / "test1.py"
    f1.write_text("content")
    
    index_directory(str(tmp_path))
    
    import chromadb
    import core.rag.indexer
    client = chromadb.PersistentClient(path=str(core.rag.indexer.CHROMA_PATH))
    collection = client.get_collection("code_index")
    results = collection.get()
    
    assert len(results["ids"]) == 1
    metadata = results["metadatas"][0]
    
    assert metadata["project_root"] == str(tmp_path.resolve())
    assert metadata["file_path"] == "test1.py"
    
    old_id = results["ids"][0]
    
    f1.unlink()
    f2 = tmp_path / "test2.py"
    f2.write_text("test2")
    
    index_directory(str(tmp_path))
    
    results = collection.get()
    assert len(results["ids"]) == 1
    assert old_id not in results["ids"]

