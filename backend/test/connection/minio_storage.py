from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("MINIO_ENDPOINT")
access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")
secure = os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "t")

# Initialize MinIO client
client = Minio(
    endpoint=endpoint,
    access_key=access_key,
    secret_key=secret_key,
    secure=secure
)

try:
    buckets = client.list_buckets()
    print("✅ Successfully connected to MinIO!")
    print("📦 Buckets found:")
    for bucket in buckets:
        print(f" - {bucket.name}")

    bucket_name = "ttu-storage"

    print(f"📄 Objects in bucket '{bucket_name}':")
    objects = client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        print(f" - {obj.object_name}")
except S3Error as e:
    print("❌ Connection to MinIO failed:", e)
