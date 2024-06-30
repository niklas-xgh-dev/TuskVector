import pytest
from fastapi.testclient import TestClient
import os
import sys
from dotenv import load_dotenv

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.main import app

load_dotenv(os.path.join(os.path.dirname(__file__), '.env.test'))

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