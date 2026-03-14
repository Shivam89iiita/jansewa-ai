"""Pydantic schemas for verification."""

from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class VerificationCreate(BaseModel):
    after_image_url: str
    after_latitude: Optional[float] = None
    after_longitude: Optional[float] = None
    after_timestamp: Optional[datetime] = None


class VerificationApproval(BaseModel):
    approved: bool
    remarks: Optional[str] = None


class VerificationOut(BaseModel):
    id: uuid.UUID
    complaint_id: uuid.UUID

    before_image_url: Optional[str] = None
    before_latitude: Optional[float] = None
    before_longitude: Optional[float] = None
    before_timestamp: Optional[datetime] = None

    after_image_url: Optional[str] = None
    after_latitude: Optional[float] = None
    after_longitude: Optional[float] = None
    after_timestamp: Optional[datetime] = None

    location_match: Optional[bool] = None
    time_valid: Optional[bool] = None
    visual_change_detected: Optional[bool] = None
    visual_change_confidence: Optional[float] = None
    tamper_detected: Optional[bool] = None

    verification_status: Optional[str] = None
    overall_confidence: Optional[float] = None
    ai_remarks: Optional[str] = None

    verified_by: Optional[uuid.UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True
