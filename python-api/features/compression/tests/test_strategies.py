# ROSETIC:compression-guid
from features.compression import (
    Bz2Compression,
    CompressionAlgorithm,
    GzipCompression,
    LzmaCompression,
)
from features.compression.strategies import create_compressor

def test_gzip_strategy_metadata():
    """Test GZIP strategy has correct name and extension."""
    strategy = GzipCompression()
    assert strategy.name == "gzip"
    assert strategy.extension == ".gz"


def test_bz2_strategy_metadata():
    """Test BZ2 strategy has correct name and extension."""
    strategy = Bz2Compression()
    assert strategy.name == "bz2"
    assert strategy.extension == ".bz2"


def test_lzma_strategy_metadata():
    """Test LZMA strategy has correct name and extension."""
    strategy = LzmaCompression()
    assert strategy.name == "lzma"
    assert strategy.extension == ".xz"


def test_create_compressor_for_gzip():
    """Test factory returns GzipCompression for GZIP algorithm."""
    compressor = create_compressor(CompressionAlgorithm.GZIP)
    assert isinstance(compressor, GzipCompression)


def test_create_compressor_for_bz2():
    """Test factory returns Bz2Compression for BZ2 algorithm."""
    compressor = create_compressor(CompressionAlgorithm.BZ2)
    assert isinstance(compressor, Bz2Compression)


def test_create_compressor_for_lzma():
    """Test factory returns LzmaCompression for LZMA algorithm."""
    compressor = create_compressor(CompressionAlgorithm.LZMA)
    assert isinstance(compressor, LzmaCompression)

