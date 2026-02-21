"""Unit tests for cms.Contact, ContactManagementSystem, and validation."""

import tempfile
from pathlib import Path

import pytest

from cms import Contact, ContactManagementSystem
from storage_manager import StorageManager


# --------------------------------------------------------------------------- #
#  Contact                                                                    #
# --------------------------------------------------------------------------- #

def test_contact_from_dict():
    data = {"name": "  Jane  ", "phone": "9876543210", "email": " j@k.com "}
    c = Contact.from_dict(data)
    assert c.name == "Jane"
    assert c.phone == "9876543210"
    assert c.email == "j@k.com"


def test_contact_from_dict_missing_fields():
    c = Contact.from_dict({})
    assert c.name == ""
    assert c.phone == ""
    assert c.email == ""


def test_contact_to_dict():
    c = Contact(name="X", phone="9999999999", email="x@y.z")
    assert c.to_dict() == {"name": "X", "phone": "9999999999", "email": "x@y.z"}


def test_contact_matches_name():
    c = Contact(name="Alice Smith", phone="1111111111", email="a@b.com")
    assert c.matches("alice") is True
    assert c.matches("ALICE") is True
    assert c.matches("smith") is True
    assert c.matches("bob") is False


def test_contact_matches_phone():
    c = Contact(name="A", phone="9876543210", email="")
    assert c.matches("9876543210") is True
    assert c.matches("9876") is True
    assert c.matches("0000") is False


def test_contact_matches_email():
    c = Contact(name="A", phone="1111111111", email="test@example.com")
    assert c.matches("test@example") is True
    assert c.matches("example.com") is True


# --------------------------------------------------------------------------- #
#  ContactManagementSystem (with temp storage)                               #
# --------------------------------------------------------------------------- #

@pytest.fixture
def cms_with_temp_storage():
    """CMS instance using a temporary JSON file (no side effects on real data)."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "contacts.json"
        storage = StorageManager(filepath=path)
        yield ContactManagementSystem(storage=storage)


def test_add_contact_success(cms_with_temp_storage):
    cms = cms_with_temp_storage
    ok, msg = cms.add_contact("New User", "9999888877", "new@test.com")
    assert ok is True
    assert "added successfully" in msg.lower()
    contacts = cms.view_contacts()
    assert len(contacts) == 1
    assert contacts[0].name == "New User"
    assert contacts[0].phone == "9999888877"
    assert contacts[0].email == "new@test.com"


def test_add_contact_duplicate_phone_fails(cms_with_temp_storage):
    cms = cms_with_temp_storage
    cms.add_contact("First", "8888777766", "")
    ok, msg = cms.add_contact("Second", "8888777766", "")
    assert ok is False
    assert "already exists" in msg.lower()
    assert len(cms.view_contacts()) == 1


def test_add_contact_requires_name_and_phone(cms_with_temp_storage):
    cms = cms_with_temp_storage
    ok1, _ = cms.add_contact("", "1111222233", "")
    ok2, _ = cms.add_contact("Name", "", "")
    assert ok1 is False
    assert ok2 is False


def test_add_contact_invalid_phone_fails(cms_with_temp_storage):
    cms = cms_with_temp_storage
    ok, msg = cms.add_contact("X", "123", "")
    assert ok is False
    assert "10 digits" in msg.lower()


def test_add_contact_valid_phone_with_91_prefix(cms_with_temp_storage):
    cms = cms_with_temp_storage
    ok, _ = cms.add_contact("India", "+91 9876543210", "")
    assert ok is True
    contacts = cms.view_contacts()
    assert contacts[0].phone == "9876543210"


def test_add_contact_invalid_email_fails(cms_with_temp_storage):
    cms = cms_with_temp_storage
    ok, msg = cms.add_contact("X", "9876543210", "not-an-email")
    assert ok is False
    assert "valid email" in msg.lower()


def test_search_empty_query_returns_all(cms_with_temp_storage):
    cms = cms_with_temp_storage
    cms.add_contact("A", "1111111111", "")
    cms.add_contact("B", "2222222222", "")
    assert len(cms.search_contact("")) == 2
    assert len(cms.search_contact("   ")) == 2


def test_search_filters_by_query(cms_with_temp_storage):
    cms = cms_with_temp_storage
    cms.add_contact("Alice", "1111111111", "alice@x.com")
    cms.add_contact("Bob", "2222222222", "bob@y.com")
    assert len(cms.search_contact("alice")) == 1
    assert len(cms.search_contact("2222")) == 1
    assert len(cms.search_contact("bob@y")) == 1
    assert len(cms.search_contact("zzz")) == 0


def test_update_contact_success(cms_with_temp_storage):
    cms = cms_with_temp_storage
    cms.add_contact("Old", "7777777777", "old@x.com")
    ok, msg = cms.update_contact("7777777777", "New", "7777777777", "new@y.com")
    assert ok is True
    contacts = cms.view_contacts()
    assert contacts[0].name == "New"
    assert contacts[0].email == "new@y.com"


def test_update_contact_change_phone(cms_with_temp_storage):
    cms = cms_with_temp_storage
    cms.add_contact("One", "6666666666", "")
    ok, _ = cms.update_contact("6666666666", "One", "5555555555", "")
    assert ok is True
    assert cms.view_contacts()[0].phone == "5555555555"


def test_update_contact_phone_collision_fails(cms_with_temp_storage):
    cms = cms_with_temp_storage
    cms.add_contact("First", "4444444444", "")
    cms.add_contact("Second", "3333333333", "")
    ok, msg = cms.update_contact("4444444444", "First", "3333333333", "")
    assert ok is False
    assert "already used" in msg.lower()


def test_update_contact_not_found_fails(cms_with_temp_storage):
    cms = cms_with_temp_storage
    ok, msg = cms.update_contact("0000000000", "X", "0000000000", "")
    assert ok is False
    assert "no contact found" in msg.lower()


def test_delete_contact_success(cms_with_temp_storage):
    cms = cms_with_temp_storage
    cms.add_contact("ToRemove", "1212121212", "")
    ok, msg = cms.delete_contact("1212121212")
    assert ok is True
    assert "deleted" in msg.lower()
    assert len(cms.view_contacts()) == 0


def test_delete_contact_not_found_fails(cms_with_temp_storage):
    cms = cms_with_temp_storage
    ok, msg = cms.delete_contact("0000000000")
    assert ok is False
    assert "no contact found" in msg.lower()
