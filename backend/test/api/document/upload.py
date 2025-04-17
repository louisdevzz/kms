import requests
import logging
import io
from backend.test.api.auth.login import test_login
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = "/kms/document"
TEST_FILE_NAME = "TestFile.txt"
TEST_FILE_MIMETYPE = "text/plain"


def upload_document_with_token(token):
    try:
        content = "This is a test text file.\nUploaded via Python requests using BytesIO."
        file = io.BytesIO(content.encode("utf-8"))
        file.name = TEST_FILE_NAME

        metadata = {
            "name": "Test Text Document",
            "doc_type": "text",
            "department_id": "dept_123",
            # "tags": json.dumps(["text", "sample", "test"]),
            "tags": ["test", "example"],
            "owner": "test@example.com",
            "category": "testing",
            "description": "Test text file upload",
            "university": "Test University"
        }

        files = {
            'document': (
                file.name,
                file,
                TEST_FILE_MIMETYPE
            )
        }

        form_data = []
        for key, value in metadata.items():
            if key == "tags" and isinstance(value, list):
                for item in value:
                    form_data.append((key, str(item)))
            else:
                form_data.append((key, str(value)))

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response = requests.post(
            f"{BASE_URL}{UPLOAD_ENDPOINT}?self=true",
            files=files,
            data=form_data,
            headers=headers
        )

        if response.status_code == 200:
            logger.info(f"✅ Text document upload successful!")
            return response.json()
        else:
            logger.error(f"❌ Upload failed with status {response.status_code}")
            return {"error": response.text}

    except Exception as e:
        logger.error(f"🚨 Exception during upload test: {str(e)}", exc_info=True)
        return {"error": str(e)}


if __name__ == "__main__":
    logger.info("Starting manual text document upload...")
    token = test_login()

    if token:
        result = upload_document_with_token(token)
        print("🔁 Upload result:", result)
    else:
        print("❌ Login failed — cannot upload document.")
