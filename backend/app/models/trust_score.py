"""Trust score model — ward-wise daily scoring."""

from datetime import date
from sqlalchemy import Integer, Date, Numeric, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class TrustScore(Base):
    __tablename__ = "trust_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[int] = mapped_column(
        ForeignKey("wards.id"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)

    resolution_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    avg_response_hours: Mapped[float] = mapped_column(Numeric(8, 2), nullable=True)
    public_sentiment: Mapped[float] = mapped_column(Numeric(4, 3), nullable=True)
    transparency_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    communication_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    final_trust_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)

    # Relationships
    ward = relationship("Ward", back_populates="trust_scores")

    __table_args__ = (
        UniqueConstraint("ward_id", "date", name="uq_ward_date"),
        Index("idx_trust_scores_ward_date", "ward_id", date.desc()),
    )
