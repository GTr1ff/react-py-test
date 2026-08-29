# ROSETIC:compression-guid
from features.compression import (
    CompressionAlgorithm,
    CompressionLevel,
    CompressionService,
)

def test_service_default_initialization():
    """Test service initializes with defaults."""
    service = CompressionService()
    assert service.algorithm == "gzip"
    assert service._default_level == CompressionLevel.BALANCED.value
    assert service._buffer_size == 64 * 1024

def test_service_accepts_custom_algorithm():
    """Test service accepts custom algorithm."""
    service = CompressionService(algorithm=CompressionAlgorithm.BZ2)
    assert service.algorithm == "bz2"

def test_service_accepts_custom_compression_level():
    """Test service accepts custom default compression level."""
    service = CompressionService(default_level=CompressionLevel.BEST)
    assert service._default_level == 9

def test_service_accepts_custom_buffer_size():
    """Test service accepts custom buffer size."""
    service = CompressionService(buffer_size=128 * 1024)
    assert service._buffer_size == 128 * 1024

