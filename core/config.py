from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "qwen2.5:3b"
EMBED_MODEL = "all-MiniLM-L6-v2"
CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"
CHUNK_SIZE = 50
CHUNK_OVERLAP = 10
TOP_K = 5
MAX_FILES = 10_000
MAX_FILE_SIZE_KB = 512
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".go", ".rs", ".java",
    ".c", ".cpp", ".md", ".yaml", ".yml", ".toml", ".json",
}
