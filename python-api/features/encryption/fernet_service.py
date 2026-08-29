# ROSETIC:encryption-guid
import functools
import os

from cryptography.fernet import Fernet, MultiFernet, InvalidToken

class FernetService:
    """
    A MultiFernet-based encryption service for symmetric encryption.
    """
    
    def __init__(self, key: bytes | str | list[bytes | str]):
        """
        Initialize the Fernet service with MultiFernet.
        
        Args:
            key: Single key (bytes/str) or list of keys for key rotation.
                 Keys should be URL-safe base64-encoded 32-byte keys.
                 Single keys are automatically wrapped in a list.
                 
        Raises:
            ValueError: If key list is empty
            TypeError: If key types are invalid
            InvalidKeyError: If a key is malformed or invalid
        """
        # Normalize to list of keys
        if isinstance(key, list):
            if len(key) == 0:
                raise ValueError("At least one key required")
            keys = key
        else:
            keys = [key]
        
        # Process keys to bytes
        processed_keys: list[bytes] = []
        for k in keys:
            if isinstance(k, str):
                processed_keys.append(k.encode())
            elif isinstance(k, bytes):
                processed_keys.append(k)
            else:
                raise TypeError(f"Keys must be bytes or str, got {type(k)}")
        
        self.fernet = MultiFernet([Fernet(k) for k in processed_keys])

    @classmethod
    def from_env(cls, env_var: str = "FERNET_KEY") -> 'FernetService':
        """
        Create a FernetService instance from environment variable.
        
        This is the recommended way to instantiate FernetService.
        """
        key_value = os.getenv(env_var)
        if not key_value:
            raise ValueError(f"Environment variable {env_var} not set")
        
        # Support comma-separated keys for key rotation
        if ',' in key_value:
            keys: list[bytes | str] = [k.strip() for k in key_value.split(',')]
            return cls(keys)
        else:
            return cls(key_value)

    @staticmethod
    def generate_key() -> str:
        """
        Generate a new Fernet key.
        """
        return Fernet.generate_key().decode()
    
    @staticmethod
    def validate_key(key: bytes | str) -> bool:
        """Validate if a key is a properly formatted Fernet key."""
        try:
            test_key = key.encode('utf-8') if isinstance(key, str) else key
            # Try to create a Fernet instance - will raise if invalid
            Fernet(test_key)
            return True
        except Exception:
            return False

    def encrypt(self, data: bytes | str) -> str:
        """Encrypt data and return as base64 encoded string."""
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data).decode()

    def decrypt(self, token: str, ttl: int | None = None) -> bytes:
        """Decrypt token and return as bytes."""
        return self.fernet.decrypt(token.encode(), ttl=ttl)

    def decrypt_to_string(self, token: str, ttl: int | None = None) -> str:
        """Decrypt token and return as string."""
        return self.decrypt(token, ttl).decode()

    def is_token_valid(self, token: str, ttl: int | None = None) -> bool:
        """Check if a token is valid without returning it."""
        try:
            self.fernet.decrypt(token.encode(), ttl=ttl)
            return True
        except InvalidToken:
            return False

    def rotate_key(self, new_key: bytes | str) -> None:
        """
        Add a new key to the front of the key list (becomes primary encryption key).
        Old keys are retained for decryption of existing tokens.
        """
        # Process new key to bytes
        if isinstance(new_key, str):
            new_key_bytes = new_key.encode()
        elif isinstance(new_key, bytes):
            new_key_bytes = new_key
        else:
            raise TypeError(f"Key must be bytes or str, got {type(new_key)}")
        
        # Validate the new key before adding
        if not self.validate_key(new_key_bytes):
            raise ValueError(f"Invalid Fernet key provided: {new_key_bytes!r}")
        
        # Add new key to the front (becomes primary for encryption)
        self.fernet = MultiFernet([Fernet(new_key_bytes)] + list(self.fernet._fernets))
    
    def rotate_token(self, token: str) -> str:
        """
        Re-encrypt a token with the current primary key.
        Useful after rotating keys to update old tokens.
        """
        return self.fernet.rotate(token.encode()).decode()
    
    def get_key_count(self) -> int:
        """Get the number of active keys."""
        return len(list(self.fernet._fernets))
    
    def retire_old_keys(self, confirm: bool = False) -> int:
        """
        Remove all keys except the primary (first) key.
        
        This should be called AFTER all tokens have been re-encrypted with
        the primary key using rotate_token(). Once old tokens are rotated,
        the old keys are no longer needed for decryption.
        """
        if not confirm:
            raise ValueError(
                "retire_old_keys() requires explicit confirmation. "
                "WARNING: This will make tokens encrypted with old keys undecryptable."
            )
        
        current_key_count = self.get_key_count()
        
        if current_key_count == 1:
            raise ValueError(
                "Cannot retire keys: only one key is active. "
                "No old keys to retire."
            )
        
        # Keep only the first Fernet instance (primary key)
        primary_fernet = next(iter(self.fernet._fernets))
        self.fernet = MultiFernet([primary_fernet])
        
        # Return number of keys that were retired
        retired_count = current_key_count - 1
        return retired_count


@functools.cache
def _build_fernet_service() -> FernetService:
    return FernetService.from_env()


def get_fernet_service() -> FernetService:
    """FastAPI dependency returning the shared FernetService instance."""
    return _build_fernet_service()

