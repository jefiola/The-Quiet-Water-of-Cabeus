import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.artifact import Artifact
from app.models.lore_log import LoreLog


def _load_fixture_data() -> list[dict]:
    fixture_path = Path(__file__).resolve().parent / "data" / "mock_data.json"
    with fixture_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def seed_database(db: Session) -> None:
    if db.query(Artifact).first():
        return

    for artifact_data in _load_fixture_data():
        artifact = Artifact(
            id=artifact_data["id"],
            name=artifact_data["name"],
            mission_name=artifact_data["mission_name"],
            artifact_type=artifact_data["artifact_type"],
            celestial_body=artifact_data["celestial_body"],
            region=artifact_data.get("region"),
            latitude=artifact_data.get("latitude"),
            longitude=artifact_data.get("longitude"),
            altitude_m=artifact_data.get("altitude_m"),
            status=artifact_data["status"],
            description=artifact_data["description"],
            historical_summary=artifact_data["historical_summary"],
            telemetry_summary=artifact_data["telemetry_summary"],
            last_known_status=artifact_data.get("last_known_status"),
            primary_image_url=artifact_data.get("primary_image_url"),
            discovered_by=artifact_data.get("discovered_by"),
            media_links=artifact_data.get("media_links", []),
            metadata_=artifact_data.get("metadata", {}),
        )
        db.add(artifact)
        db.flush()

        for log_data in artifact_data.get("logs", []):
            db.add(
                LoreLog(
                    artifact_id=artifact.id,
                    sequence=log_data["sequence"],
                    title=log_data["title"],
                    log_type=log_data.get("log_type", "transcript"),
                    source_name=log_data.get("source_name"),
                    transcript=log_data["transcript"],
                    audio_url=log_data.get("audio_url"),
                    image_url=log_data.get("image_url"),
                    discovered_at=log_data.get("discovered_at"),
                )
            )

    db.commit()
