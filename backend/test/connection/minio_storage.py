from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
from utils.config_loader import get_storage_config

load_dotenv()

config = get_storage_config()
endpoint = config['endpoint']
access_key = config['access_key']
secret_key = config['secret_key']
secure = config['secure']

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
