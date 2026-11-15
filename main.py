from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import json
import uuid

# Impor fungsi helper dari data_manager.py buatanmu
# (Pastikan path import sesuai dengan struktur foldermu)
try:
    from .data_manager import get_all_crafts, get_craft_by_id, get_story_chapter
except ImportError:
    from data_manager import get_all_crafts, get_craft_by_id, get_story_chapter

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

# In-memory storage untuk frontend events
frontend_events: List[Dict[str, Any]] = []
MAX_EVENTS = 1000

# Serve frontend static files
FRONTEND_DIR = Path(__file__).parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# API Documentation/Test Page
@app.get("/api", response_class=HTMLResponse)
def api_docs():
    crafts = get_all_crafts()
    craft_ids = [c.get("id") for c in crafts] if crafts else []
    craft_links = "".join(f'<li><a href="/api/crafts/{cid}">/api/crafts/{cid}</a> - {next((c["name"] for c in crafts if c["id"]==cid), "")}</li>' for cid in craft_ids)
    
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>The Quiet Water of Cabeus - API Docs</title>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; background: #02030a; color: #e8ecf4; }}
        h1 {{ color: #f0b35a; border-bottom: 1px solid #f0b35a; padding-bottom: 0.5rem; }}
        h2 {{ color: #7fb2ff; margin-top: 2rem; }}
        a {{ color: #7fb2ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{ background: #1a1f3a; padding: 0.2rem 0.4rem; border-radius: 4px; color: #f0b35a; }}
        ul {{ line-height: 2; }}
        .endpoint {{ background: #0a1020; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 3px solid #f0b35a; }}
        .method {{ display: inline-block; background: #f0b35a; color: #02030a; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: bold; margin-right: 1rem; font-size: 0.85rem; }}
        .links {{ display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }}
        .btn {{ background: rgba(10,16,30,.55); border: 1px solid #f0b35a; padding: 0.8rem 1.5rem; color: #f0b35a; text-decoration: none; border-radius: 4px; }}
        .btn:hover {{ background: #f0b35a; color: #02030a; }}
        .btn-secondary {{ border-color: #7fb2ff; color: #7fb2ff; }}
        .btn-secondary:hover {{ background: #7fb2ff; color: #02030a; }}
        .event-count {{ color: #f0b35a; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="links">
        <a href="/" class="btn">🎮 Open Visualization</a>
        <a href="/docs" class="btn">📖 Swagger UI</a>
        <a href="/redoc" class="btn">📘 ReDoc</a>
        <a href="/api/events" class="btn btn-secondary">📊 View Events ({len(frontend_events)})</a>
    </div>
    
    <h1>The Quiet Water of Cabeus - API Endpoints</h1>
    
    <div class="endpoint">
        <span class="method">GET</span><code>/</code> - Main visualization app
    </div>
    
    <h2>Crafts</h2>
    <div class="endpoint">
        <span class="method">GET</span><code>/api/crafts</code> - List all spacecraft
    </div>
    <ul>
        {craft_links}
    </ul>
    
    <h2>Story Chapters</h2>
    <div class="endpoint">
        <span class="method">GET</span><code>/api/story/1</code> - Chapter 1: The Question That Bugged Scientists
    </div>
    <div class="endpoint">
        <span class="method">GET</span><code>/api/story/2</code> - Chapter 2: The Long Journey
    </div>
    <div class="endpoint">
        <span class="method">GET</span><code>/api/story/3</code> - Chapter 3: The Impact
    </div>
    <div class="endpoint">
        <span class="method">GET</span><code>/api/story/4</code> - Chapter 4: The Discovery
    </div>
    
    <h2>Frontend Event Tracking</h2>
    <div class="endpoint">
        <span class="method">POST</span><code>/api/events</code> - Receive event from frontend (craft_select, chapter_view, etc.)
    </div>
    <div class="endpoint">
        <span class="method">GET</span><code>/api/events</code> - View all recorded events
    </div>
    <div class="endpoint">
        <span class="method">GET</span><code>/api/events/stats</code> - Event statistics summary
    </div>
    <div class="endpoint">
        <span class="method">DELETE</span><code>/api/events</code> - Clear all events
    </div>
    
    <h2>Auto-generated Docs</h2>
    <ul>
        <li><a href="/docs">Swagger UI</a> - Interactive API testing</li>
        <li><a href="/redoc">ReDoc</a> - Clean documentation</li>
    </ul>
</body>
</html>
"""

# 1. Endpoint Utama (Root) - Serve frontend
@app.get("/")
def read_root():
    return FileResponse(FRONTEND_DIR / "THE_QUIET_WATER_OF_CABEUS_v37_fixed.html")

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

# ===== FRONTEND EVENT TRACKING =====

@app.post("/api/events")
async def receive_frontend_event(request: Request):
    """Menerima event dari frontend (craft selection, chapter navigation, dll)"""
    try:
        body = await request.json()
    except:
        body = {}
    
    event = {
        "id": str(uuid.uuid4())[:8],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": body.get("type", "unknown"),
        "craft_id": body.get("craft_id"),
        "chapter": body.get("chapter"),
        "action": body.get("action"),
        "metadata": body.get("metadata", {}),
        "user_agent": request.headers.get("user-agent", ""),
        "ip": request.client.host if request.client else "unknown"
    }
    
    frontend_events.append(event)
    
    # Batasi jumlah event yang disimpan
    if len(frontend_events) > MAX_EVENTS:
        frontend_events.pop(0)
    
    print(f"[FRONTEND EVENT] {event['type']} - {event.get('craft_id') or event.get('chapter') or event.get('action')}")
    
    return {"success": True, "event_id": event["id"], "total_events": len(frontend_events)}

@app.get("/api/events")
def get_frontend_events(limit: int = 100, offset: int = 0):
    """Melihat semua event yang tercatat dari frontend"""
    events = frontend_events[offset:offset + limit]
    return {
        "success": True,
        "total": len(frontend_events),
        "limit": limit,
        "offset": offset,
        "data": list(reversed(events))  # Terbaru di atas
    }

@app.get("/api/events/stats")
def get_event_stats():
    """Statistik ringkasan event"""
    if not frontend_events:
        return {"success": True, "data": {"total_events": 0, "by_type": {}, "by_craft": {}, "by_chapter": {}}}
    
    by_type = {}
    by_craft = {}
    by_chapter = {}
    
    for e in frontend_events:
        # By type
        t = e.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
        
        # By craft
        if e.get("craft_id"):
            c = e["craft_id"]
            by_craft[c] = by_craft.get(c, 0) + 1
        
        # By chapter
        if e.get("chapter"):
            ch = str(e["chapter"])
            by_chapter[ch] = by_chapter.get(ch, 0) + 1
    
    return {
        "success": True,
        "data": {
            "total_events": len(frontend_events),
            "by_type": by_type,
            "by_craft": by_craft,
            "by_chapter": by_chapter,
            "first_event": frontend_events[0]["timestamp"] if frontend_events else None,
            "last_event": frontend_events[-1]["timestamp"] if frontend_events else None
        }
    }

@app.delete("/api/events")
def clear_frontend_events():
    """Hapus semua event"""
    global frontend_events
    count = len(frontend_events)
    frontend_events = []
    return {"success": True, "cleared": count}