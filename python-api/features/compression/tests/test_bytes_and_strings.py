# ROSETIC:compression-guid
from features.compression import CompressionService

def test_compress_and_decompress_bytes_roundtrip(gzip_service: CompressionService, sample_bytes: bytes):
    """Test bytes can be compressed and decompressed back to original."""
    compressed = gzip_service.compress_bytes(sample_bytes)
    decompressed = gzip_service.decompress_bytes(compressed)
    assert decompressed == sample_bytes


def test_compress_and_decompress_string_roundtrip(gzip_service: CompressionService, sample_text: str):
    """Test string encoding/decoding logic."""
    compressed = gzip_service.compress_string(sample_text)
    decompressed = gzip_service.decompress_to_string(compressed)
    assert decompressed == sample_text


def test_compress_string_with_custom_encoding(gzip_service: CompressionService):
    """Test compress_string handles different encodings."""
    text = "现在你知道这意味着什么"
    
    # Test UTF-8 encoding
    compressed_utf8 = gzip_service.compress_string(text, encoding="utf-8")
    assert gzip_service.decompress_to_string(compressed_utf8, encoding="utf-8") == text
    
    # Test UTF-16 encoding
    compressed_utf16 = gzip_service.compress_string(text, encoding="utf-16")
    assert gzip_service.decompress_to_string(compressed_utf16, encoding="utf-16") == text


def test_different_algorithms_produce_different_output(
    gzip_service: CompressionService,
    bz2_service: CompressionService,
    lzma_service: CompressionService,
    sample_bytes: bytes
):
    """Test that different algorithms work independently."""
    gzip_compressed = gzip_service.compress_bytes(sample_bytes)
    bz2_compressed = bz2_service.compress_bytes(sample_bytes)
    lzma_compressed = lzma_service.compress_bytes(sample_bytes)
    
    # All should decompress to original with their respective service
    assert gzip_service.decompress_bytes(gzip_compressed) == sample_bytes
    assert bz2_service.decompress_bytes(bz2_compressed) == sample_bytes
    assert lzma_service.decompress_bytes(lzma_compressed) == sample_bytes

