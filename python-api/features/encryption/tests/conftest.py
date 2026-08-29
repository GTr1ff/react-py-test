# ROSETIC:encryption-guid
"""
Shared test fixtures for encryption tests.
"""
import pytest
from features.encryption.fernet_service import FernetService

@pytest.fixture
def test_key():
    """Generate a valid test Fernet key."""
    return FernetService.generate_key()


@pytest.fixture
def test_key_bytes(test_key):
    """Generate a valid test Fernet key as bytes."""
    return test_key.encode()


@pytest.fixture
def second_test_key():
    """Generate a second valid test Fernet key for rotation tests."""
    return FernetService.generate_key()


@pytest.fixture
def third_test_key():
    """Generate a third valid test Fernet key for multi-key tests."""
    return FernetService.generate_key()


@pytest.fixture
def service(test_key):
    """Create a FernetService instance with a test key."""
    return FernetService(test_key)


@pytest.fixture
def multi_key_service(test_key, second_test_key, third_test_key):
    """Create a FernetService instance with multiple keys."""
    return FernetService([test_key, second_test_key, third_test_key])


@pytest.fixture
def sample_data():
    """Sample data for encryption tests."""
    return "Hello, World! This is sensitive data."


@pytest.fixture
def sample_data_bytes():
    """Sample data as bytes for encryption tests."""
    return b"Binary data \x00\x01\x02\xff"


@pytest.fixture
def encrypted_token(service, sample_data):
    """Pre-encrypted token for decryption tests."""
    return service.encrypt(sample_data)


@pytest.fixture
def old_encrypted_token(second_test_key, sample_data):
    """Token encrypted with the old key (for rotation tests)."""
    old_service = FernetService(second_test_key)
    return old_service.encrypt(sample_data)
