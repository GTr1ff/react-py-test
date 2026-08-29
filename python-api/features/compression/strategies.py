# ROSETIC:compression-guid
import bz2
import gzip
import lzma
from abc import ABC, abstractmethod
from typing import IO

from .config import (
    DEFAULT_COMPRESSION_LEVEL,
    CompressionAlgorithm,
)
from .exceptions import CompressionFailedError, DecompressionFailedError, UnsupportedAlgorithmError

class CompressionStrategy(ABC):
    """Abstract base class for compression strategies."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the compression algorithm."""
    
    @property
    @abstractmethod
    def extension(self) -> str:
        """Return the extension of the compression algorithm."""
    
    @abstractmethod
    def compress(self, data: bytes, level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
        """Compress the given data."""
    
    @abstractmethod
    def decompress(self, data: bytes) -> bytes:
        """Decompress the given data."""
    
    @abstractmethod
    def open_compressed(
        self,
        filename: str,
        mode: str = "rb",
        level: int = DEFAULT_COMPRESSION_LEVEL
    ) -> IO[bytes]:
        """
        Open a compressed file for reading or writing.
        
        Args:
            filename: Path to the file
            mode: File mode ('rb' for reading, 'wb' for writing)
            level: Compression level for writing
            
        Returns:
            File-like object for compressed data
        """


class GzipCompression(CompressionStrategy):
    """
    GZIP compression strategy.
    
    GZIP provides a good balance between compression ratio and speed.
    It's the most widely supported compression format.
    """
    
    @property
    def name(self) -> str:
        return "gzip"

    @property
    def extension(self) -> str:
        return ".gz"
    
    def compress(self, data: bytes, level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
        try:
            return gzip.compress(data, compresslevel=level)
        except Exception as e:
            raise CompressionFailedError(self.name, str(e)) from e
    
    def decompress(self, data: bytes) -> bytes:
        try:
            return gzip.decompress(data)
        except Exception as e:
            raise DecompressionFailedError(self.name, str(e)) from e
    
    def open_compressed(
        self,
        filename: str,
        mode: str = "rb",
        level: int = DEFAULT_COMPRESSION_LEVEL
    ) -> IO[bytes]:
        return gzip.open(filename, mode, compresslevel=level)  # type: ignore[return-value]


class Bz2Compression(CompressionStrategy):
    """
    BZ2 compression strategy.
    
    BZ2 typically achieves better compression ratios than GZIP
    but is slower. Good for archival purposes.
    """
    
    @property
    def name(self) -> str:
        return "bz2"
    
    @property
    def extension(self) -> str:
        return ".bz2"
    
    def compress(self, data: bytes, level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
        try:
            return bz2.compress(data, compresslevel=level)
        except Exception as e:
            raise CompressionFailedError(self.name, str(e)) from e
    
    def decompress(self, data: bytes) -> bytes:
        try:
            return bz2.decompress(data)
        except Exception as e:
            raise DecompressionFailedError(self.name, str(e)) from e
    
    def open_compressed(
        self,
        filename: str,
        mode: str = "rb",
        level: int = DEFAULT_COMPRESSION_LEVEL
    ) -> IO[bytes]:
        return bz2.open(filename, mode, compresslevel=level)  # type: ignore[return-value]


class LzmaCompression(CompressionStrategy):
    """
    LZMA compression strategy.
    
    LZMA provides the best compression ratios but is the slowest.
    Best for maximum space savings when time is not critical.
    """
    
    @property
    def name(self) -> str:
        return "lzma"
    
    @property
    def extension(self) -> str:
        return ".xz"
    
    def compress(self, data: bytes, level: int = DEFAULT_COMPRESSION_LEVEL) -> bytes:
        try:
            return lzma.compress(data, preset=level)
        except Exception as e:
            raise CompressionFailedError(self.name, str(e)) from e
    
    def decompress(self, data: bytes) -> bytes:
        try:
            return lzma.decompress(data)
        except Exception as e:
            raise DecompressionFailedError(self.name, str(e)) from e
    
    def open_compressed(
        self,
        filename: str,
        mode: str = "rb",
        level: int = DEFAULT_COMPRESSION_LEVEL
    ) -> IO[bytes]:
        return lzma.open(filename, mode, preset=level)  # type: ignore[return-value]

_ALGO_TO_CLASS: dict[CompressionAlgorithm, type[CompressionStrategy]] = {
    CompressionAlgorithm.GZIP: GzipCompression,
    CompressionAlgorithm.BZ2: Bz2Compression,
    CompressionAlgorithm.LZMA: LzmaCompression,
}

def create_compressor(algorithm: CompressionAlgorithm) -> CompressionStrategy:
    try:
        return _ALGO_TO_CLASS[algorithm]()
    except KeyError as e:
        raise UnsupportedAlgorithmError(algorithm.value) from e

