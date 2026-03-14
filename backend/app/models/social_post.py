"""Social media post model."""

import uuid
from datetime import datetime
from sqlalchemy import (
    String, Integer, Boolean, Text, DateTime, Numeric, ForeignKey, Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class SocialPost(Base):
    __tablename__ = "social_posts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    platform: Mapped[str] = mapped_column(String(20), nullable=False)
    post_url: Mapped[str] = mapped_column(String(500), nullable=True)
    post_text: Mapped[str] = mapped_column(Text, nullable=True)
    author_handle: Mapped[str] = mapped_column(String(255), nullable=True)

    # AI analysis
    sentiment: Mapped[str] = mapped_column(String(20), nullable=True)
    sentiment_score: Mapped[float] = mapped_column(Numeric(4, 3), nullable=True)
    extracted_category: Mapped[str] = mapped_column(String(100), nullable=True)
    extracted_ward: Mapped[int] = mapped_column(Integer, nullable=True)
    is_complaint: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_misinformation: Mapped[bool] = mapped_column(Boolean, default=False)
    misinfo_confidence: Mapped[float] = mapped_column(Numeric(3, 2), nullable=True)
    misinfo_explanation: Mapped[str] = mapped_column(Text, nullable=True)

    # Engagement metrics
    likes: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    replies: Mapped[int] = mapped_column(Integer, default=0)
    virality_score: Mapped[int] = mapped_column(Integer, nullable=True)

    linked_complaint_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("complaints.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    linked_complaint = relationship("Complaint")

    __table_args__ = (
        Index("idx_social_posts_sentiment", "sentiment"),
    )
