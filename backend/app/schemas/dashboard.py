"""Pydantic schemas for dashboard, social, communications, public, auth."""

from __future__ import annotations
import uuid
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ── Auth ─────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = Field(default="LEADER", pattern="^(LEADER|DEPARTMENT_HEAD|WORKER|ADMIN)$")
    department: Optional[str] = None
    ward_id: Optional[int] = None
    phone: Optional[str] = None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut = None


class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: Optional[str] = None
    role: str
    department: Optional[str] = None
    ward_id: Optional[int] = None

    class Config:
        from_attributes = True


# ── Dashboard ────────────────────────────────────────────

class DashboardOverview(BaseModel):
    total_open: int
    total_critical: int
    resolved_today: int
    avg_trust_score: float
    total_complaints: int
    total_resolved: int
    trend_open: int  # change from yesterday
    trend_critical: int
    trend_resolved: int
    trend_trust: float


class WardHeatmapItem(BaseModel):
    ward_id: int
    ward_number: int
    ward_name: str
    latitude: Optional[float]
    longitude: Optional[float]
    total_complaints: int
    open_complaints: int
    critical_complaints: int


class SentimentTrendItem(BaseModel):
    date: date
    positive: int
    negative: int
    angry: int
    neutral: int
    avg_score: float


# ── Social ───────────────────────────────────────────────

class SocialPostOut(BaseModel):
    id: uuid.UUID
    platform: str
    post_url: Optional[str] = None
    post_text: Optional[str] = None
    author_handle: Optional[str] = None
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    extracted_category: Optional[str] = None
    extracted_ward: Optional[int] = None
    is_complaint: Optional[bool] = None
    is_misinformation: bool = False
    misinfo_confidence: Optional[float] = None
    misinfo_explanation: Optional[str] = None
    likes: int = 0
    shares: int = 0
    replies: int = 0
    virality_score: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SocialAlert(BaseModel):
    id: uuid.UUID
    post_text: str
    platform: str
    sentiment: str
    virality_score: int
    is_misinformation: bool
    misinfo_explanation: Optional[str] = None


# ── Communications ───────────────────────────────────────

class CommunicationGenerate(BaseModel):
    complaint_id: Optional[uuid.UUID] = None
    comm_type: str = Field(
        ...,
        pattern="^(ACKNOWLEDGMENT|PROGRESS|COMPLETION|CRISIS_RESPONSE|WEEKLY_DIGEST)$",
    )
    format: str = Field(default="whatsapp", pattern="^(whatsapp|social_media|official_notice)$")


class CommunicationOut(BaseModel):
    id: uuid.UUID
    complaint_id: Optional[uuid.UUID] = None
    comm_type: Optional[str] = None
    content_english: Optional[str] = None
    content_hindi: Optional[str] = None
    format: Optional[str] = None
    status: str
    approved_by: Optional[uuid.UUID] = None
    published_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Public Portal ────────────────────────────────────────

class WardScorecard(BaseModel):
    ward_id: int
    ward_name: str
    ward_number: int
    total_complaints: int
    total_resolved: int
    resolution_rate: float
    avg_response_hours: float
    trust_score: float


class PublicAction(BaseModel):
    complaint_id: uuid.UUID
    summary: str
    category: str
    status: str
    resolved_at: Optional[datetime] = None
    has_verification: bool = False


class TrustScoreOut(BaseModel):
    ward_id: int
    date: date
    resolution_rate: Optional[float] = None
    avg_response_hours: Optional[float] = None
    public_sentiment: Optional[float] = None
    transparency_score: Optional[float] = None
    communication_score: Optional[float] = None
    final_trust_score: Optional[float] = None

    class Config:
        from_attributes = True
