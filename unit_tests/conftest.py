import pytest
from fastapi.testclient import TestClient
import os
import sys
from dotenv import load_dotenv

# Get the absolute path of the current file
current_file = os.path.abspath(__file__)

# Get the directory containing the current file (unit_tests)
current_dir = os.path.dirname(current_file)

# Get the project root (one level up from unit_tests)
project_root = os.path.dirname(current_dir)

# Add the project root and the backend directory to the Python path
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'backend'))

# Now we can import from backend
from main import app

# Load the test environment variables
env_path = os.path.join(current_dir, '.env.test')
load_dotenv(env_path)

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    return client

@pytest.fixture(scope="module")
def test_api_key():
    api_key = os.getenv("TEST_API_KEY")
    if not api_key:
        raise ValueError("TEST_API_KEY not set in .env.test file")
    return api_key