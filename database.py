import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "digital_clone")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# GridFS bucket for storing raw file bytes (PDFs, images, etc.)
fs_bucket = AsyncIOMotorGridFSBucket(db, bucket_name="uploads")

# Collection for file metadata
files_collection = db["files"]
