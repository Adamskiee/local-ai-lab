from pathlib import Path
import pytest


def test_config_constants():
    from models.config import (
        OLLAMA_URL,
        OLLAMA_MODEL,
        EMBED_MODEL,
        CHROMA_PATH,
        CHUNK_SIZE,
        CHUNK_OVERLAP,
        TOP_K,
        MAX_FILES,
        MAX_FILE_SIZE_KB,
        SUPPORTED_EXTENSIONS,
    )

    assert OLLAMA_URL == "http://localhost:11434"
    assert OLLAMA_MODEL == "qwen2.5:3b"
    assert EMBED_MODEL == "all-MiniLM-L6-v2"
    assert isinstance(CHROMA_PATH, Path)
    assert CHROMA_PATH.is_absolute()
    assert CHROMA_PATH.name == "chroma_db"
    assert CHUNK_SIZE == 50
    assert CHUNK_OVERLAP == 10
    assert TOP_K == 5
    assert MAX_FILES == 10_000
    assert MAX_FILE_SIZE_KB == 512
    assert isinstance(SUPPORTED_EXTENSIONS, set)
    expected_extensions = {
        ".py", ".js", ".ts", ".go", ".rs", ".java",
        ".c", ".cpp", ".md", ".yaml", ".yml", ".toml", ".json",
    }
    assert SUPPORTED_EXTENSIONS == expected_extensions
