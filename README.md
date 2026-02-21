# pep_pro — Contact Management System

A minimal contact directory built with Python and Streamlit. Add, search, edit, and delete contacts with a dark-mode UI. Data is stored in a local JSON file.

## Requirements

- Python 3.8+
- Streamlit

## Setup

1. Clone or download this project and open a terminal in the project folder.

2. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the app

```bash
streamlit run app.py
```

The app will open in your browser. Use the **All Contacts** tab to view and search, and **Add New Contact** to create entries. Phone numbers must be 10 digits (optional `+91` prefix). Edit or delete contacts via the expander under each card; delete requires confirmation.

## Running tests

To run the test suite (optional):

```bash
pip install -r requirements-dev.txt
pytest
```

## Project layout

- `app.py` — Streamlit UI and styling
- `cms.py` — Contact model and business logic (CRUD, validation)
- `storage_manager.py` — JSON file read/write
- `contacts.json` — Stored contacts (created on first run; ignored by git)
