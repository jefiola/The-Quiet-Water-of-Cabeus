from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.artifact import Artifact
from app.models.lore_log import LoreLog
from app.models.user_unlock import UserUnlock


def list_artifacts(db: Session):
    return db.scalars(select(Artifact).order_by(Artifact.name)).all()


def get_artifact(db: Session, artifact_id: str):
    return db.get(Artifact, artifact_id)


def get_artifact_logs(db: Session, artifact_id: str):
    return (
        db.scalars(
            select(LoreLog)
            .where(LoreLog.artifact_id == artifact_id)
            .order_by(LoreLog.sequence)
        )
        .all()
    )


def get_unlock(db: Session, artifact_id: str, session_id: str):
    return db.scalar(
        select(UserUnlock).where(UserUnlock.artifact_id == artifact_id, UserUnlock.session_id == session_id)
    )


def create_unlock(db: Session, artifact_id: str, session_id: str):
    existing = get_unlock(db, artifact_id, session_id)
    if existing:
        return existing, True

    unlock = UserUnlock(artifact_id=artifact_id, session_id=session_id)
    db.add(unlock)
    db.commit()
    db.refresh(unlock)
    return unlock, False
