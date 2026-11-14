import json
from pathlib import Path

# Menentukan direktori folder 'data' berdasarkan posisi file data_manager.py
DATA_DIR = Path(__file__).parent / "data"

def load_json_file(filename: str):
    """Membaca file JSON; kesalahan data diteruskan ke pemanggil."""
    file_path = DATA_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Pengelola Data Wahana (Crafts/Wahana) ---
def get_all_crafts():
    """Mengambil semua data wahana antariksa."""
    crafts = load_json_file("crafts.json")
    if not isinstance(crafts, list) or any(not isinstance(craft, dict) for craft in crafts):
        raise ValueError("crafts.json must contain an array of objects")
    return crafts

def get_craft_by_id(craft_id: str):
    """Mencari data wahana spesifik berdasarkan ID."""
    crafts = get_all_crafts()
    if not crafts:
        return None
    for craft in crafts:
        if craft.get("id") == craft_id:
            return craft
    return None

# --- Pengelola Naskah Cerita Per Chapter ---
def get_story_chapter(chapter_number: int):
    """Mengambil naskah cerita interaktif berdasarkan nomor chapter."""
    filename = f"lcross_chapter{chapter_number}.json"
    try:
        story = load_json_file(filename)
    except FileNotFoundError:
        if not DATA_DIR.is_dir():
            raise
        return None
    if not isinstance(story, dict):
        raise ValueError(f"{filename} must contain an object")
    return story
