import unittest

from sqlalchemy import create_engine, event, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, _enable_sqlite_foreign_keys
from app.models.artifact import Artifact
from app.models.lore_log import LoreLog
from app.models.user_unlock import UserUnlock
from app.schemas.artifact import ArtifactSummary


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        event.listen(self.engine, "connect", _enable_sqlite_foreign_keys)
        Base.metadata.create_all(self.engine)
        self.addCleanup(self.engine.dispose)

    def test_metadata_and_foreign_keys(self):
        with Session(self.engine) as db:
            artifact = Artifact(
                id="one", name="One", mission_name="Mission", artifact_type="probe",
                celestial_body="Moon", status="active", description="Description",
                historical_summary="History", telemetry_summary="Telemetry", metadata_={"key": "value"},
            )
            db.add(artifact)
            db.commit()
            self.assertEqual(ArtifactSummary.model_validate(artifact).model_dump()["metadata"], {"key": "value"})
            db.add(UserUnlock(artifact_id="one", session_id="session"))
            db.commit()
            db.execute(text("DELETE FROM artifacts WHERE id = 'one'"))
            db.commit()
            self.assertEqual(db.query(UserUnlock).count(), 0)
            db.add(UserUnlock(artifact_id="missing", session_id="session"))
            with self.assertRaises(IntegrityError):
                db.commit()


if __name__ == "__main__":
    unittest.main()
