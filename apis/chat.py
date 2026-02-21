from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.chat import retrieve, ask_lm_studio_stream
import json

router = APIRouter()


class ChatRequest(BaseModel):
  message: str


@router.post("/chat")
async def chat(request: ChatRequest):
  """
  RAG chat endpoint.
  Retrieves relevant chunks from ChromaDB, then streams
  the LLM response as Server-Sent Events (SSE).
  """
  chunks = retrieve(request.message)
  sources = list({c["filename"] for c in chunks})

  def event_stream():
    # Send sources first
    yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"

    # Stream LLM tokens
    for token in ask_lm_studio_stream(request.message, chunks):
      yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

    # Signal completion
    yield f"data: {json.dumps({'type': 'done'})}\n\n"

  return StreamingResponse(
    event_stream(),
    media_type="text/event-stream",
    headers={
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
    },
  )
