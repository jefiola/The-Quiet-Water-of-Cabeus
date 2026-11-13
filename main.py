from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Impor fungsi helper dari data_manager.py buatanmu
# (Pastikan path import sesuai dengan struktur foldermu)
from .data_manager import get_all_crafts, get_craft_by_id, get_story_chapter

app = FastAPI(
    title="NASA Space Apps Hackathon - The Quiet Water of Cabeus API",
    version="1.0.0"
)

# Konfigurasi CORS (Sangat penting agar Frontend bisa komunikasi dengan Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua origin untuk kemudahan development hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Endpoint Utama (Root)
@app.get("/")
def read_root():
    return {
        "project": "The Quiet Water of Cabeus",
        "theme": "Abandoned but Not Forgotten (NASA Space Apps)",
        "status": "Backend is running smoothly!"
    }

# 2. Endpoint untuk Mengambil Semua Data Wahana Antariksa
@app.get("/api/crafts")
def api_get_all_crafts():
    crafts = get_all_crafts()
    if not crafts:
        raise HTTPException(status_code=404, detail="Data wahana antariksa tidak ditemukan.")
    return {"success": True, "data": crafts}

# 3. Endpoint untuk Mengambil Detail Wahana Berdasarkan ID (misal: /api/crafts/lcross)
@app.get("/api/crafts/{craft_id}")
def api_get_craft_by_id(craft_id: str):
    craft = get_craft_by_id(craft_id)
    if not craft:
        raise HTTPException(status_code=404, detail=f"Wahana dengan ID '{craft_id}' tidak ditemukan.")
    return {"success": True, "data": craft}

# 4. Endpoint untuk Mengambil Naskah Cerita Berdasarkan Chapter (misal: /api/story/1)
@app.get("/api/story/{chapter_number}")
def api_get_story_chapter(chapter_number: int):
    story = get_story_chapter(chapter_number)
    if not story:
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_number} tidak ditemukan.")
    return {"success": True, "data": story}