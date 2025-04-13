import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/kms/auth/login"

CREDENTIALS = {
    "email": "test@example.com",
    "password": "password"
}


def test_login():
    try:
        data = {k: (None, v) for k, v in CREDENTIALS.items()}

        response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            files=data
        )

        if response.status_code == 200:
            logger.info("✅ Login successful!")
            token = response.json().get("access_token")
            logger.info(f"Token: {token}")
            return token
        else:
            logger.error(f"❌ Login failed with status {response.status_code}")
            logger.error(f"Response: {response.text}")
            return None

    except Exception as e:
        logger.error(f"🚨 Exception during login test: {str(e)}")
        return None


if __name__ == "__main__":
    logger.info("Starting login test...")
    token = test_login()
    if token:
        logger.info("Test completed successfully!")
    else:
        logger.error("Test failed!")