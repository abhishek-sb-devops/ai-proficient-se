from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class ShortenRequest(BaseModel):
    original_url: HttpUrl = Field(..., description="The original target URL to shorten")
    custom_alias: Optional[str] = Field(None, description="Optional custom alias for the URL")


class ShortenResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: str


class AnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: str
    total_clicks: int = Field(..., description="Total redirect clicks recorded")
