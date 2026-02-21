from openai import OpenAI
from services.embedder import _model, _collection
import os

LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "local-model")

_lm_client = OpenAI(base_url=LMSTUDIO_BASE_URL, api_key="not-needed")

SYSTEM_PROMPT = (
  "You are a helpful digital clone assistant. "
  "Answer the user's question based ONLY on the context provided below. "
  "If the context doesn't contain enough information, say so honestly. "
  "Always cite which source file the information came from.\n\n"
  "Context:\n{context}"
)


def retrieve(query: str, top_k: int = 5) -> list[dict]:
  """Embed the query and search ChromaDB for the most relevant chunks."""
  query_embedding = _model.encode([query]).tolist()
  results = _collection.query(
    query_embeddings=query_embedding,
    n_results=top_k,
  )

  chunks = []
  for i in range(len(results["documents"][0])):
    chunks.append({
      "text": results["documents"][0][i],
      "filename": results["metadatas"][0][i].get("filename", "unknown"),
      "chunk_index": results["metadatas"][0][i].get("chunk_index", 0),
    })
  return chunks


def build_messages(query: str, chunks: list[dict]) -> list[dict]:
  """Build the message list for the LLM with context from retrieved chunks."""
  context = "\n\n".join(
    f"[Source: {c['filename']}]\n{c['text']}" for c in chunks
  )
  return [
    {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
    {"role": "user", "content": query},
  ]


def ask_lm_studio_stream(query: str, chunks: list[dict]):
  """Stream tokens from LM Studio. Yields string chunks."""
  messages = build_messages(query, chunks)
  stream = _lm_client.chat.completions.create(
    model=LMSTUDIO_MODEL,
    messages=messages,
    stream=True,
  )
  for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
      yield delta.content
