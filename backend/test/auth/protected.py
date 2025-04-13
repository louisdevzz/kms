import requests
import logging
from login import test_login

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"
PROTECTED_ENDPOINT = "/kms/auth/me"


def test_protected(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}{PROTECTED_ENDPOINT}",
            headers=headers
        )

        if response.status_code == 200:
            logger.info("✅ Protected endpoint access successful!")
            logger.info(f"User data: {response.json()}")
            return True
        else:
            logger.error(f"❌ Failed to access protected endpoint: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False

    except Exception as e:
        logger.error(f"🚨 Exception during protected endpoint test: {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("Starting protected endpoint test...")

    # login first
    token = test_login()

    if token:
        if test_protected(token):
            logger.info("Test completed successfully!")
        else:
            logger.error("Failed to access protected endpoint")
    else:
        logger.error("Cannot test protected endpoint without valid token")