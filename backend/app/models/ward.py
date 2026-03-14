"""Ward model — administrative divisions."""

from sqlalchemy import String, Integer, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Ward(Base):
    __tablename__ = "wards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    ward_name: Mapped[str] = mapped_column(String(255), nullable=False)
    area_name: Mapped[str] = mapped_column(String(255), nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    is_vulnerable: Mapped[bool] = mapped_column(Boolean, default=False)
    latitude: Mapped[float] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[float] = mapped_column(Numeric(11, 8), nullable=True)

    # Relationships
    complaints = relationship("Complaint", back_populates="ward")
    users = relationship("User", back_populates="ward")
    citizens = relationship("Citizen", back_populates="ward")
    trust_scores = relationship("TrustScore", back_populates="ward")
