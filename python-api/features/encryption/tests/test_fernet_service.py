# ROSETIC:encryption-guid
"""
Unit tests for the FernetService encryption service.
"""
from cryptography.fernet import InvalidToken
import pytest
import time
import os
from unittest.mock import patch

from features.encryption.fernet_service import FernetService, get_fernet_service, _build_fernet_service

class TestFernetServiceInitialization:
    """Test cases for FernetService initialization."""

    def test_init_with_single_string_key(self, test_key):
        """Test initialization with a single string key."""
        service = FernetService(test_key)
        
        assert service.fernet is not None
        assert service.get_key_count() == 1

    def test_init_with_single_bytes_key(self, test_key_bytes):
        """Test initialization with a single bytes key."""
        service = FernetService(test_key_bytes)
        
        assert service.fernet is not None
        assert service.get_key_count() == 1

    def test_init_with_multiple_keys(self, test_key, second_test_key):
        """Test initialization with multiple keys."""
        service = FernetService([test_key, second_test_key])
        
        assert service.get_key_count() == 2

    def test_init_with_mixed_key_types(self, test_key, second_test_key):
        """Test initialization with mixed string and bytes keys."""
        keys = [test_key, second_test_key.encode()]
        service = FernetService(keys)
        
        assert service.get_key_count() == 2

    def test_init_with_empty_list_raises_error(self):
        """Test that empty key list raises ValueError."""
        with pytest.raises(ValueError, match="At least one key required"):
            FernetService([])

    def test_init_with_invalid_key_type_raises_error(self):
        """Test that invalid key type raises TypeError."""
        with pytest.raises(TypeError, match="Keys must be bytes or str"):
            FernetService([123]) # type: ignore

    def test_init_with_malformed_key_raises_error(self):
        """Test that malformed key raises InvalidKeyError."""
        bad_key = "not-a-valid-fernet-key"
        
        with pytest.raises(ValueError):
            FernetService(bad_key)


# ─── Static Methods Tests ──────────────────────────────────

class TestFernetServiceStaticMethods:
    """Test cases for static utility methods."""

    def test_generate_key_returns_string(self):
        """Test that generate_key returns a string."""
        key = FernetService.generate_key()
        
        assert isinstance(key, str)
        assert len(key) == 44  # Fernet keys are 44 chars when base64-encoded

    def test_generate_key_creates_valid_keys(self):
        """Test that generated keys are valid."""
        key = FernetService.generate_key()
        
        assert FernetService.validate_key(key)

    def test_validate_key_with_valid_string_key(self, test_key):
        """Test validate_key with valid string key."""
        is_valid = FernetService.validate_key(test_key)
        
        assert is_valid is True

    def test_validate_key_with_valid_bytes_key(self, test_key_bytes):
        """Test validate_key with valid bytes key."""
        is_valid = FernetService.validate_key(test_key_bytes)
        
        assert is_valid is True

    def test_validate_key_with_invalid_key(self):
        """Test validate_key with invalid key."""
        invalid_key = "invalid-key"
        is_valid = FernetService.validate_key(invalid_key)
        
        assert is_valid is False

    def test_validate_key_with_empty_string(self):
        """Test validate_key with empty string."""
        is_valid = FernetService.validate_key("")
        
        assert is_valid is False


# ─── Encryption Tests ──────────────────────────────────

class TestFernetServiceEncryption:
    """Test cases for encryption operations."""

    def test_encrypt_string_data(self, service, sample_data):
        """Test encrypting string data."""
        token = service.encrypt(sample_data)
        
        assert isinstance(token, str)
        assert token != sample_data
        assert len(token) > 0

    def test_encrypt_bytes_data(self, service, sample_data_bytes):
        """Test encrypting bytes data."""
        token = service.encrypt(sample_data_bytes)
        
        assert isinstance(token, str)
        assert len(token) > 0

    def test_encrypt_produces_unique_tokens(self, service, sample_data):
        """Test that encrypting same data produces different tokens."""
        token1 = service.encrypt(sample_data)
        token2 = service.encrypt(sample_data)
    
        assert token1 != token2

    def test_encrypt_empty_string(self, service):
        """Test encrypting empty string."""
        token = service.encrypt("")
        
        assert isinstance(token, str)
        assert len(token) > 0


# ─── Decryption Tests ──────────────────────────────────

class TestFernetServiceDecryption:
    """Test cases for decryption operations."""

    def test_decrypt_to_bytes(self, service, sample_data):
        """Test decrypting token to bytes."""
        token = service.encrypt(sample_data)
        
        decrypted = service.decrypt(token)
        
        assert isinstance(decrypted, bytes)
        assert decrypted == sample_data.encode()

    def test_decrypt_to_string(self, service, sample_data):
        """Test decrypting token to string."""
        token = service.encrypt(sample_data)
        
        decrypted = service.decrypt_to_string(token)
        
        assert isinstance(decrypted, str)
        assert decrypted == sample_data

    def test_decrypt_bytes_data(self, service, sample_data_bytes):
        """Test decrypting bytes data."""
        token = service.encrypt(sample_data_bytes)
        
        decrypted = service.decrypt(token)
        
        assert decrypted == sample_data_bytes

    def test_decrypt_with_invalid_token_raises_error(self, service):
        """Test that invalid token raises InvalidTokenError."""
        invalid_token = "invalid-token-data"

        with pytest.raises(InvalidToken):
            service.decrypt(invalid_token)

    def test_decrypt_with_wrong_key_raises_error(self, encrypted_token):
        """Test that decrypting with wrong key raises error."""
        wrong_service = FernetService(FernetService.generate_key())
        
        with pytest.raises(InvalidToken):
            wrong_service.decrypt(encrypted_token)

    def test_decrypt_with_ttl_valid_token(self, service, sample_data):
        """Test decrypting token within TTL."""
        token = service.encrypt(sample_data)
        
        decrypted = service.decrypt_to_string(token, ttl=60)
        
        assert decrypted == sample_data


# ─── Token Validation Tests ──────────────────────────────────────

class TestFernetServiceTokenValidation:
    """Test cases for token validation operations."""

    def test_is_token_valid_with_valid_token(self, service, encrypted_token):
        """Test is_token_valid with valid token."""
        is_valid = service.is_token_valid(encrypted_token)
        
        assert is_valid is True

    def test_is_token_valid_with_invalid_token(self, service):
        """Test is_token_valid with invalid token."""
        invalid_token = "invalid-token"
        is_valid = service.is_token_valid(invalid_token)
        
        assert is_valid is False

# ─── Key Rotation Tests ──────────────────────────────────

class TestFernetServiceKeyRotation:
    """Test cases for key rotation operations."""

    def test_rotate_key_adds_new_key(self, service, second_test_key):
        """Test that rotate_key adds a new key."""
        initial_count = service.get_key_count()
        service.rotate_key(second_test_key)
        
        assert service.get_key_count() == initial_count + 1

    def test_rotate_key_with_bytes(self, service, second_test_key):
        """Test rotate_key with bytes key."""
        initial_count = service.get_key_count()

        service.rotate_key(second_test_key.encode())
        
        assert service.get_key_count() == initial_count + 1

    def test_rotate_key_new_key_becomes_primary(self, service, second_test_key, sample_data):
        """Test that new key is used for encryption after rotation."""
        # Arrange
        service.rotate_key(second_test_key)
        
        # Act
        token = service.encrypt(sample_data)
        
        # Create service with only new key
        new_key_service = FernetService(second_test_key)
        decrypted = new_key_service.decrypt_to_string(token)
        
        # Assert
        assert decrypted == sample_data

    def test_rotate_key_old_keys_still_decrypt(self, service, second_test_key, encrypted_token):
        """Test that old keys can still decrypt after rotation."""
        # Arrange
        service.rotate_key(second_test_key)
        
        # Act
        decrypted = service.decrypt_to_string(encrypted_token)
        
        # Assert
        assert isinstance(decrypted, str)

    def test_rotate_key_with_invalid_key_raises_error(self, service):
        """Test that rotating with invalid key raises InvalidKeyError."""
        invalid_key = "invalid-key"
        
        with pytest.raises(ValueError, match="Invalid Fernet key provided"):
            service.rotate_key(invalid_key)

    def test_rotate_token(self, test_key, second_test_key, sample_data):
        """Test re-encrypting token with new key."""
        # Arrange
        old_service = FernetService(second_test_key)
        old_token = old_service.encrypt(sample_data)
        
        # Create service with both keys (new first)
        service = FernetService([test_key, second_test_key])
        
        # Act
        new_token = service.rotate_token(old_token)
        
        # Assert
        assert new_token != old_token
        # New token should decrypt with new key only
        new_service = FernetService(test_key)
        decrypted = new_service.decrypt_to_string(new_token)
        assert decrypted == sample_data

    def test_rotate_token_with_invalid_token_raises_error(self, service):
        """Test rotate_token with invalid token raises InvalidTokenError."""
        invalid_token = "invalid-token"
        
        with pytest.raises(InvalidToken):
            service.rotate_token(invalid_token)


# ─── Key Retirement Tests ──────────────────────────────────

class TestFernetServiceKeyRetirement:
    """Test cases for key retirement operations."""

    def test_retire_old_keys_without_confirmation_raises_error(self, multi_key_service):
        """Test that retire_old_keys without confirmation raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="retire_old_keys\\(\\) requires explicit confirmation"):
            multi_key_service.retire_old_keys()

    def test_retire_old_keys_with_confirmation(self, multi_key_service):
        """Test retiring old keys with confirmation."""
        initial_count = multi_key_service.get_key_count()
        retired_count = multi_key_service.retire_old_keys(confirm=True)
        
        assert retired_count == initial_count - 1
        assert multi_key_service.get_key_count() == 1

    def test_retire_old_keys_with_single_key_raises_error(self, service):
        """Test that retiring keys with only one key raises ValueError."""
        with pytest.raises(ValueError, match="Cannot retire keys: only one key is active"):
            service.retire_old_keys(confirm=True)

    def test_retire_old_keys_returns_count(self, test_key, second_test_key, third_test_key):
        """Test that retire_old_keys returns correct count."""
        service = FernetService([test_key, second_test_key, third_test_key])
        retired = service.retire_old_keys(confirm=True)

        assert retired == 2

    def test_after_retirement_only_new_tokens_decrypt(
        self, test_key, second_test_key, sample_data
    ):
        """Test that after retirement, only tokens encrypted with primary key work."""
        # Arrange
        old_service = FernetService(second_test_key)
        old_token = old_service.encrypt(sample_data)
        
        # Create multi-key service and retire old keys
        service = FernetService([test_key, second_test_key])
        service.retire_old_keys(confirm=True)
        
        # New token should work
        new_token = service.encrypt(sample_data)
        assert service.decrypt_to_string(new_token) == sample_data
        
        # Old token should fail
        with pytest.raises(InvalidToken):
            service.decrypt(old_token)


# ─── Environment Variable Tests ──────────────────────────────────

class TestFernetServiceFromEnv:
    """Test cases for from_env class method."""

    def test_from_env_with_single_key(self, test_key):
        """Test loading single key from environment."""
        with patch.dict(os.environ, {"FERNET_KEY": test_key}):
            service = FernetService.from_env()

            assert service.get_key_count() == 1

    def test_from_env_with_multiple_keys(self, test_key, second_test_key):
        """Test loading multiple keys from environment."""
        env_value = f"{test_key},{second_test_key}"
        with patch.dict(os.environ, {"FERNET_KEY": env_value}):
            service = FernetService.from_env()

            assert service.get_key_count() == 2

    def test_from_env_with_missing_var_raises_error(self):
        """Test that missing environment variable raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Environment variable FERNET_KEY not set"):
                FernetService.from_env()

    def test_from_env_with_whitespace_in_keys(self, test_key, second_test_key):
        """Test that whitespace around keys is stripped."""
        env_value = f"{test_key} , {second_test_key} "
        with patch.dict(os.environ, {"FERNET_KEY": env_value}):
            service = FernetService.from_env()
            
            assert service.get_key_count() == 2


# ─── Singleton Tests ──────────────────────────────────

class TestGetFernetService:
    """Test cases for the get_fernet_service dependency and its cached builder."""

    def test_returns_same_instance(self, service):
        """Test that multiple calls return the same cached instance."""
        with patch('features.encryption.fernet_service.FernetService.from_env', return_value=service):
            _build_fernet_service.cache_clear()

            instance1 = get_fernet_service()
            instance2 = get_fernet_service()

            assert instance1 is instance2

    def test_returns_fernet_service_instance(self, service):
        """Test that the cached accessor returns a FernetService instance."""
        with patch('features.encryption.fernet_service.FernetService.from_env', return_value=service):
            _build_fernet_service.cache_clear()

            instance = get_fernet_service()

            assert isinstance(instance, FernetService)

    def test_cached_instance_encryption_decryption(self, service, sample_data):
        """Test that cached instance can encrypt and decrypt data."""
        with patch('features.encryption.fernet_service.FernetService.from_env', return_value=service):
            _build_fernet_service.cache_clear()

            instance = get_fernet_service()
            encrypted = instance.encrypt(sample_data)
            decrypted = instance.decrypt_to_string(encrypted)

            assert decrypted == sample_data

    def test_from_env_called_only_once(self, service):
        """Test that from_env is invoked only once across multiple calls."""
        with patch(
            'features.encryption.fernet_service.FernetService.from_env',
            return_value=service,
        ) as mock_from_env:
            _build_fernet_service.cache_clear()

            get_fernet_service()
            get_fernet_service()
            get_fernet_service()

            assert mock_from_env.call_count == 1

    def test_cache_clear_creates_new_instance(self, test_key, second_test_key):
        """Test that cache_clear forces re-initialization with new env state."""
        # Create services with different keys
        service1 = FernetService(test_key)
        service2 = FernetService(second_test_key)

        with patch('features.encryption.fernet_service.FernetService.from_env', return_value=service1):
            _build_fernet_service.cache_clear()
            instance1 = get_fernet_service()

        with patch('features.encryption.fernet_service.FernetService.from_env', return_value=service2):
            _build_fernet_service.cache_clear()
            instance2 = get_fernet_service()

        # They should be different instances with different keys
        assert instance1 is not instance2

        # Test that they can't decrypt each other's data
        encrypted1 = instance1.encrypt("test1")
        encrypted2 = instance2.encrypt("test2")

        with pytest.raises(InvalidToken):
            instance1.decrypt_to_string(encrypted2)

        with pytest.raises(InvalidToken):
            instance2.decrypt_to_string(encrypted1)

