import os
import sys
import logging
from minio import Minio
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_minio_direct():
    """Test MinIO connection directly without importing project modules."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get MinIO configuration from environment
        endpoint = os.getenv("MINIO_ENDPOINT")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        bucket_name = os.getenv("MINIO_BUCKET_NAME")
        secure = os.getenv("MINIO_SECURE", "false").lower() in ("true", "1", "t")
        
        logger.info(f"MinIO endpoint: {endpoint}")
        logger.info(f"Bucket name: {bucket_name}")
        logger.info(f"Secure connection: {secure}")
        
        # Initialize MinIO client
        client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        
        logger.info("MinIO client initialized successfully!")
        
        # Check if bucket exists
        if client.bucket_exists(bucket_name):
            logger.info(f"✅ Bucket '{bucket_name}' exists!")
        else:
            logger.warning(f"⚠️ Bucket '{bucket_name}' does not exist.")
            logger.info(f"Creating bucket '{bucket_name}'...")
            client.make_bucket(bucket_name)
            logger.info(f"✅ Bucket '{bucket_name}' created successfully!")
        
        # List objects in the bucket
        objects = list(client.list_objects(bucket_name, prefix="", recursive=True))
        logger.info(f"Found {len(objects)} objects in bucket")
        for obj in objects[:5]:  # Show just the first 5 to avoid overwhelming logs
            logger.info(f"Object: {obj.object_name}, Size: {obj.size} bytes")
        
        logger.info("✅ MinIO connection test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing MinIO connection: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    test_minio_direct() 