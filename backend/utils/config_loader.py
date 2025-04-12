from typing import Dict

# mongodb
MONGODB_URI = "mongodb://user:password@localhost:27017/"
MONGODB_DB_NAME = "university_db"

# minio
MINIO_ENDPOINT = "minio.example.com:9000"
MINIO_ACCESS_KEY = "your-access-key"
MINIO_SECRET_KEY = "your-secret-key"
MINIO_BUCKET_NAME = "documents"
MINIO_SECURE = False

# collections
user_dao = "users"
document_dao = "documents"
department_dao = "departments"
permission_dao = "permissions"
activity_log_dao = "activity_logs"

# secret_key
SECRET_KEY = "9u3nIzvDjVuT_w3Zo5pPUhd6_zWvUcR2wSPOTQjeUAg"


def get_db_config() -> Dict[str, str]:
    return {
        "uri": MONGODB_URI,
        "db_name": MONGODB_DB_NAME
    }


def get_storage_config() -> Dict[str, str]:
    return {
        "endpoint": MINIO_ENDPOINT,
        "access_key": MINIO_ACCESS_KEY,
        "secret_key": MINIO_SECRET_KEY,
        "bucket_name": MINIO_BUCKET_NAME,
        "secure": MINIO_SECURE
    }


def get_collections() -> Dict[str, str]:
    return {
        "user_dao": user_dao,
        "document_dao": document_dao,
        "department_dao": department_dao,
        "permission_dao": permission_dao,
        "activity_log_dao": activity_log_dao
    }


def get_secret_key() -> str:
    return SECRET_KEY
