import os
import sys
import logging
from io import BytesIO
from dotenv import load_dotenv

# Fix the import path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from dao.minio_module.storage import MinIOStorage
from utils.config_loader import get_storage_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_minio_connection():
    """Test MinIO connection and operations."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get MinIO configuration
        minio_config = get_storage_config()
        logger.info(f"MinIO endpoint: {minio_config['endpoint']}")
        
        # Initialize MinIO storage
        minio = MinIOStorage(
            endpoint=minio_config['endpoint'],
            access_key=minio_config['access_key'],
            secret_key=minio_config['secret_key'],
            bucket_name=minio_config['bucket_name'],
            secure=minio_config.get('secure')
        )
        
        logger.info("MinIO storage initialized successfully!")
        
        # Create test content
        test_content = BytesIO(b"This is a test file to verify MinIO connection.")
        test_size = test_content.getbuffer().nbytes
        test_object_name = "connection_test/test.txt"
        
        # Try to upload
        logger.info(f"Attempting to upload test file: {test_object_name}")
        upload_success = minio.addDoc(
            object_name=test_object_name,
            data=test_content,
            length=test_size,
            content_type="text/plain"
        )
        
        if upload_success:
            logger.info("✅ Upload test successful!")
        else:
            logger.error("❌ Upload test failed!")
            return False
        
        # Try to download
        logger.info(f"Attempting to download test file: {test_object_name}")
        downloaded = minio.getDoc(test_object_name)
        
        if downloaded:
            content = downloaded.read()
            logger.info(f"✅ Download test successful! Content: {content.decode('utf-8')}")
            downloaded.close()
        else:
            logger.error("❌ Download test failed!")
            return False
        
        # Try to delete
        logger.info(f"Attempting to delete test file: {test_object_name}")
        delete_success = minio.deleteDoc(test_object_name)
        
        if delete_success:
            logger.info("✅ Delete test successful!")
        else:
            logger.error("❌ Delete test failed!")
            return False
        
        logger.info("✅ All MinIO tests passed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing MinIO connection: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    test_minio_connection() 