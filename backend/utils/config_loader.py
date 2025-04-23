import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


def get_db_config() -> Dict[str, str]:
    username = os.getenv("MONGODB_USERNAME")
    password = os.getenv("MONGODB_PASSWORD")
    cluster = os.getenv("MONGODB_CLUSTER")
    db_name = os.getenv("MONGODB_DB_NAME")

    from urllib.parse import quote_plus
    encoded_password = quote_plus(password) if password else ""

    uri = f"mongodb+srv://{username}:{encoded_password}@{cluster}/"

    return {
        "uri": uri,
        "db_name": db_name
    }


def get_storage_config() -> Dict[str, str]:
    return {
        "endpoint": os.getenv("MINIO_ENDPOINT"),
        "access_key": os.getenv("MINIO_ACCESS_KEY"),
        "secret_key": os.getenv("MINIO_SECRET_KEY"),
        "bucket_name": os.getenv("MINIO_BUCKET_NAME"),
        "secure": os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "t")

    }


def get_collections() -> Dict[str, str]:
    return {
        "user_dao": os.getenv("USER_DAO"),
        "document_dao":  os.getenv("DOCUMENT_DAO"),
        "department_dao": os.getenv("DEPARTMENT_DAO"),
        "permission_dao": os.getenv("PERMISSION_DAO"),
        "activity_log_dao": os.getenv("ACTIVITY_LOG_DAO")
    }


def get_secret_key() -> str:
    return os.getenv("SECRET_KEY")
