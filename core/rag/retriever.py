from pathlib import Path
import chromadb
from chromadb.errors import InvalidDimensionException

try:
    from chromadb.errors import NotFoundError
except ImportError:
    NotFoundError = ValueError

from core.config import CHROMA_PATH, TOP_K
from core.rag.indexer import get_model

_chroma_client = None

def _get_chroma_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return _chroma_client

def retrieve(query: str, project_root: str | Path, top_k: int = TOP_K) -> list[dict]:
    client = _get_chroma_client()
    try:
        col = client.get_collection(name="code_index")
    except (ValueError, NotFoundError):
        # ValueError is sometimes raised by older chromadb, NotFoundError by newer
        return []

    root_abs = str(Path(project_root).resolve())
    
    n_results = min(top_k, col.count())
    if n_results == 0:
        return []

    model = get_model()
    query_embeddings = model.encode([query]).tolist()

    res = col.query(
        query_embeddings=query_embeddings,
        n_results=n_results,
        where={"project_root": root_abs}
    )

    if not res or not res.get("documents") or not res["documents"][0]:
        return []

    chunks = []
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        chunks.append({
            "content": doc,
            "file_path": meta["file_path"],
            "start_line": meta["start_line"],
        })
    return chunks

def project_has_chunks(project_root: str | Path) -> bool:
    client = _get_chroma_client()
    try:
        col = client.get_collection(name="code_index")
    except (ValueError, NotFoundError):
        return False
        
    root_abs = str(Path(project_root).resolve())
    res = col.get(
        where={"project_root": root_abs},
        limit=1
    )
    return len(res.get("ids", [])) > 0
