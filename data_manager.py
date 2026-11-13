import json
from pathlib import Path

# Menentukan direktori folder 'data' berdasarkan posisi file data_manager.py
DATA_DIR = Path(__file__).parent / "data"

def load_json_file(filename: str):
    """Fungsi helper umum untuk membaca file JSON secara aman."""
    file_path = DATA_DIR / filename
    if not file_path.exists():
        print(f"File {filename} tidak ditemukan di {DATA_DIR}")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error saat membaca {filename}: {e}")
        return None

# --- Pengelola Data Wahana (Crafts/Wahana) ---
def get_all_crafts():
    """Mengambil semua data wahana antariksa."""
    return load_json_file("crafts.json")

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
    return load_json_file(filename)