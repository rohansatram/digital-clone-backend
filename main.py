from fastapi import FastAPI
from apis import health, upload

app = FastAPI(
    title="Digital Clone API",
    description="Upload files (text, PDFs, images) to build your digital clone.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(upload.router)
