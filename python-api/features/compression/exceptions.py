# ROSETIC:compression-guid
"""
Custom exceptions for the compression module.

These exceptions provide clear, specific error messages for
compression-related operations.
"""

class CompressionError(Exception):
    """Base exception for all compression-related errors."""


class CompressionFailedError(CompressionError):
    """Raised when compression operation fails."""
    
    def __init__(self, algorithm: str, reason: str):
        self.algorithm = algorithm
        self.reason = reason
        super().__init__(f"Compression failed using {algorithm}: {reason}")


class DecompressionFailedError(CompressionError):
    """Raised when decompression operation fails."""
    
    def __init__(self, algorithm: str, reason: str):
        self.algorithm = algorithm
        self.reason = reason
        super().__init__(f"Decompression failed using {algorithm}: {reason}")


class UnsupportedAlgorithmError(CompressionError):
    """Raised when an unsupported compression algorithm is requested."""
    
    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        super().__init__(f"Unsupported compression algorithm: {algorithm}")

