from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ArtifactSummary(BaseModel):
    id: str
    name: str
    mission_name: str
    artifact_type: str
    celestial_body: str
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    status: str
    description: str
    primary_image_url: str | None = None
    telemetry_summary: str | None = None
    metadata: dict[str, Any] | None = Field(default=None, validation_alias=AliasChoices("metadata_", "metadata"))

    model_config = ConfigDict(from_attributes=True)


class ArtifactDetail(ArtifactSummary):
    historical_summary: str
    last_known_status: str | None = None
    media_links: list[str] = Field(default_factory=list)
    discovered_by: str | None = None


class LoreLogPublic(BaseModel):
    id: str
    artifact_id: str
    sequence: int
    title: str
    log_type: str
    source_name: str | None = None
    transcript: str
    audio_url: str | None = None
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ArtifactListResponse(BaseModel):
    items: list[ArtifactSummary]
    count: int


class LoreLogListResponse(BaseModel):
    artifact_id: str
    count: int
    logs: list[LoreLogPublic]


class UnlockRequest(BaseModel):
    artifact_id: str
    session_id: str
    secret_token: str | None = None


class UnlockResponse(BaseModel):
    message: str
    artifact_id: str
    session_id: str
    unlocked: bool
    already_unlocked: bool
