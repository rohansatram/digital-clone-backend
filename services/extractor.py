import io
from pypdf import PdfReader
from PIL import Image
import pytesseract


def extract_text(content: bytes, content_type: str) -> str:
  """
  Extract plain text from uploaded file bytes.
  Supports: text/plain, application/pdf, image/*
  """
  if content_type == "text/plain":
    return content.decode("utf-8", errors="ignore")

  if content_type == "application/pdf":
    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()

  if content_type.startswith("image/"):
    image = Image.open(io.BytesIO(content))
    return pytesseract.image_to_string(image).strip()

  return ""
