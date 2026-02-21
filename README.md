# Digital Clone

A FastAPI backend that lets you upload text, PDFs, and images to build a personal vector-searchable knowledge base — your digital clone.

---

## Prerequisites

- Python 3.10+
- MongoDB (see below)

---

## 1. Install MongoDB

`mongodb-community` is not in the default Homebrew tap. Add the official MongoDB tap first:

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

---

## 2. Set Up the Python Environment

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
```

Also install the system `tesseract` binary (for image OCR):

```bash
brew install tesseract
```

---

## 3. Run the Server

```bash
venv/bin/uvicorn main:app --reload
```

The API will be available at **http://127.0.0.1:8000**

> `--reload` enables hot-reloading on file changes (great for development).

---

## 4. Explore the API

FastAPI auto-generates interactive docs:

| UI | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/files` | List all uploaded files |
| `POST` | `/upload` | Upload a file (text, PDF, image) |
| `POST` | `/chat` | RAG chat — streams response via SSE |

### Upload a file (via curl)

```bash
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@/path/to/your/file.pdf;type=application/pdf"
```

Supported file types: `text/plain`, `application/pdf`, `image/jpeg`, `image/png`, `image/gif`, `image/webp`

### Chat (via curl)

```bash
curl -N -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is in my documents?"}'
```

> Requires **LM Studio** running with a model loaded and Local Server enabled (default port `1234`).

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MONGO_URI` | `mongodb://localhost:27017` | MongoDB connection string |
| `MONGO_DB_NAME` | `digital_clone` | Database name |
| `LMSTUDIO_BASE_URL` | `http://localhost:1234/v1` | LM Studio local server URL |
| `LMSTUDIO_MODEL` | `local-model` | Model name to use in LM Studio |

Create a `.env` file in the project root to override these.