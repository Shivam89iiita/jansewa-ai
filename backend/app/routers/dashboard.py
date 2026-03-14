"""Dashboard router — overview, heatmap, sentiment trends, trust scores."""

from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.complaint import Complaint
from app.models.ward import Ward
from app.models.social_post import SocialPost
from app.models.trust_score import TrustScore
from app.schemas.dashboard import (
    DashboardOverview,
    WardHeatmapItem,
    SentimentTrendItem,
    TrustScoreOut,
)

router = APIRouter()


@router.get("/overview", response_model=DashboardOverview)
async def dashboard_overview(db: AsyncSession = Depends(get_db)):
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)

    # Current counts
    total = (await db.execute(select(func.count()).select_from(Complaint))).scalar() or 0
    total_open = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"])
        )
    )).scalar() or 0
    total_critical = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.priority_level == "CRITICAL",
            Complaint.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"]),
        )
    )).scalar() or 0
    resolved_today = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.status.in_(["VERIFIED", "CLOSED"]),
            Complaint.resolved_at >= today_start,
        )
    )).scalar() or 0
    total_resolved = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.status.in_(["VERIFIED", "CLOSED"])
        )
    )).scalar() or 0

    # Trends (yesterdays)
    yesterday_open = (await db.execute(
        select(func.count()).select_from(Complaint).where(
            Complaint.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"]),
            Complaint.created_at < today_start,
        )
    )).scalar() or 0

    # Avg trust
    avg_trust = (await db.execute(
        select(func.avg(TrustScore.final_trust_score))
    )).scalar() or 72.5

    return DashboardOverview(
        total_open=total_open,
        total_critical=total_critical,
        resolved_today=resolved_today,
        avg_trust_score=round(float(avg_trust), 1),
        total_complaints=total,
        total_resolved=total_resolved,
        trend_open=total_open - yesterday_open,
        trend_critical=0,
        trend_resolved=resolved_today,
        trend_trust=0.0,
    )


@router.get("/ward-heatmap", response_model=list[WardHeatmapItem])
async def ward_heatmap(db: AsyncSession = Depends(get_db)):
    wards = (await db.execute(select(Ward))).scalars().all()
    result = []
    for w in wards:
        total = (await db.execute(
            select(func.count()).select_from(Complaint).where(Complaint.ward_id == w.id)
        )).scalar() or 0
        open_c = (await db.execute(
            select(func.count()).select_from(Complaint).where(
                Complaint.ward_id == w.id,
                Complaint.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"]),
            )
        )).scalar() or 0
        critical = (await db.execute(
            select(func.count()).select_from(Complaint).where(
                Complaint.ward_id == w.id,
                Complaint.priority_level == "CRITICAL",
            )
        )).scalar() or 0

        result.append(WardHeatmapItem(
            ward_id=w.id,
            ward_number=w.ward_number,
            ward_name=w.ward_name,
            latitude=float(w.latitude) if w.latitude else None,
            longitude=float(w.longitude) if w.longitude else None,
            total_complaints=total,
            open_complaints=open_c,
            critical_complaints=critical,
        ))
    return result


@router.get("/sentiment-trend", response_model=list[SentimentTrendItem])
async def sentiment_trend(
    days: int = Query(30, ge=7, le=90),
    db: AsyncSession = Depends(get_db),
):
    """Daily sentiment breakdown over the last N days."""
    start_date = datetime.utcnow() - timedelta(days=days)
    stmt = (
        select(
            cast(SocialPost.created_at, Date).label("day"),
            SocialPost.sentiment,
            func.count().label("cnt"),
            func.avg(SocialPost.sentiment_score).label("avg_score"),
        )
        .where(SocialPost.created_at >= start_date)
        .group_by("day", SocialPost.sentiment)
        .order_by("day")
    )
    rows = (await db.execute(stmt)).all()

    # Pivot by day
    day_data: dict = {}
    for row in rows:
        d = row.day
        if d not in day_data:
            day_data[d] = {"positive": 0, "negative": 0, "angry": 0, "neutral": 0, "scores": []}
        sent = (row.sentiment or "NEUTRAL").lower()
        if sent in day_data[d]:
            day_data[d][sent] += row.cnt
        day_data[d]["scores"].append(float(row.avg_score or 0))

    result = []
    for d in sorted(day_data.keys()):
        dd = day_data[d]
        scores = dd.pop("scores")
        result.append(SentimentTrendItem(
            date=d,
            positive=dd["positive"],
            negative=dd["negative"],
            angry=dd["angry"],
            neutral=dd["neutral"],
            avg_score=round(sum(scores) / len(scores), 3) if scores else 0,
        ))
    return result


@router.get("/trust-scores", response_model=list[TrustScoreOut])
async def trust_scores(db: AsyncSession = Depends(get_db)):
    """Latest trust scores per ward."""
    # Get latest date per ward
    subq = (
        select(
            TrustScore.ward_id,
            func.max(TrustScore.date).label("max_date"),
        )
        .group_by(TrustScore.ward_id)
        .subquery()
    )
    stmt = (
        select(TrustScore)
        .join(
            subq,
            (TrustScore.ward_id == subq.c.ward_id)
            & (TrustScore.date == subq.c.max_date),
        )
        .order_by(desc(TrustScore.final_trust_score))
    )
    result = await db.execute(stmt)
    return [TrustScoreOut.model_validate(t) for t in result.scalars().all()]
