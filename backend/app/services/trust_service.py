"""Trust score calculator — composite ward-level scoring."""

import logging
from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.models.verification import Verification
from app.models.communication import Communication
from app.models.social_post import SocialPost
from app.models.trust_score import TrustScore

logger = logging.getLogger(__name__)


async def calculate_trust_score(ward_id: int, db: AsyncSession) -> dict:
    """
    Calculate ward trust score based on 5 components:
      1. Resolution rate (% complaints resolved)
      2. Average response hours
      3. Public sentiment (avg social media score)
      4. Transparency score (% work with verified proof)
      5. Communication score (comms published per complaint)

    Final = 0.30×Resolution + 0.25×ResponseTime + 0.20×Sentiment
          + 0.15×Transparency + 0.10×Communication
    """
    today = date.today()
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    # ── 1. Resolution rate ───────────────────────────────
    total_stmt = (
        select(func.count())
        .select_from(Complaint)
        .where(Complaint.ward_id == ward_id, Complaint.created_at >= thirty_days_ago)
    )
    resolved_stmt = (
        select(func.count())
        .select_from(Complaint)
        .where(
            Complaint.ward_id == ward_id,
            Complaint.created_at >= thirty_days_ago,
            Complaint.status.in_(["VERIFIED", "CLOSED"]),
        )
    )

    total_result = await db.execute(total_stmt)
    resolved_result = await db.execute(resolved_stmt)
    total = total_result.scalar() or 0
    resolved = resolved_result.scalar() or 0
    resolution_rate = (resolved / total * 100) if total > 0 else 50.0

    # ── 2. Average response hours ────────────────────────
    avg_hours_stmt = (
        select(
            func.avg(
                func.extract("epoch", Complaint.resolved_at - Complaint.created_at) / 3600
            )
        )
        .where(
            Complaint.ward_id == ward_id,
            Complaint.resolved_at.isnot(None),
            Complaint.created_at >= thirty_days_ago,
        )
    )
    avg_result = await db.execute(avg_hours_stmt)
    avg_hours = avg_result.scalar() or 48.0
    # Normalize: 0h → 100, 168h (1 week) → 0
    response_score = max(0, min(100, 100 - (float(avg_hours) / 168 * 100)))

    # ── 3. Public sentiment ──────────────────────────────
    sentiment_stmt = (
        select(func.avg(SocialPost.sentiment_score))
        .where(
            SocialPost.extracted_ward == ward_id,
            SocialPost.created_at >= thirty_days_ago,
        )
    )
    sent_result = await db.execute(sentiment_stmt)
    avg_sentiment = sent_result.scalar() or 0.0
    # Convert -1..+1 → 0..100
    sentiment_score = (float(avg_sentiment) + 1) * 50

    # ── 4. Transparency score ────────────────────────────
    verified_stmt = (
        select(func.count())
        .select_from(Verification)
        .join(Complaint, Verification.complaint_id == Complaint.id)
        .where(
            Complaint.ward_id == ward_id,
            Verification.verification_status == "VERIFIED",
            Verification.created_at >= thirty_days_ago,
        )
    )
    ver_result = await db.execute(verified_stmt)
    verified_count = ver_result.scalar() or 0
    transparency = (verified_count / resolved * 100) if resolved > 0 else 0.0

    # ── 5. Communication score ───────────────────────────
    comms_stmt = (
        select(func.count())
        .select_from(Communication)
        .join(Complaint, Communication.complaint_id == Complaint.id)
        .where(
            Complaint.ward_id == ward_id,
            Communication.status == "PUBLISHED",
            Communication.created_at >= thirty_days_ago,
        )
    )
    comms_result = await db.execute(comms_stmt)
    comms_count = comms_result.scalar() or 0
    comms_per_complaint = (comms_count / total * 100) if total > 0 else 0.0
    communication_score = min(100, comms_per_complaint)

    # ── Composite ────────────────────────────────────────
    final = (
        0.30 * resolution_rate
        + 0.25 * response_score
        + 0.20 * sentiment_score
        + 0.15 * transparency
        + 0.10 * communication_score
    )
    final = round(min(100, max(0, final)), 2)

    # Persist
    trust = TrustScore(
        ward_id=ward_id,
        date=today,
        resolution_rate=round(resolution_rate, 2),
        avg_response_hours=round(float(avg_hours), 2),
        public_sentiment=round(float(avg_sentiment), 3),
        transparency_score=round(transparency, 2),
        communication_score=round(communication_score, 2),
        final_trust_score=final,
    )

    # Upsert
    existing_stmt = select(TrustScore).where(
        TrustScore.ward_id == ward_id, TrustScore.date == today
    )
    existing = (await db.execute(existing_stmt)).scalar_one_or_none()
    if existing:
        existing.resolution_rate = trust.resolution_rate
        existing.avg_response_hours = trust.avg_response_hours
        existing.public_sentiment = trust.public_sentiment
        existing.transparency_score = trust.transparency_score
        existing.communication_score = trust.communication_score
        existing.final_trust_score = trust.final_trust_score
    else:
        db.add(trust)

    await db.flush()

    return {
        "ward_id": ward_id,
        "date": str(today),
        "resolution_rate": round(resolution_rate, 2),
        "avg_response_hours": round(float(avg_hours), 2),
        "response_score": round(response_score, 2),
        "public_sentiment": round(float(avg_sentiment), 3),
        "sentiment_score": round(sentiment_score, 2),
        "transparency_score": round(transparency, 2),
        "communication_score": round(communication_score, 2),
        "final_trust_score": final,
    }
