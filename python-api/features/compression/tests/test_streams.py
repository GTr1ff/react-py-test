# ROSETIC:compression-guid
import io
from pathlib import Path
from features.compression import CompressionService

def test_get_compressed_stream_for_writing(gzip_service: CompressionService, tmp_path: Path):
    """Test get_compressed_stream returns writable stream."""
    output_file = tmp_path / "stream_test.gz"
    
    with gzip_service.get_compressed_stream(output_file) as stream:
        stream.write(b"line 1\n")
        stream.write(b"line 2\n")
    
    assert output_file.exists()


def test_get_decompressed_stream_for_reading(gzip_service: CompressionService, tmp_path: Path):
    """Test get_decompressed_stream returns readable stream."""
    output_file = tmp_path / "stream_read_test.gz"
    
    # Write some data
    with gzip_service.get_compressed_stream(output_file) as stream:
        stream.write(b"test data\n")
    
    # Read it back
    with gzip_service.get_decompressed_stream(output_file) as stream:
        content = stream.read()
    
    assert content == b"test data\n"


def test_stream_write_and_read_roundtrip(gzip_service: CompressionService, tmp_path: Path):
    """Test writing via compressed stream and reading via decompressed stream."""
    test_file = tmp_path / "roundtrip.gz"
    test_lines = [b"first line\n", b"second line\n", b"third line\n"]
    
    # Write
    with gzip_service.get_compressed_stream(test_file, level=6) as f:
        for line in test_lines:
            f.write(line)
    
    # Read back
    with gzip_service.get_decompressed_stream(test_file) as f:
        text_stream = io.TextIOWrapper(f, encoding="utf-8")
        lines = [line.strip() for line in text_stream]
    
    assert lines == ["first line", "second line", "third line"]


def test_get_compressed_stream_with_custom_level(gzip_service: CompressionService, tmp_path: Path):
    """Test get_compressed_stream accepts custom compression level."""
    output_file = tmp_path / "custom_level.gz"
    
    with gzip_service.get_compressed_stream(output_file, level=1) as stream:
        stream.write(b"fast compression\n")
    
    assert output_file.exists()
    
    # Verify it's readable
    with gzip_service.get_decompressed_stream(output_file) as stream:
        assert stream.read() == b"fast compression\n"


def test_stream_accepts_string_path(gzip_service: CompressionService, tmp_path: Path):
    """Test stream methods accept string paths (not just Path objects)."""
    output_file_str = str(tmp_path / "string_path.gz")
    
    # Write with string path
    with gzip_service.get_compressed_stream(output_file_str) as stream:
        stream.write(b"test\n")
    
    # Read with string path
    with gzip_service.get_decompressed_stream(output_file_str) as stream:
        assert stream.read() == b"test\n"

