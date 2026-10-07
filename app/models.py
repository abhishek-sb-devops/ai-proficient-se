import time
import re
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field, validator


class ShortenRequest(BaseModel):
    """DTO for incoming shorten URL payload."""

    url: HttpUrl = Field(..., description="The original long URL to shorten.")
    custom_alias: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=30,
        description="Optional custom slug (alphanumeric, hyphens, underscores).",
    )

    @validator("custom_alias")
    def validate_alias_format(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            if not re.match(r"^[a-zA-Z0-9_-]+$", value):
                raise ValueError("Custom alias contains invalid characters.")
        return value


class URLRecord(BaseModel):
    """Domain model representing stored URL metadata."""

    short_code: str
    original_url: str
    created_at: float = Field(default_factory=time.time)


class AnalyticsResponse(BaseModel):
    """DTO for returning URL click statistics."""

    short_code: str
    original_url: str
    total_clicks: int
    created_at: float