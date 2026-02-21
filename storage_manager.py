"""
storage_manager.py — Handles persistent storage via JSON.
Cross-platform file paths using pathlib.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class StorageManager:
    """Manages reading and writing contact data to a local JSON file."""

    def __init__(
        self,
        filename: str = "contacts.json",
        filepath: Optional[Path] = None,
    ) -> None:
        if filepath is not None:
            self._filepath: Path = Path(filepath)
        else:
            # Resolve relative to the directory where this script lives
            self._filepath = Path(__file__).parent.resolve() / filename

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def load(self) -> List[Dict[str, Any]]:
        """
        Load contacts from the JSON file.

        Returns an empty list when the file does not exist or is corrupt,
        so the application always starts in a usable state.
        """
        if not self._filepath.exists():
            return []

        try:
            with self._filepath.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
                if not isinstance(data, list):
                    return []
                return data
        except (json.JSONDecodeError, OSError) as exc:
            # Log to stderr so it doesn't pollute the Streamlit UI.
            import sys
            print(f"[StorageManager] Failed to load '{self._filepath}': {exc}", file=sys.stderr)
            return []

    def save(self, contacts: List[Dict[str, Any]]) -> bool:
        """
        Save contacts to the JSON file (human-readable, indented).

        Returns True on success, False on failure.
        """
        try:
            with self._filepath.open("w", encoding="utf-8") as fh:
                json.dump(contacts, fh, indent=4, ensure_ascii=False)
            return True
        except OSError as exc:
            import sys
            print(f"[StorageManager] Failed to save '{self._filepath}': {exc}", file=sys.stderr)
            return False

    @property
    def filepath(self) -> Path:
        """Read-only path to the underlying JSON file."""
        return self._filepath
