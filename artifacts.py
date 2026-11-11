from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas.artifact import (
    ArtifactDetail,
    ArtifactListResponse,
    ArtifactSummary,
    LoreLogListResponse,
    UnlockRequest,
    UnlockResponse,
)

router = APIRouter(prefix="/api/artifacts", tags=["artifacts"])


@router.get("", response_model=ArtifactListResponse)
def list_artifacts(db: Session = Depends(get_db)):
    artifacts = crud.artifact.list_artifacts(db)
    return {"items": [ArtifactSummary.model_validate(item).model_dump() for item in artifacts], "count": len(artifacts)}


@router.get("/{artifact_id}", response_model=ArtifactDetail)
def get_artifact(artifact_id: str, db: Session = Depends(get_db)):
    artifact = crud.artifact.get_artifact(db, artifact_id)
    if artifact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    return ArtifactDetail.model_validate(artifact)


@router.get("/{artifact_id}/logs", response_model=LoreLogListResponse)
def get_logs_for_artifact(artifact_id: str, db: Session = Depends(get_db)):
    artifact = crud.artifact.get_artifact(db, artifact_id)
    if artifact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")

    logs = crud.artifact.get_artifact_logs(db, artifact_id)
    return {
        "artifact_id": artifact_id,
        "count": len(logs),
        "logs": [
            {
                "id": log.id,
                "artifact_id": log.artifact_id,
                "sequence": log.sequence,
                "title": log.title,
                "log_type": log.log_type,
                "source_name": log.source_name,
                "transcript": log.transcript,
                "audio_url": log.audio_url,
                "image_url": log.image_url,
            }
            for log in logs
        ],
    }


@router.post("/unlock", response_model=UnlockResponse)
def unlock_artifact(payload: UnlockRequest, db: Session = Depends(get_db)):
    artifact = crud.artifact.get_artifact(db, payload.artifact_id)
    if artifact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")

    unlock, already_unlocked = crud.artifact.create_unlock(db, payload.artifact_id, payload.session_id)
    if already_unlocked:
        return UnlockResponse(
            message="Artifact was already unlocked for this session.",
            artifact_id=payload.artifact_id,
            session_id=payload.session_id,
            unlocked=True,
            already_unlocked=True,
        )

    return UnlockResponse(
        message="Artifact unlocked successfully.",
        artifact_id=payload.artifact_id,
        session_id=payload.session_id,
        unlocked=True,
        already_unlocked=False,
    )
