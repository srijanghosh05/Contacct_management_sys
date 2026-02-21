"""Unit tests for storage_manager.StorageManager."""

import json
import tempfile
from pathlib import Path

import pytest

from storage_manager import StorageManager


@pytest.fixture
def temp_file():
    """A temporary JSON file path; file is removed after test."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        path = Path(f.name)
    yield path
    path.unlink(missing_ok=True)


def test_load_missing_file_returns_empty_list(temp_file):
    path = temp_file
    path.unlink(missing_ok=True)
    storage = StorageManager(filepath=path)
    assert storage.load() == []


def test_load_valid_json_returns_list(temp_file):
    data = [
        {"name": "Alice", "phone": "9876543210", "email": "a@b.com"},
    ]
    temp_file.write_text(json.dumps(data), encoding="utf-8")
    storage = StorageManager(filepath=temp_file)
    assert storage.load() == data


def test_load_non_list_returns_empty_list(temp_file):
    temp_file.write_text('{"key": "value"}', encoding="utf-8")
    storage = StorageManager(filepath=temp_file)
    assert storage.load() == []


def test_load_invalid_json_returns_empty_list(temp_file):
    temp_file.write_text("not json at all", encoding="utf-8")
    storage = StorageManager(filepath=temp_file)
    assert storage.load() == []


def test_save_writes_indented_json(temp_file):
    temp_file.unlink(missing_ok=True)
    storage = StorageManager(filepath=temp_file)
    contacts = [{"name": "Bob", "phone": "9123456789", "email": ""}]
    assert storage.save(contacts) is True
    content = temp_file.read_text(encoding="utf-8")
    parsed = json.loads(content)
    assert parsed == contacts
    assert "    " in content  # indent=4


def test_save_and_load_roundtrip(temp_file):
    temp_file.unlink(missing_ok=True)
    storage = StorageManager(filepath=temp_file)
    contacts = [
        {"name": "A", "phone": "1111111111", "email": "a@x.com"},
        {"name": "B", "phone": "2222222222", "email": ""},
    ]
    storage.save(contacts)
    assert storage.load() == contacts


def test_filepath_property(temp_file):
    storage = StorageManager(filepath=temp_file)
    assert storage.filepath == temp_file
