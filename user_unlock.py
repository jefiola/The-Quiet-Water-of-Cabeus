from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserUnlock(Base):
    __tablename__ = "user_unlocks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    artifact_id: Mapped[str] = mapped_column(String, ForeignKey("artifacts.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str] = mapped_column(String, index=True)
    unlock_type: Mapped[str] = mapped_column(String, default="artifact")
    unlocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    artifact: Mapped["Artifact"] = relationship(back_populates="unlocks")
