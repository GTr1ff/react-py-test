# ROSETIC:compression-guid
from pathlib import Path
import pytest
from features.compression import CompressionAlgorithm, CompressionService

@pytest.fixture
def gzip_service() -> CompressionService:
    """Provide a GZIP compression service."""
    return CompressionService(algorithm=CompressionAlgorithm.GZIP)


@pytest.fixture
def bz2_service() -> CompressionService:
    """Provide a BZ2 compression service."""
    return CompressionService(algorithm=CompressionAlgorithm.BZ2)


@pytest.fixture
def lzma_service() -> CompressionService:
    """Provide an LZMA compression service."""
    return CompressionService(algorithm=CompressionAlgorithm.LZMA)


@pytest.fixture
def sample_bytes() -> bytes:
    """Provide sample bytes for testing."""
    return b"Lorem Ipsum dolor sit amet. This is test data." * 50


@pytest.fixture
def sample_text() -> str:
    """Provide sample text for testing."""
    return "The quick brown fox jumps over the lazy dog. " * 100


@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """Create a temporary file with test data."""
    test_file = tmp_path / "test_input.txt"
    test_file.write_bytes(b"Test file content " * 1000)
    return test_file

