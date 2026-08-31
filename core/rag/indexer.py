from pathlib import Path
import logging
import os

from core.config import (
    EMBED_MODEL,
    CHROMA_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MAX_FILES,
    MAX_FILE_SIZE_KB,
    SUPPORTED_EXTENSIONS
)

_model = None

def get_model():
    global _model
    if _model is None:
        # Known limitation: _model is a module-level singleton loaded lazily. This avoids memory bloat but is not thread-safe under threaded/async workers. Acceptable for a local personal tool.
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBED_MODEL)
    return _model

def _chunk_lines(lines: list[str]) -> list[tuple[int, str]]:
    chunks = []
    i = 0
    while i < len(lines):
        end = min(i + CHUNK_SIZE, len(lines))
        chunk = "\n".join(lines[i:end])
        if chunk.strip():
            chunks.append((i + 1, chunk))
        i += max(1, CHUNK_SIZE - CHUNK_OVERLAP)
    return chunks

def should_index_file(path: Path) -> bool:
    if path.suffix not in SUPPORTED_EXTENSIONS:
        return False
    if path.stat().st_size > MAX_FILE_SIZE_KB * 1024:
        return False
    return True

def index_directory(path: str) -> dict:
    root = Path(path).resolve()
    
    files_to_index = []
    count = 0
    
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            p = Path(dirpath) / filename
            if should_index_file(p):
                count += 1
                if count > MAX_FILES:
                    raise ValueError(f"Too many files: {count} > {MAX_FILES}")
                files_to_index.append(p)
                
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name="code_index")
    
    collection.delete(where={"project_root": str(root)})
        
    model = get_model()
    total_chunks = 0
    
    ids = []
    documents = []
    metadatas = []
    
    for file_path in files_to_index:
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
            
        rel_path = str(file_path.relative_to(root))
        lines = content.splitlines()
        chunks = _chunk_lines(lines)
        
        for start_line, chunk_text in chunks:
            chunk_id = f"{root}::{rel_path}::{start_line}"
            
            ids.append(chunk_id)
            documents.append(chunk_text)
            metadatas.append({
                "project_root": str(root),
                "file_path": rel_path,
                "start_line": start_line
            })
            total_chunks += 1
            
    if documents:
        BATCH_SIZE = 256
        for i in range(0, len(documents), BATCH_SIZE):
            batch_docs = documents[i:i+BATCH_SIZE]
            batch_ids = ids[i:i+BATCH_SIZE]
            batch_metas = metadatas[i:i+BATCH_SIZE]
            batch_embs = model.encode(batch_docs).tolist()
            
            collection.add(
                ids=batch_ids,
                embeddings=batch_embs,
                documents=batch_docs,
                metadatas=batch_metas
            )
            
    return {
        "files_indexed": len(files_to_index),
        "chunks_indexed": total_chunks
    }
