# ROSETIC:compression-guid
from pathlib import Path
import pytest
from features.compression import CompressionService

def test_compress_file_with_default_output_path(gzip_service: CompressionService, temp_file: Path):
    """Test compress_file appends correct extension when output_path is None."""
    compressed = gzip_service.compress_file(temp_file)
    
    # Should append .gz to the original filename
    assert compressed.exists()
    assert compressed.name == f"{temp_file.name}.gz"
    assert compressed.parent == temp_file.parent


def test_compress_file_with_explicit_output_path(gzip_service: CompressionService, temp_file: Path, tmp_path: Path):
    """Test compress_file uses explicit output path when provided."""
    output_path = tmp_path / "custom_name.compressed"
    compressed = gzip_service.compress_file(temp_file, output_path)
    
    assert compressed == output_path
    assert compressed.exists()


def test_decompress_file_with_default_output_path(gzip_service: CompressionService, temp_file: Path):
    """Test decompress_file removes extension when output_path is None."""
    compressed = gzip_service.compress_file(temp_file)
    decompressed = gzip_service.decompress_file(compressed)
    
    # Should remove the .gz extension
    assert decompressed.exists()
    assert decompressed.suffix == ".txt"


def test_decompress_file_with_explicit_output_path(gzip_service: CompressionService, temp_file: Path, tmp_path: Path):
    """Test decompress_file uses explicit output path when provided."""
    compressed = gzip_service.compress_file(temp_file)
    output_path = tmp_path / "restored.dat"
    decompressed = gzip_service.decompress_file(compressed, output_path)
    
    assert decompressed == output_path
    assert decompressed.exists()


def test_compress_file_roundtrip_preserves_content(gzip_service: CompressionService, temp_file: Path):
    """Test file content is preserved through compress/decompress cycle."""
    original_content = temp_file.read_bytes()
    
    compressed = gzip_service.compress_file(temp_file)
    decompressed = gzip_service.decompress_file(compressed)
    
    assert decompressed.read_bytes() == original_content


def test_compress_file_with_remove_source(gzip_service: CompressionService, temp_file: Path):
    """Test remove_source deletes original file after compression."""
    original_path = temp_file
    compressed = gzip_service.compress_file(temp_file, remove_source=True)
    
    assert compressed.exists()
    assert not original_path.exists()


def test_decompress_file_with_remove_source(gzip_service: CompressionService, temp_file: Path):
    """Test remove_source deletes compressed file after decompression."""
    compressed = gzip_service.compress_file(temp_file)
    compressed_path = compressed
    
    decompressed = gzip_service.decompress_file(compressed, remove_source=True)
    
    assert decompressed.exists()
    assert not compressed_path.exists()


def test_compress_nonexistent_file_raises_error(gzip_service: CompressionService, tmp_path: Path):
    """Test compressing non-existent file raises FileNotFoundError."""
    nonexistent = tmp_path / "does_not_exist.txt"
    
    with pytest.raises(FileNotFoundError) as exc_info:
        gzip_service.compress_file(nonexistent)
    
    assert str(nonexistent) in str(exc_info.value)


def test_decompress_nonexistent_file_raises_error(gzip_service: CompressionService, tmp_path: Path):
    """Test decompressing non-existent file raises FileNotFoundError."""
    nonexistent = tmp_path / "does_not_exist.gz"
    
    with pytest.raises(FileNotFoundError) as exc_info:
        gzip_service.decompress_file(nonexistent)
    
    assert str(nonexistent) in str(exc_info.value)


def test_different_extensions_for_different_algorithms(
    gzip_service: CompressionService,
    bz2_service: CompressionService,
    lzma_service: CompressionService,
    temp_file: Path
):
    """Test each algorithm appends its correct extension."""
    gzip_compressed = gzip_service.compress_file(temp_file)
    assert gzip_compressed.suffix == ".gz"
    
    bz2_compressed = bz2_service.compress_file(temp_file)
    assert bz2_compressed.suffix == ".bz2"
    
    lzma_compressed = lzma_service.compress_file(temp_file)
    assert lzma_compressed.suffix == ".xz"


def test_compress_file_with_custom_level(gzip_service: CompressionService, temp_file: Path):
    """Test compress_file accepts custom compression level parameter."""
    compressed_fast = gzip_service.compress_file(temp_file, level=1)
    assert compressed_fast.exists()
    
    # Verify it can be decompressed
    decompressed = gzip_service.decompress_file(compressed_fast)
    assert decompressed.read_bytes() == temp_file.read_bytes()

