# ROSETIC:compression-guid
"""
Compression Module

A pluggable compression module for FastAPI applications that supports
multiple compression algorithms (GZIP, BZ2, LZMA) with both synchronous
and asynchronous operations.
"""

from .config import (
    DEFAULT_ALGORITHM,
    DEFAULT_BUFFER_SIZE,
    DEFAULT_COMPRESSION_LEVEL,
    CompressionAlgorithm,
    CompressionLevel,
)
from .exceptions import (
    CompressionError,
    CompressionFailedError,
    DecompressionFailedError,
    UnsupportedAlgorithmError,
)
from .service import CompressionService
from .strategies import (
    Bz2Compression,
    CompressionStrategy,
    GzipCompression,
    LzmaCompression,
)

__all__ = [
    # Main service
    "CompressionService",
    # Configuration
    "CompressionAlgorithm",
    "CompressionLevel",
    "DEFAULT_ALGORITHM",
    "DEFAULT_COMPRESSION_LEVEL",
    "DEFAULT_BUFFER_SIZE",
    # Exceptions
    "CompressionError",
    "CompressionFailedError",
    "DecompressionFailedError",
    "UnsupportedAlgorithmError",
    # Strategies (for advanced usage)
    "CompressionStrategy",
    "GzipCompression",
    "Bz2Compression",
    "LzmaCompression",
]
