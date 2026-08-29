# ROSETIC:compression-guid
from enum import Enum
from typing import Final

class CompressionAlgorithm(str, Enum):
    """Supported compression algorithms."""
    GZIP = "gzip"
    BZ2 = "bz2"
    LZMA = "lzma"


class CompressionLevel(int, Enum):
    """Compression level presets for convenience."""
    FASTEST = 1
    BALANCED = 6
    BEST = 9


# Default configuration constants
DEFAULT_ALGORITHM: Final[CompressionAlgorithm] = CompressionAlgorithm.GZIP
DEFAULT_COMPRESSION_LEVEL: Final[int] = CompressionLevel.BALANCED.value
DEFAULT_BUFFER_SIZE: Final[int] = 64 * 1024  # 64 KB chunks for streaming

