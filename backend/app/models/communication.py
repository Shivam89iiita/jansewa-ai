"""Communication model — AI-generated public messages."""

import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Communication(Base):
    __tablename__ = "communications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    complaint_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("complaints.id"), nullable=True
    )
    comm_type: Mapped[str] = mapped_column(
        String(30), nullable=True
    )  # ACKNOWLEDGMENT, PROGRESS, COMPLETION, CRISIS_RESPONSE, WEEKLY_DIGEST
    content_english: Mapped[str] = mapped_column(Text, nullable=True)
    content_hindi: Mapped[str] = mapped_column(Text, nullable=True)
    format: Mapped[str] = mapped_column(
        String(20), nullable=True
    )  # whatsapp, social_media, official_notice

    status: Mapped[str] = mapped_column(
        String(20), default="DRAFT"
    )  # DRAFT, APPROVED, PUBLISHED
    approved_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    complaint = relationship("Complaint", back_populates="communications")
    approver = relationship("User", foreign_keys=[approved_by])
