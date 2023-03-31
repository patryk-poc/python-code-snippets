import os

import pytest

from tools.scripts.create_random_files import create_file, get_filename


@pytest.fixture(autouse=True)
def cleanup_files():
    """Cleanup files created during testing."""
    yield
    for file_name in os.listdir():
        if file_name.startswith("file_"):
            os.remove(file_name)


@pytest.mark.parametrize(
    "number, expected",
    [(999, "file_0999.bin"), (1000, "file_1000.bin"), (5000, "file_5000.bin")],
)
def test_get_filename(number, expected):
    """Test get_filename function."""
    result = get_filename(number)
    assert result == expected


@pytest.mark.parametrize("number, size", [(999, 100), (1000, 200), (5000, 500)])
def test_create_file(number, size):
    """Test create_file function."""
    create_file(number, size)
    filename = get_filename(number)
    assert os.path.exists(filename)
    assert os.path.getsize(filename) == size
