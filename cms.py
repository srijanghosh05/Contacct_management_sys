"""
cms.py — Core business logic for the Contact Management System.

Classes
-------
Contact
    Represents a single contact with name, phone, and email.
ContactManagementSystem
    Manages a collection of Contact objects with O(1) duplicate detection.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple

from storage_manager import StorageManager


# --------------------------------------------------------------------------- #
#  Contact                                                                    #
# --------------------------------------------------------------------------- #

@dataclass
class Contact:
    """A simple contact record."""

    name: str
    phone: str
    email: str
    photo: str = ""  # Filename of the photo, empty if no photo

    # ------------------------------------------------------------------ #
    #  Serialization                                                     #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Contact":
        """Reconstruct a Contact from a dictionary (e.g. loaded from JSON)."""
        return cls(
            name=str(data.get("name", "")).strip(),
            phone=str(data.get("phone", "")).strip(),
            email=str(data.get("email", "")).strip(),
            photo=str(data.get("photo", "")).strip(),  # Backward compatible: defaults to empty
        )

    # ------------------------------------------------------------------ #
    #  Helpers                                                           #
    # ------------------------------------------------------------------ #

    def matches(self, query: str) -> bool:
        """Case-insensitive search across all fields."""
        q = query.lower()
        return (
            q in self.name.lower()
            or q in self.phone.lower()
            or q in self.email.lower()
        )

    def __str__(self) -> str:
        return f"{self.name} | {self.phone} | {self.email}"


# --------------------------------------------------------------------------- #
#  ContactManagementSystem                                                    #
# --------------------------------------------------------------------------- #

class ContactManagementSystem:
    """
    Manages contacts using:
    - A ``list`` for ordered storage and iteration.
    - A ``set`` of phone numbers for O(1) duplicate detection.
    """

    def __init__(self, storage: Optional[StorageManager] = None) -> None:
        self._contacts: List[Contact] = []
        self._phone_set: set = set()          # O(1) duplicate guard
        self._storage: StorageManager = storage if storage is not None else StorageManager()
        self._load_from_disk()

    # ------------------------------------------------------------------ #
    #  Persistence                                                       #
    # ------------------------------------------------------------------ #

    def _load_from_disk(self) -> None:
        """Populate internal state from the JSON file on startup."""
        raw = self._storage.load()
        for record in raw:
            contact = Contact.from_dict(record)
            if contact.phone and contact.phone not in self._phone_set:
                self._contacts.append(contact)
                self._phone_set.add(contact.phone)

    def _persist(self) -> bool:
        """Write current state back to disk."""
        return self._storage.save([c.to_dict() for c in self._contacts])

    # ------------------------------------------------------------------ #
    #  CRUD                                                                #
    # ------------------------------------------------------------------ #

    def add_contact(
        self, name: str, phone: str, email: str, photo: str = ""
    ) -> Tuple[bool, str]:
        """
        Add a new contact.

        Parameters
        ----------
        photo : str
            Filename of the photo (empty string if no photo).

        Returns
        -------
        (True, success_message) on success.
        (False, error_message) on failure.
        """
        name, phone, email = name.strip(), phone.strip(), email.strip()
        photo = photo.strip()

        if not name or not phone:
            return False, "Name and phone number are required."

        if not _valid_phone(phone):
            return False, "Phone number must be exactly 10 digits (excluding the +91 country code)."

        if phone in self._phone_set:
            return False, f"A contact with phone '{phone}' already exists."

        if email and not _valid_email(email):
            return False, "Please enter a valid email address."

        contact = Contact(name=name, phone=phone, email=email, photo=photo)
        self._contacts.append(contact)
        self._phone_set.add(phone)
        self._persist()
        return True, f"Contact '{name}' added successfully."

    def view_contacts(self) -> List[Contact]:
        """Return all contacts (read-only view)."""
        return list(self._contacts)

    def search_contact(self, query: str) -> List[Contact]:
        """Return contacts whose name, phone, or email contains *query*."""
        if not query.strip():
            return list(self._contacts)
        return [c for c in self._contacts if c.matches(query)]

    def update_contact(
        self,
        original_phone: str,
        new_name: str,
        new_phone: str,
        new_email: str,
        new_photo: str = "",
    ) -> Tuple[bool, str]:
        """
        Update an existing contact identified by *original_phone*.

        Parameters
        ----------
        new_photo : str
            Filename of the photo (empty string to keep existing or remove).

        Returns (success, message).
        """
        new_name = new_name.strip()
        new_phone = new_phone.strip()
        new_email = new_email.strip()
        new_photo = new_photo.strip()

        if not new_name or not new_phone:
            return False, "Name and phone number are required."

        if not _valid_phone(new_phone):
            return False, "Phone number must be exactly 10 digits (excluding the +91 country code)."

        if new_email and not _valid_email(new_email):
            return False, "Please enter a valid email address."

        for idx, contact in enumerate(self._contacts):
            if contact.phone == original_phone:
                # Phone changed → check for collision
                if new_phone != original_phone and new_phone in self._phone_set:
                    return False, f"Phone '{new_phone}' is already used by another contact."

                # Use existing photo if new_photo is empty (keep current photo)
                photo_to_use = new_photo if new_photo else contact.photo

                # Apply update
                self._phone_set.discard(original_phone)
                self._contacts[idx] = Contact(
                    name=new_name, phone=new_phone, email=new_email, photo=photo_to_use
                )
                self._phone_set.add(new_phone)
                self._persist()
                return True, f"Contact updated successfully."

        return False, f"No contact found with phone '{original_phone}'."

    def delete_contact(self, phone: str) -> Tuple[bool, str]:
        """
        Delete the contact with *phone*.

        Note: This does not delete the photo file. Photo cleanup should be handled
        by the caller if needed.

        Returns (success, message).
        """
        phone = phone.strip()
        for idx, contact in enumerate(self._contacts):
            if contact.phone == phone:
                removed = self._contacts.pop(idx)
                self._phone_set.discard(phone)
                self._persist()
                return True, f"Contact '{removed.name}' deleted."

        return False, f"No contact found with phone '{phone}'."


# --------------------------------------------------------------------------- #
#  Validation helpers                                                          #
# --------------------------------------------------------------------------- #

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Matches exactly 10 digits after an optional +91 / 91 prefix
# (spaces, hyphens, and dots between digits are ignored before counting)
_PHONE_PREFIX_RE = re.compile(r"^(?:\+?91[\s\-.]?)?")


def _valid_phone(phone: str) -> bool:
    """
    Return True if *phone* contains exactly 10 digits after stripping
    an optional leading +91 / 91 country code and any separators.

    Valid examples
    --------------
    9876543210          → ✓
    +91 98765 43210     → ✓
    91-9876-543210      → ✓
    +919876543210       → ✓
    12345               → ✗  (too short)
    +1 9876543210       → ✗  (wrong country code)
    """
    # Strip leading country code (+91 or 91)
    stripped = _PHONE_PREFIX_RE.sub("", phone.strip())
    # Remove separators (spaces, hyphens, dots)
    digits = re.sub(r"[\s\-.]", "", stripped)
    return digits.isdigit() and len(digits) == 10


def _valid_email(email: str) -> bool:
    return bool(_EMAIL_RE.match(email))
