import requests
import logging
import pytest

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

# API Configuration
BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/kms/auth/login"
PROTECTED_ENDPOINT = "/kms/auth/me"

# Test credentials
CREDENTIALS = {
    "email": "test@example.com",
    "password": "password"
}


@pytest.fixture
def token():
    """Pytest fixture to get authentication token"""
    try:
        data = {k: (None, v) for k, v in CREDENTIALS.items()}
        response = requests.post(
            f"{BASE_URL}{LOGIN_ENDPOINT}",
            files=data
        )

        if response.status_code == 200:
            token = response.json().get("access_token")
            logger.info("\n✅ Login successful (fixture)")
            return token
        else:
            logger.error(f"❌ Login failed: {response.status_code}")
            pytest.fail("Login failed")

    except Exception as e:
        logger.error(f"🚨 Login exception: {str(e)}")
        pytest.fail(f"Login exception: {str(e)}")


def test_protected_endpoint(token):
    """Test accessing protected endpoint with valid token"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}{PROTECTED_ENDPOINT}",
            headers=headers
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        logger.info("\n✅ Protected endpoint access successful")
        logger.info(f"User: {response.json()}")

    except Exception as e:
        logger.error(f"🚨 Protected endpoint exception: {str(e)}")
        pytest.fail(f"Protected endpoint exception: {str(e)}")


if __name__ == "__main__":

    # login first
    token = token()

    test_protected_endpoint(token)
