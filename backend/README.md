# NASA Mission Lore API

A FastAPI backend for a lore-driven web event about spacecraft on the Moon.

## Features

- Spacecraft catalog loaded from `app/data/crafts.json`
- LCROSS story chapters loaded from `app/data/lcross_chapter<N>.json`

## Local setup

1. Open a terminal in the project root.
2. Create and activate a virtual environment:

   PowerShell:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the API server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Open the interactive API docs:
   - http://localhost:8000/docs
   - http://localhost:8000/redoc

## Available API endpoints

- `GET /`
- `GET /api/crafts`
- `GET /api/crafts/{craft_id}`
- `GET /api/story/{chapter_number}`

## Tests

```bash
python -m unittest -v test_data_api
```
