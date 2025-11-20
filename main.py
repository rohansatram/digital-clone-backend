from fastapi import FastAPI
from apis import health

app = FastAPI()

app.include_router(health.router)
