from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.artifacts import router as artifacts_router
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models import Artifact, LoreLog, UserUnlock  # noqa: F401
from app.seed import seed_database


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="NASA abandoned equipment lore-driven storytelling API.",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


app.include_router(artifacts_router)
