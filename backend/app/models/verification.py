"""Verification model — work completion proof."""

import uuid
from datetime import datetime
from sqlalchemy import (
    String, Boolean, Text, DateTime, Numeric, ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Verification(Base):
    __tablename__ = "verifications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    complaint_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("complaints.id"), nullable=False
    )

    # Before evidence (from complaint)
    before_image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    before_latitude: Mapped[float] = mapped_column(Numeric(10, 8), nullable=True)
    before_longitude: Mapped[float] = mapped_column(Numeric(11, 8), nullable=True)
    before_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # After evidence (from worker)
    after_image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    after_latitude: Mapped[float] = mapped_column(Numeric(10, 8), nullable=True)
    after_longitude: Mapped[float] = mapped_column(Numeric(11, 8), nullable=True)
    after_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # AI verification results
    location_match: Mapped[bool] = mapped_column(Boolean, nullable=True)
    time_valid: Mapped[bool] = mapped_column(Boolean, nullable=True)
    visual_change_detected: Mapped[bool] = mapped_column(Boolean, nullable=True)
    visual_change_confidence: Mapped[float] = mapped_column(
        Numeric(3, 2), nullable=True
    )
    tamper_detected: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # Final verdict
    verification_status: Mapped[str] = mapped_column(
        String(20), nullable=True
    )  # VERIFIED, REJECTED, MANUAL_REVIEW
    overall_confidence: Mapped[float] = mapped_column(Numeric(3, 2), nullable=True)
    ai_remarks: Mapped[str] = mapped_column(Text, nullable=True)

    verified_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    complaint = relationship("Complaint", back_populates="verifications")
    verifier = relationship("User", foreign_keys=[verified_by])
