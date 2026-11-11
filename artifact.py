from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, index=True)
    mission_name: Mapped[str] = mapped_column(String, index=True)
    artifact_type: Mapped[str] = mapped_column(String)
    celestial_body: Mapped[str] = mapped_column(String, index=True)
    region: Mapped[str | None] = mapped_column(String, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    altitude_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    historical_summary: Mapped[str] = mapped_column(Text)
    telemetry_summary: Mapped[str] = mapped_column(Text)
    last_known_status: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    discovered_by: Mapped[str | None] = mapped_column(String, nullable=True)
    media_links: Mapped[list[str]] = mapped_column(JSON, default=list)
    metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, default=dict, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    logs: Mapped[list["LoreLog"]] = relationship(back_populates="artifact", cascade="all, delete-orphan")
    unlocks: Mapped[list["UserUnlock"]] = relationship(back_populates="artifact", cascade="all, delete-orphan")
