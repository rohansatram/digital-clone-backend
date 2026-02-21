import chromadb
from sentence_transformers import SentenceTransformer
import os

# Persistent ChromaDB stored in ./chroma_db/
CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

_chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _chroma_client.get_or_create_collection(name="digital_clone")

_model = SentenceTransformer("all-MiniLM-L6-v2")


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
  """Split text into overlapping chunks."""
  chunks = []
  start = 0
  while start < len(text):
    end = start + chunk_size
    chunks.append(text[start:end].strip())
    start += chunk_size - overlap
  return [c for c in chunks if c]  # filter empty chunks


def embed_and_store(text: str, file_id: str, filename: str) -> int:
  """
  Chunk the text, embed each chunk, and store in ChromaDB.
  Returns the number of chunks stored.
  """
  chunks = _chunk_text(text)
  if not chunks:
    return 0

  embeddings = _model.encode(chunks).tolist()

  _collection.add(
    ids=[f"{file_id}_chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=embeddings,
    metadatas=[
      {"file_id": file_id, "filename": filename, "chunk_index": i}
      for i in range(len(chunks))
    ],
  )

  return len(chunks)
