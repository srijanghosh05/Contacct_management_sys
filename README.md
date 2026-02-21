# Directory ? Contact Management System

A sleek, dark-mode contact directory built with **Python** and **Streamlit**. Manage your contacts with a modern UI: add photos, search instantly, edit or delete with confirmation, and keep everything in sync with local JSON storage.

---

## Features

| Feature | Description |
|--------|-------------|
| **All Contacts** | View all contacts in one place, sorted alphabetically by name |
| **Search** | Search by name, phone, or email ? results update as you type |
| **Add Contact** | Create new contacts with name, phone, email, and an optional photo |
| **Photo** | Upload a profile photo per contact (JPG, PNG, WebP, GIF); fallback to initials |
| **Edit** | Update any contact's details or photo from the Manage expander |
| **Delete** | Remove contacts with a two-step confirmation to avoid accidents |
| **Local storage** | Data and photos stored locally (JSON + `photos/` folder); no account required |
| **Dark UI** | Polished dark theme with gradients, smooth animations, and clear typography |

---

## Requirements

- **Python** 3.8 or higher
- **Streamlit** (see `requirements.txt`)

---

## Quick Start

### 1. Get the project

Clone or download this repo and open a terminal in the project folder:

```bash
cd pep_pro
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Windows (CMD):** `.venv\Scripts\activate.bat`
- **macOS / Linux:** `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens in your browser (usually `http://localhost:8501`). You're ready to add and manage contacts.

---

## How to Use

1. **All Contacts** ? See every contact in alphabetical order. Use the search box to filter by name, phone, or email. Open **Manage Contact Details** under a card to edit or delete.

2. **Add New Contact** ? Fill in **Full Name** and **Phone** (required). Optionally add **Email** and a **Photo**. Phone must be 10 digits; you can use an optional `+91` prefix (e.g. `+91 9876543210`).

3. **Editing** ? In **Manage Contact Details**, change name, phone, email, or upload a new photo. Click **Save Changes** to apply.

4. **Deleting** ? Click **Delete [Name]**, then confirm with **Yes, delete**. The contact and its photo (if any) are removed.

---

## Running Tests

Optional: run the test suite for the contact logic and storage:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

`requirements-dev.txt` includes the main app dependencies plus **pytest**.

---

## Project Structure

| File / folder | Purpose |
|--------------|---------|
| `app.py` | Streamlit UI: pages, forms, styling, photo display |
| `cms.py` | Contact model and ContactManagementSystem (CRUD, validation) |
| `storage_manager.py` | Load/save contacts to `contacts.json` |
| `photo_manager.py` | Save, load, and delete contact photos in `photos/` |
| `contacts.json` | Contact data (created on first run; in `.gitignore`) |
| `photos/` | Uploaded contact photos (in `.gitignore`) |
| `tests/` | Unit tests for `cms` and `storage_manager` |
| `requirements.txt` | App dependencies (e.g. Streamlit) |
| `requirements-dev.txt` | App + dev dependencies (e.g. pytest) |

---

## Notes

- **Phone validation:** Exactly 10 digits; optional `+91` or `91` prefix; spaces, hyphens, and dots are ignored.
- **Data location:** Contacts are stored in `contacts.json` next to the app; photos go in the `photos/` directory.
- **Privacy:** `contacts.json` and `photos/` are listed in `.gitignore` so your data and photos are not committed to git.

---

## Tech Stack

- **Python 3.8+**
- **Streamlit** -> UI and file uploads
- **pathlib** -> Cross-platform paths

---

Enjoy your contact directory. For issues or ideas, open an issue or extend the code to fit your workflow.
