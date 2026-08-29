# ROSETIC:compression-guid
from pathlib import Path
import pytest
from features.compression import CompressionService

@pytest.mark.asyncio
async def test_compress_file_async_with_default_output(gzip_service: CompressionService, temp_file: Path):
    """Test async compression appends correct extension."""
    compressed = await gzip_service.compress_file_async(temp_file)
    
    assert compressed.exists()
    assert compressed.suffix == ".gz"


@pytest.mark.asyncio
async def test_compress_file_async_with_explicit_output(gzip_service: CompressionService, temp_file: Path, tmp_path: Path):
    """Test async compression uses explicit output path."""
    output_path = tmp_path / "async_compressed.gz"
    compressed = await gzip_service.compress_file_async(temp_file, output_path)
    
    assert compressed == output_path
    assert compressed.exists()


@pytest.mark.asyncio
async def test_async_roundtrip_preserves_content(gzip_service: CompressionService, temp_file: Path):
    """Test async compress/decompress preserves file content."""
    original_content = temp_file.read_bytes()
    
    compressed = await gzip_service.compress_file_async(temp_file)
    decompressed = await gzip_service.decompress_file_async(compressed)
    
    assert decompressed.read_bytes() == original_content


@pytest.mark.asyncio
async def test_compress_file_async_with_remove_source(gzip_service: CompressionService, temp_file: Path):
    """Test async compression with remove_source deletes original."""
    original_path = temp_file
    compressed = await gzip_service.compress_file_async(temp_file, remove_source=True)
    
    assert compressed.exists()
    assert not original_path.exists()


@pytest.mark.asyncio
async def test_decompress_file_async_with_remove_source(gzip_service: CompressionService, temp_file: Path):
    """Test async decompression with remove_source deletes compressed file."""
    compressed = await gzip_service.compress_file_async(temp_file)
    decompressed = await gzip_service.decompress_file_async(compressed, remove_source=True)
    
    assert decompressed.exists()
    assert not compressed.exists()


@pytest.mark.asyncio
async def test_compress_file_async_nonexistent_raises(gzip_service: CompressionService, tmp_path: Path):
    """Test async compression of non-existent file raises FileNotFoundError."""
    nonexistent = tmp_path / "ghost.txt"
    
    with pytest.raises(FileNotFoundError):
        await gzip_service.compress_file_async(nonexistent)


@pytest.mark.asyncio
async def test_decompress_file_async_nonexistent_raises(gzip_service: CompressionService, tmp_path: Path):
    """Test async decompression of non-existent file raises FileNotFoundError."""
    nonexistent = tmp_path / "ghost.gz"
    
    with pytest.raises(FileNotFoundError):
        await gzip_service.decompress_file_async(nonexistent)


@pytest.mark.asyncio
async def test_async_compress_with_custom_level(gzip_service: CompressionService, temp_file: Path):
    """Test async compression accepts custom level parameter."""
    compressed = await gzip_service.compress_file_async(temp_file, level=9)
    assert compressed.exists()
    
    decompressed = await gzip_service.decompress_file_async(compressed)
    assert decompressed.read_bytes() == temp_file.read_bytes()

