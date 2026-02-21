from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from apis import health, upload, chat

load_dotenv()

app = FastAPI(
  title="Digital Clone API",
  description="Upload files (text, PDFs, images) to build your digital clone.",
  version="0.1.0",
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(chat.router)
