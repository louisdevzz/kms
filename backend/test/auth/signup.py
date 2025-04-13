import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test configuration
BASE_URL = "http://localhost:8000"
SIGNUP_ENDPOINT = "/kms/auth/signup"

TEST_USER = {
    "email": "test@example.com",
    "password": "password",
    "name": "Test User",
    "department_id": "dept_123",
    "roles": ["user"]
}


def test_signup():
    try:
        data = {}

        for key, value in TEST_USER.items():
            if key == "roles":
                import json
                value = json.dumps(value)
            data[key] = (None, value)

        response = requests.post(
            f"{BASE_URL}{SIGNUP_ENDPOINT}",
            files=data
        )

        if response.status_code == 200:
            logger.info("✅ Signup successful!")
            logger.info(f"Response: {response.json()}")
            return True
        else:
            logger.error(f"❌ Signup failed with status {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False

    except Exception as e:
        logger.error(f"🚨 Exception during signup test: {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("Starting signup test...")
    success = test_signup()
    if success:
        logger.info("Test completed successfully!")
    else:
        logger.error("Test failed!")