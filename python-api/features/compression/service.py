# ROSETIC:compression-guid
import asyncio
from pathlib import Path
from typing import Any

from .config import DEFAULT_ALGORITHM, DEFAULT_BUFFER_SIZE, DEFAULT_COMPRESSION_LEVEL, CompressionAlgorithm
from .exceptions import CompressionFailedError, DecompressionFailedError
from .strategies import create_compressor

class CompressionService:
    """
    High-level compression service supporting multiple algorithms.
    
    This service provides a unified interface for compression operations,
    supporting multiple compression algorithms (GZIP, BZ2, LZMA) 
    and both synchronous and asynchronous operations.
    """
    
    def __init__(
        self,
        algorithm: CompressionAlgorithm = DEFAULT_ALGORITHM,
        default_level: int = DEFAULT_COMPRESSION_LEVEL,
        buffer_size: int = DEFAULT_BUFFER_SIZE,
    ):
        """
        Initialize the compression service.
        
        Args:
            algorithm: Compression algorithm to use
            default_level: Default compression level (1-9)
            buffer_size: Buffer size for streaming operations (in bytes)
        """
        self._default_level = default_level
        self._buffer_size = buffer_size
        self._strategy = create_compressor(algorithm)
    
    @property
    def algorithm(self) -> str:
        """Get the name of the current compression algorithm."""
        return self._strategy.name
    
    # ========== Bytes Compression/Decompression ==========
    
    def compress_bytes(
        self,
        data: bytes,
        level: int | None = None
    ) -> bytes:
        """
        Compress raw bytes.

        Args:
            data: Raw bytes to compress
            level: Compression level (1-9). If None, uses default level.
        """
        compression_level = level if level is not None else self._default_level
        return self._strategy.compress(data, compression_level)
    
    def decompress_bytes(self, data: bytes) -> bytes:
        """Decompress raw bytes."""
        return self._strategy.decompress(data)
    
    # ========== String Compression/Decompression ==========
    
    def compress_string(
        self,
        text: str,
        encoding: str = "utf-8",
        level: int | None = None
    ) -> bytes:
        """
        Compress a string to bytes.
        
        Args:
            text: String to compress
            encoding: Text encoding to use (default: utf-8)
            level: Compression level (1-9). If None, uses default level.
        """
        data = text.encode(encoding)
        return self.compress_bytes(data, level)
    
    def decompress_to_string(
        self,
        data: bytes,
        encoding: str = "utf-8"
    ) -> str:
        """
        Decompress bytes to a string.
        
        Args:
            data: Compressed bytes to decompress
            encoding: Text encoding to use (default: utf-8)
        """
        decompressed_bytes = self.decompress_bytes(data)
        return decompressed_bytes.decode(encoding)
    
    # ========== File Compression/Decompression (Sync) ==========
    
    def compress_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        level: int | None = None,
        remove_source: bool = False
    ) -> Path:
        """
        Compress a file (synchronous).
        
        Args:
            input_path: Path to the file to compress
            output_path: Path for the compressed file. If None, appends
                        appropriate extension to input_path.
            level: Compression level (1-9). If None, uses default level.
            remove_source: If True, removes the source file after compression
            
        Returns:
            Path to the compressed file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            CompressionFailedError: If compression fails
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(str(input_path))
        
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix(input_path.suffix + self._strategy.extension)
        else:
            output_path = Path(output_path)
        
        compression_level = level if level is not None else self._default_level
        
        try:
            self._compress_file_sync(input_path, output_path, compression_level)
            
            if remove_source:
                input_path.unlink()
            
            return output_path
            
        except Exception as e:
            # Clean up partial output file
            if output_path.exists():
                output_path.unlink()
            raise CompressionFailedError(self._strategy.name, str(e))
    
    def decompress_file(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        remove_source: bool = False
    ) -> Path:
        """
        Decompress a file (synchronous).
        
        Args:
            input_path: Path to the compressed file
            output_path: Path for the decompressed file. If None, removes
                        the compression extension from input_path.
            remove_source: If True, removes the compressed file after decompression
            
        Returns:
            Path to the decompressed file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            DecompressionFailedError: If decompression fails
        """
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(str(input_path))
        
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix("")
        else:
            output_path = Path(output_path)
        
        try:
            self._decompress_file_sync(input_path, output_path)
            
            if remove_source:
                input_path.unlink()
            
            return output_path
            
        except Exception as e:
            # Clean up partial output file
            if output_path.exists():
                output_path.unlink()
            raise DecompressionFailedError(self._strategy.name, str(e))
    
    # ========== File Compression/Decompression (Async) ==========
    
    async def compress_file_async(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        level: int | None = None,
        remove_source: bool = False
    ) -> Path:
        """
        Compress a file asynchronously.
        
        This method uses asyncio to avoid blocking the event loop,
        making it suitable for use in FastAPI endpoints and background tasks.
        
        Args:
            input_path: Path to the file to compress
            output_path: Path for the compressed file. If None, appends
                        appropriate extension to input_path.
            level: Compression level (1-9). If None, uses default level.
            remove_source: If True, removes the source file after compression
            
        Returns:
            Path to the compressed file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            CompressionFailedError: If compression fails
        """
        input_path = Path(input_path)
        
        if not await asyncio.to_thread(input_path.exists):
            raise FileNotFoundError(str(input_path))
        
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix(input_path.suffix + self._strategy.extension)
        else:
            output_path = Path(output_path)
        
        compression_level = level if level is not None else self._default_level
        
        try:
            await asyncio.to_thread(
                self._compress_file_sync,
                input_path,
                output_path,
                compression_level
            )
            
            if remove_source:
                await asyncio.to_thread(
                    input_path.unlink
                )
            
            return output_path
            
        except Exception as e:
            # Clean up partial output file
            if output_path.exists():
                await asyncio.to_thread(
                    output_path.unlink
                )
            raise CompressionFailedError(self._strategy.name, str(e))
    
    async def decompress_file_async(
        self,
        input_path: str | Path,
        output_path: str | Path | None = None,
        remove_source: bool = False
    ) -> Path:
        """
        Decompress a file asynchronously.
        
        This method uses asyncio to avoid blocking the event loop,
        making it suitable for use in FastAPI endpoints and background tasks.
        
        Args:
            input_path: Path to the compressed file
            output_path: Path for the decompressed file. If None, removes
                        the compression extension from input_path.
            remove_source: If True, removes the compressed file after decompression
            
        Returns:
            Path to the decompressed file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            DecompressionFailedError: If decompression fails
        """
        input_path = Path(input_path)
        
        if not await asyncio.to_thread(input_path.exists):
            raise FileNotFoundError(str(input_path))
        
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix("")
        else:
            output_path = Path(output_path)
        
        try:
            await asyncio.to_thread(
                self._decompress_file_sync,
                input_path,
                output_path
            )
            
            if remove_source:
                await asyncio.to_thread(
                    input_path.unlink
                )
            
            return output_path
            
        except Exception as e:
            # Clean up partial output file
            if output_path.exists():
                await asyncio.to_thread(
                    output_path.unlink
                )
            raise DecompressionFailedError(self._strategy.name, str(e))
    
    # ========== Helper Methods ==========
    
    def _compress_file_sync(
        self,
        input_path: Path,
        output_path: Path,
        level: int
    ) -> None:
        with open(input_path, "rb") as f_in:
            with self._strategy.open_compressed(str(output_path), "wb", level) as f_out:
                while chunk := f_in.read(self._buffer_size):
                    f_out.write(chunk)
    
    def _decompress_file_sync(
        self,
        input_path: Path,
        output_path: Path
    ) -> None:
        with self._strategy.open_compressed(str(input_path), "rb") as f_in:
            with open(output_path, "wb") as f_out:
                while chunk := f_in.read(self._buffer_size):
                    f_out.write(chunk)
    
    def get_compressed_stream(
        self,
        filepath: str | Path,
        level: int | None = None
    ) -> Any:
        """
        Get a writable stream for compressed output.
        
        This is useful for streaming large amounts of data directly
        to a compressed file without loading everything into memory.
        
        Args:
            filepath: Path to the compressed output file
            level: Compression level (1-9). If None, uses default level.
        """
        compression_level = level if level is not None else self._default_level
        return self._strategy.open_compressed(str(filepath), "wb", compression_level)
    
    def get_decompressed_stream(
        self,
        filepath: str | Path
    ) -> Any:
        """
        Get a readable stream for decompressed input.
        
        This is useful for reading large compressed files without
        loading everything into memory at once.
        """
        return self._strategy.open_compressed(str(filepath), "rb")

