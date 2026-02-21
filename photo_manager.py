"""
photo_manager.py — Handles photo uploads and storage for contacts.
"""

import os
from pathlib import Path
from typing import Optional
import streamlit as st


class PhotoManager:
    """Manages contact photos stored in a local directory."""

    def __init__(self, photos_dir: str = "photos") -> None:
        """
        Initialize the photo manager.

        Parameters
        ----------
        photos_dir : str
            Directory name where photos will be stored (relative to script location).
        """
        self._photos_dir: Path = Path(__file__).parent.resolve() / photos_dir
        self._photos_dir.mkdir(exist_ok=True)

    def save_photo(self, uploaded_file, phone: str) -> Optional[str]:
        """
        Save an uploaded photo file.

        Parameters
        ----------
        uploaded_file : streamlit.UploadedFile
            The uploaded file object from st.file_uploader.
        phone : str
            Contact's phone number (used as part of filename for uniqueness).

        Returns
        -------
        str or None
            Filename of saved photo, or None if save failed.
        """
        if uploaded_file is None:
            return None

        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/gif"]
        if uploaded_file.type not in allowed_types:
            return None

        # Generate filename: phone_timestamp.extension
        file_ext = Path(uploaded_file.name).suffix or ".jpg"
        filename = f"{phone}_{uploaded_file.name}"
        # Sanitize filename (remove any path separators)
        filename = filename.replace("/", "_").replace("\\", "_")
        
        filepath = self._photos_dir / filename

        try:
            # Save the file
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return filename
        except Exception as e:
            st.error(f"Failed to save photo: {e}")
            return None

    def get_photo_path(self, filename: str) -> Optional[Path]:
        """
        Get the full path to a photo file.

        Parameters
        ----------
        filename : str
            The photo filename.

        Returns
        -------
        Path or None
            Full path to the photo, or None if file doesn't exist.
        """
        if not filename:
            return None
        filepath = self._photos_dir / filename
        return filepath if filepath.exists() else None

    def delete_photo(self, filename: str) -> bool:
        """
        Delete a photo file.

        Parameters
        ----------
        filename : str
            The photo filename to delete.

        Returns
        -------
        bool
            True if deleted successfully, False otherwise.
        """
        if not filename:
            return False
        try:
            filepath = self._photos_dir / filename
            if filepath.exists():
                filepath.unlink()
            return True
        except Exception:
            return False

    @property
    def photos_dir(self) -> Path:
        """Read-only path to the photos directory."""
        return self._photos_dir
