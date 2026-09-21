import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ner_logix")
DATABASE_REQUIRED = os.getenv("DATABASE_REQUIRED", "false").lower() == "true"
SERVER_SELECTION_TIMEOUT_MS = int(
    os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "2000")
)

client = AsyncMongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
)
db = client[DATABASE_NAME]


async def check_database_connection():
    try:
        await client.admin.command("ping")
        print("MongoDB connection successful!")
    except Exception as exc:
        message = f"MongoDB connection failed: {exc}"

        if DATABASE_REQUIRED:
            raise RuntimeError(message) from exc

        print(f"Warning: {message} (continuing in fallback demo mode)")
