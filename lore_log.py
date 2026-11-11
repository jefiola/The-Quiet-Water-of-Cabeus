from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LoreLog(Base):
    __tablename__ = "lore_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    artifact_id: Mapped[str] = mapped_column(String, ForeignKey("artifacts.id", ondelete="CASCADE"), index=True)
    sequence: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String)
    log_type: Mapped[str] = mapped_column(String, default="transcript")
    source_name: Mapped[str | None] = mapped_column(String, nullable=True)
    transcript: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(String, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    discovered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    artifact: Mapped["Artifact"] = relationship(back_populates="logs")
