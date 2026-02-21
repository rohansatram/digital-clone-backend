from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime, timezone
from database import fs_bucket, files_collection
import io

router = APIRouter()

SUPPORTED_CONTENT_TYPES = {
  "text/plain",
  "application/pdf",
  "image/jpeg",
  "image/png",
  "image/gif",
  "image/webp",
}


@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile = File(...)):
  """
  Upload a file (text, PDF, or image).

  The raw bytes are stored in MongoDB GridFS and the file metadata
  is stored in the `files` collection.
  """
  if file.content_type not in SUPPORTED_CONTENT_TYPES:
    raise HTTPException(
      status_code=415,
      detail=(
        f"Unsupported file type: '{file.content_type}'. "
        f"Supported types: {sorted(SUPPORTED_CONTENT_TYPES)}"
      ),
    )

  contents = await file.read()
  file_size = len(contents)

  if file_size == 0:
    raise HTTPException(status_code=400, detail="Uploaded file is empty.")

  # Store raw bytes in GridFS
  grid_in = fs_bucket.open_upload_stream(
    file.filename,
    metadata={
      "content_type": file.content_type,
      "uploaded_at": datetime.now(timezone.utc),
    },
  )
  await grid_in.write(contents)
  await grid_in.close()
  grid_file_id = grid_in._id

  # Store metadata in the files collection
  doc = {
    "filename": file.filename,
    "content_type": file.content_type,
    "size_bytes": file_size,
    "grid_file_id": grid_file_id,
    "uploaded_at": datetime.now(timezone.utc),
  }
  result = await files_collection.insert_one(doc)

  return {
    "message": "File uploaded successfully",
    "file_id": str(result.inserted_id),
    "grid_file_id": str(grid_file_id),
    "filename": file.filename,
    "content_type": file.content_type,
    "size_bytes": file_size,
  }